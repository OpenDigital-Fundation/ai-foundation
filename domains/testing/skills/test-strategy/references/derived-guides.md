<!-- Modified by OpenDigital from github/awesome-copilot (Apache-2.0). See PROVENANCE.yaml in this domain. -->
# Test strategy — derived guides

Part of `testing:test-strategy`.

## Quality Playbook Generator

<!-- source: github/awesome-copilot skills/quality-playbook/SKILL.md#recheck-mode-verify-bug-fixes -->

### Recheck Mode — Verify Bug Fixes

Recheck mode is a lightweight verification pass that checks whether bugs from a previous run have been fixed. Instead of re-running the full six-phase pipeline (60-90 minutes), recheck reads the existing `quality/BUGS.md`, checks each bug against the current source tree, and reports which bugs are fixed vs. still open. A typical recheck takes 2-10 minutes.

**When to use recheck mode:** After the user (or another agent) has applied fixes for bugs found by the playbook. The user says "recheck" or "verify the bug fixes" or "check which bugs are fixed."

**Do not use recheck mode** as a substitute for running the full playbook. Recheck only verifies previously found bugs — it does not find new ones.

#### Recheck procedure

**Step 1: Read the bug inventory.**

Read `quality/BUGS.md` and parse every `### BUG-NNN` entry. For each bug, extract:
- Bug ID (e.g., BUG-001)
- File path and line number from the `**File:**` field
- Description summary (first sentence of `**Description:**`)
- Severity
- Fix patch path from `**Fix patch:**` field (e.g., `quality/patches/BUG-001-fix.patch`)
- Regression test path from `**Regression test:**` field

**Step 2: Check each bug against the current source.**

For each bug, perform these checks in order:

1. **Fix patch check.** If a fix patch exists at the referenced path, run `git apply --check --reverse quality/patches/BUG-NNN-fix.patch` against the current tree. If the reverse-apply succeeds (exit 0), the fix patch is already applied — the bug is likely fixed. If it fails, the fix has not been applied or the code has changed.

2. **Source inspection.** Open the file at the cited line number. Read the surrounding context (±20 lines). Compare what you see against the bug description. Has the problematic code been changed? Does the fix address the root cause described in the bug report?

3. **Regression test execution.** If a regression test patch exists:
   - Apply it: `git apply quality/patches/BUG-NNN-regression-test.patch`
   - Run the test (using the project's test runner). If the test PASSES, the bug is fixed. If it FAILS, the bug is still present.
   - Reverse the patch: `git apply -R quality/patches/BUG-NNN-regression-test.patch`
   
   If the regression test patch doesn't apply cleanly (because the source has changed), note this and fall back to source inspection alone.

4. **Verdict.** Assign one of these statuses:
   - **FIXED** — Fix patch is applied AND regression test passes (or source inspection confirms the fix if test can't run)
   - **PARTIALLY_FIXED** — The problematic code has changed but the regression test still fails, or the fix addresses some but not all aspects of the bug
   - **STILL_OPEN** — The original problematic code is unchanged, or the regression test still fails
   - **INCONCLUSIVE** — Can't determine status (file moved, code heavily refactored, patches don't apply)

**Step 3: Generate recheck results.**

Write `quality/results/recheck-results.json` with this schema:

Note: The recheck schema uses `"schema_version": "1.0"` (not `"1.1"`) because it has a different structure from the TDD sidecar — the `source_run` and per-bug `status`/`evidence` fields are unique to the recheck schema. The quality gate validates this value as `"1.0"`.

```json
{
  "schema_version": "1.0",
  "skill_version": "1.5.6",
  "date": "YYYY-MM-DD",
  "project": "<project name>",
  "source_run": {
    "bugs_md_date": "<date from BUGS.md header>",
    "total_bugs": <N>
  },
  "results": [
    {
      "id": "BUG-001",
      "severity": "HIGH",
      "summary": "<one-line summary>",
      "status": "FIXED",
      "evidence": "<what confirmed the fix — e.g., 'reverse-apply succeeded + regression test passes'>"
    }
  ],
  "summary": {
    "total": <N>,
    "fixed": <N>,
    "partially_fixed": <N>,
    "still_open": <N>,
    "inconclusive": <N>
  }
}
```

Also write a human-readable summary to `quality/results/recheck-summary.md`:

```markdown
# Recheck Results

> Recheck of quality/BUGS.md from <date>
> Recheck run: <today's date>
> Skill version: <version>

## Summary

| Status | Count |
|--------|-------|
| Fixed | N |
| Partially fixed | N |
| Still open | N |
| Inconclusive | N |
| **Total** | **N** |

## Per-Bug Results

| Bug | Severity | Status | Evidence |
|-----|----------|--------|----------|
| BUG-001 | HIGH | FIXED | Reverse-apply succeeded, regression test passes |
| BUG-002 | MEDIUM | STILL_OPEN | Original code unchanged at quality_gate.py:125 |
| ... | ... | ... | ... |

## Still Open — Details

[For each STILL_OPEN or PARTIALLY_FIXED bug, include a brief explanation of what remains to be fixed.]
```

**Step 4: Print the recheck summary.**

Print the summary table to the user, then STOP. Example:

```
# Recheck Complete

Checked 19 bugs from quality/BUGS.md against current source.

| Status | Count |
|--------|-------|
| Fixed | 17 |
| Still open | 2 |
| **Total** | **19** |

Fixed bugs: BUG-001, BUG-002, BUG-003, BUG-004, BUG-005, BUG-006, BUG-007,
BUG-008, BUG-009, BUG-010, BUG-011, BUG-013, BUG-014, BUG-015, BUG-016,
BUG-017, BUG-018

Still open: BUG-012 (stale .orig file still present), BUG-019 (benchmark 40
artifact list not updated)

Results saved to:
- quality/results/recheck-results.json (machine-readable)
- quality/results/recheck-summary.md (human-readable)
```

#### Triggering recheck mode

Recheck mode activates when the user says any of: "recheck", "verify the bug fixes", "check which bugs are fixed", "recheck the bugs", "run recheck mode", or similar phrasing that clearly indicates they want to verify fixes rather than find new bugs. When triggered, skip Phases 1-7 entirely and execute only the recheck procedure above.

---

## Flaky Test Triage

<!-- source: davila7/claude-code-templates cli-tool/components/commands/testing`testing:test-driven-development`-triage.md#triage-stabilization-workflow -->

### Triage & Stabilization Workflow

#### 1. Stress Repetition to Measure Flake Frequency

Run the target test for 20 iterations without breaking early on first error so the full pass/fail ratio and flake frequency can be accurately quantified:

- **Vitest**:
  ```bash
  passes=0; fails=0
  for i in $(seq 1 20); do
    if npx vitest run <path-to-test>; then ((++passes)); else ((++fails)); fi
  done
  echo "Vitest Results: $passes passed, $fails failed out of 20 runs"
  ```
- **Jest**:
  ```bash
  passes=0; fails=0
  for i in $(seq 1 20); do
    if npx jest <path-to-test> --runInBand; then ((++passes)); else ((++fails)); fi
  done
  echo "Jest Results: $passes passed, $fails failed out of 20 runs"
  ```
- **Pytest**:
  ```bash
  passes=0; fails=0
  for i in $(seq 1 20); do
    if pytest <path-to-test> -v; then ((++passes)); else ((++fails)); fi
  done
  echo "Pytest Results: $passes passed, $fails failed out of 20 runs"
  ```
- **Go**:
  ```bash
  go test -count=20 -run <TestName> <package-path>
  ```
- **Cargo**:
  ```bash
  passes=0; fails=0
  for i in $(seq 1 20); do
    if cargo test <test_name> -- --nocapture; then ((++passes)); else ((++fails)); fi
  done
  echo "Cargo Results: $passes passed, $fails failed out of 20 runs"
  ```

Record the pass/fail ratio and capture stdout/stderr from failed iterations.

#### 2. Diagnose Flake Root Cause

Categorize the failure using the common non-determinism taxonomy:

1. **Timing & Asynchronous Race Conditions**:
   - Symptom: Fails under high CPU load or CI runners; passes on fast local hardware.
   - Indicators: Arbitrary `sleep()`, `setTimeout()`, or unawaited promises/goroutines.
   - Root cause: Test asserts before an asynchronous background operation resolves.

2. **Test Order Dependency & State Pollution**:
   - **Symptom**: Passes when executed in isolation (`--testNamePattern`), fails when the entire suite runs.
   - **Indicators**: Leaked global variables, uncleared database records, singleton caches, or shared filesystem artifacts.
   - **Verification**: Use the framework's shuffle support when it is installed. For Pytest, detect optional plugins before passing their flags:
     ```bash
     if pytest --help 2>/dev/null | grep -q -- '--random-order'; then
       pytest <path-to-test> --random-order
     elif pytest --help 2>/dev/null | grep -q -- '--randomly-seed'; then
       pytest <path-to-test> --randomly-seed=random
     else
       echo 'No Pytest randomization plugin detected; record order-randomization as unavailable.'
       pytest <path-to-test> -v
     fi
     ```
     Do not pass `--random-order` or `--randomly-seed` unless the corresponding plugin advertises the option.

3. **Clock & Timezone Skew**:
   - Symptom: Fails around midnight UTC, during month/year rollovers, or in different local timezones.
   - Indicators: Unmocked `Date.now()`, `new Date()`, `datetime.utcnow()`, or reliance on implicit locale sorting.

4. **Resource & Port Contention**:
   - Symptom: `EADDRINUSE`, file locking errors, or database transaction deadlocks when run concurrently.
   - Indicators: Hardcoded network ports, static temporary file names, or shared test database schemas.

#### 3. Apply Targeted Stabilization Patterns

Implement the appropriate pattern based on the diagnosed category:

- **Replace Arbitrary Delays with Condition-Based Polling**:
  Avoid static `sleep(1000)`. Instead, use poll-based assertions with explicit timeouts:
  ```typescript
  // Bad
  await sleep(500);
  expect(await getStatus()).toBe("completed");

  // Good
  await waitFor(async () => {
    expect(await getStatus()).toBe("completed");
  }, { timeout: 5000, interval: 50 });
  ```

- **Enforce Clean Teardown & Mock Restoration**:
  Ensure global mocks, timers, and database tables are cleared in `afterEach` hooks:
  ```typescript
  afterEach(async () => {
    vi.restoreAllMocks();
    vi.useRealTimers();
    await cleanupDatabase();
  });
  ```

- **Dynamic Resource Isolation**:
  Use ephemeral ports (`0` for OS-assigned port) and unique temporary folders per test run:
  ```typescript
  const testDir = await fs.promises.mkdtemp(path.join(os.tmpdir(), "test-run-"));
  ```

#### 4. Verification & Stability Certification

1. Verify stability by executing 50 consecutive iterations (stopping on any failure to observe if flake reoccurs):
   ```bash
   for i in $(seq 1 50); do
     <test-command> || { echo "Stability check failed on iteration $i"; exit 1; }
   done
   echo "Stability check passed: 50/50 consecutive runs passed without failure."
   ```
2. Run the enclosing test file with randomized test ordering when the framework supports it. Do not assume optional Pytest plugins are installed:
   ```bash
   # Vitest:
   npx vitest run <path-to-test> --sequence.shuffle.tests

   # Pytest:
   if pytest --help 2>/dev/null | grep -q -- '--random-order'; then
     pytest <path-to-test> --random-order
   elif pytest --help 2>/dev/null | grep -q -- '--randomly-seed'; then
     pytest <path-to-test> --randomly-seed=random
   else
     echo 'Pytest shuffle check unavailable: install pytest-random-order or pytest-randomly to enable it.'
     pytest <path-to-test> -v
   fi
   ```
3. Run the complete project test suite to guarantee zero regressions:
   ```bash
   npm test
   ```

#### 5. Report Findings

Summarize:
- **Flake Rate Before**: e.g., 3 failures out of 20 runs (15% flake rate).
- **Identified Root Cause**: Specific race condition, state leak, or timing dependency.
- **Remediation Applied**: Exact code changes made to stabilize the test.
- **Verification Result**: 50/50 consecutive runs passed without error.

## JavaScript Testing Patterns

<!-- source: wshobson/agents plugins/javascript-typescript/skills`testing:test-driven-development`ing-patterns/SKILL.md#unit-testing-patterns -->

### Unit Testing Patterns

#### Pattern 1: Testing Pure Functions

```typescript
// utils/calculator.ts
export function add(a: number, b: number): number {
  return a + b;
}

export function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error("Division by zero");
  }
  return a / b;
}

// utils/calculator.test.ts
import { describe, it, expect } from "vitest";
import { add, divide } from "./calculator";

describe("Calculator", () => {
  describe("add", () => {
    it("should add two positive numbers", () => {
      expect(add(2, 3)).toBe(5);
    });

    it("should add negative numbers", () => {
      expect(add(-2, -3)).toBe(-5);
    });

    it("should handle zero", () => {
      expect(add(0, 5)).toBe(5);
      expect(add(5, 0)).toBe(5);
    });
  });

  describe("divide", () => {
    it("should divide two numbers", () => {
      expect(divide(10, 2)).toBe(5);
    });

    it("should handle decimal results", () => {
      expect(divide(5, 2)).toBe(2.5);
    });

    it("should throw error when dividing by zero", () => {
      expect(() => divide(10, 0)).toThrow("Division by zero");
    });
  });
});
```

#### Pattern 2: Testing Classes

```typescript
// services/user.service.ts
export class UserService {
  private users: Map<string, User> = new Map();

  create(user: User): User {
    if (this.users.has(user.id)) {
      throw new Error("User already exists");
    }
    this.users.set(user.id, user);
    return user;
  }

  findById(id: string): User | undefined {
    return this.users.get(id);
  }

  update(id: string, updates: Partial<User>): User {
    const user = this.users.get(id);
    if (!user) {
      throw new Error("User not found");
    }
    const updated = { ...user, ...updates };
    this.users.set(id, updated);
    return updated;
  }

  delete(id: string): boolean {
    return this.users.delete(id);
  }
}

// services/user.service.test.ts
import { describe, it, expect, beforeEach } from "vitest";
import { UserService } from "./user.service";

describe("UserService", () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
  });

  describe("create", () => {
    it("should create a new user", () => {
      const user = { id: "1", name: "John", email: "john@example.com" };
      const created = service.create(user);

      expect(created).toEqual(user);
      expect(service.findById("1")).toEqual(user);
    });

    it("should throw error if user already exists", () => {
      const user = { id: "1", name: "John", email: "john@example.com" };
      service.create(user);

      expect(() => service.create(user)).toThrow("User already exists");
    });
  });

  describe("update", () => {
    it("should update existing user", () => {
      const user = { id: "1", name: "John", email: "john@example.com" };
      service.create(user);

      const updated = service.update("1", { name: "Jane" });

      expect(updated.name).toBe("Jane");
      expect(updated.email).toBe("john@example.com");
    });

    it("should throw error if user not found", () => {
      expect(() => service.update("999", { name: "Jane" })).toThrow(
        "User not found",
      );
    });
  });
});
```

#### Pattern 3: Testing Async Functions

```typescript
// services/api.service.ts
export class ApiService {
  async fetchUser(id: string): Promise<User> {
    const response = await fetch(`https://api.example.com/users/${id}`);
    if (!response.ok) {
      throw new Error("User not found");
    }
    return response.json();
  }

  async createUser(user: CreateUserDTO): Promise<User> {
    const response = await fetch("https://api.example.com/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(user),
    });
    return response.json();
  }
}

// services/api.service.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { ApiService } from "./api.service";

// Mock fetch globally
global.fetch = vi.fn();

describe("ApiService", () => {
  let service: ApiService;

  beforeEach(() => {
    service = new ApiService();
    vi.clearAllMocks();
  });

  describe("fetchUser", () => {
    it("should fetch user successfully", async () => {
      const mockUser = { id: "1", name: "John", email: "john@example.com" };

      (fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockUser,
      });

      const user = await service.fetchUser("1");

      expect(user).toEqual(mockUser);
      expect(fetch).toHaveBeenCalledWith("https://api.example.com/users/1");
    });

    it("should throw error if user not found", async () => {
      (fetch as any).mockResolvedValueOnce({
        ok: false,
      });

      await expect(service.fetchUser("999")).rejects.toThrow("User not found");
    });
  });

  describe("createUser", () => {
    it("should create user successfully", async () => {
      const newUser = { name: "John", email: "john@example.com" };
      const createdUser = { id: "1", ...newUser };

      (fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => createdUser,
      });

      const user = await service.createUser(newUser);

      expect(user).toEqual(createdUser);
      expect(fetch).toHaveBeenCalledWith(
        "https://api.example.com/users",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify(newUser),
        }),
      );
    });
  });
});
```
