<!-- Modified by OpenDigital from openai/skills (Apache-2.0). See PROVENANCE.yaml in this domain. -->
# Browser testing — derived guides

Part of `testing:browser-testing`.

## Playwright Interactive Skill

<!-- source: openai/skills skills/.curated/playwright-interactive/SKILL.md#viewport-fit-checks-required -->

### Viewport Fit Checks (Required)

Do not assume a screenshot is acceptable just because the main widget is visible. Before signoff, explicitly verify that the intended initial view matches the product requirement, using both screenshot review and numeric checks.

- Define the intended initial view before signoff. For scrollable pages, this is the above-the-fold experience. For app-like shells, games, editors, dashboards, or tools, this is the full interactive surface plus the controls and status needed to use it.
- Use screenshots as the primary evidence for fit. Numeric checks support the screenshots; they do not overrule visible clipping.
- Signoff fails if any required visible region is clipped, cut off, obscured, or pushed outside the viewport in the intended initial view, even if page-level scroll metrics appear acceptable.
- Scrolling is acceptable when the product is designed to scroll and the initial view still communicates the core experience and exposes the primary call to action or required starting context.
- For fixed-shell interfaces, scrolling is not an acceptable workaround if it is needed to reach part of the primary interactive surface or essential controls.
- Do not rely on document scroll metrics alone. Fixed-height shells, internal panes, and hidden-overflow containers can clip required UI while page-level scroll checks still look clean.
- Check region bounds, not just document bounds. Verify that each required visible region fits within the viewport in the startup state.
- For Electron or desktop apps, verify both the launched window size and placement and the renderer's initial visible layout before any manual resize or repositioning.
- Passing viewport-fit checks only proves that the intended initial view is visible without unintended clipping or scrolling. It does not prove that the UI is visually correct or aesthetically successful.

Web or renderer check:

```javascript
console.log(await page.evaluate(() => ({
  innerWidth: window.innerWidth,
  innerHeight: window.innerHeight,
  clientWidth: document.documentElement.clientWidth,
  clientHeight: document.documentElement.clientHeight,
  scrollWidth: document.documentElement.scrollWidth,
  scrollHeight: document.documentElement.scrollHeight,
  canScrollX: document.documentElement.scrollWidth > document.documentElement.clientWidth,
  canScrollY: document.documentElement.scrollHeight > document.documentElement.clientHeight,
})));
```

Electron check:

```javascript
console.log(await appWindow.evaluate(() => ({
  innerWidth: window.innerWidth,
  innerHeight: window.innerHeight,
  clientWidth: document.documentElement.clientWidth,
  clientHeight: document.documentElement.clientHeight,
  scrollWidth: document.documentElement.scrollWidth,
  scrollHeight: document.documentElement.scrollHeight,
  canScrollX: document.documentElement.scrollWidth > document.documentElement.clientWidth,
  canScrollY: document.documentElement.scrollHeight > document.documentElement.clientHeight,
})));
```

Augment the numeric check with `getBoundingClientRect()` checks for the required visible regions in your specific UI when clipping is a realistic failure mode; document-level metrics alone are not sufficient for fixed shells.

## UI Screenshots

<!-- source: github/awesome-copilot skills/ui-screenshots/SKILL.md#non-web-app-screenshots -->

### Non-Web App Screenshots

For desktop apps (VS, WPF, WinForms, console apps, terminals) where Playwright can't reach.

#### mss + ctypes (recommended for desktop windows)

Find a window by title via Win32 API, capture its region with `mss`. Tested at ~33ms per capture.

```python
import ctypes
from ctypes import c_int, Structure, byref, windll
import mss
from PIL import Image

user32 = windll.user32

def find_window(title_contains):
    """Find visible windows matching a title substring."""
    results = []
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(hwnd, _):
        if user32.IsWindowVisible(hwnd):
            buf = ctypes.create_unicode_buffer(256)
            user32.GetWindowTextW(hwnd, buf, 256)
            if title_contains.lower() in buf.value.lower():
                results.append((hwnd, buf.value))
        return True
    user32.EnumWindows(WNDENUMPROC(cb), 0)
    return results

def capture_window(title_contains, output_path):
    """Capture a window by title substring."""
    windows = find_window(title_contains)
    if not windows:
        raise ValueError(f"No window matching '{title_contains}'")
    hwnd = windows[0][0]

    class RECT(Structure):
        _fields_ = [('left', c_int), ('top', c_int), ('right', c_int), ('bottom', c_int)]
    rect = RECT()
    user32.GetWindowRect(hwnd, byref(rect))
    w, h = rect.right - rect.left, rect.bottom - rect.top

    with mss.mss() as sct:
        shot = sct.grab({'left': rect.left, 'top': rect.top, 'width': w, 'height': h})
        img = Image.frombytes('RGB', shot.size, shot.rgb)
        img.save(output_path)
        return img

# Usage:
capture_window('Visual Studio Code', 'vscode-capture.png')
```

**Prerequisites:** `pip install mss pillow`
**Limitation:** Window must be visible (not behind other windows or minimized).

#### Electron apps (VS Code, etc.)

**Node.js Playwright only** — Python Playwright has no `electron` API. Captures via CDP (Chrome DevTools Protocol), not from the screen — works even while minimized.

```javascript
const { _electron: electron } = require('playwright');
const app = await electron.launch({
    executablePath: 'C:\\Program Files\\Microsoft VS Code\\Code.exe',
    args: ['--new-window', '--disable-extensions', '--user-data-dir=' + tmpDir]
});
const window = await app.firstWindow();
await window.waitForLoadState('domcontentloaded');

// Minimize immediately — captures still work via CDP
await app.evaluate(({ BrowserWindow }) => {
    BrowserWindow.getAllWindows()[0].minimize();
});

await window.screenshot({ path: 'capture.png' }); // works while minimized!
await app.close();
```

**Critical**: `--user-data-dir=<temp>` is required or VS Code hands off to the existing instance and the launched process exits immediately.

#### Decision tree

| Scenario | Tool | Notes |
|---|---|---|
| Web app (localhost) | Playwright | Proven, full DOM access |
| Electron app (VS Code) | Playwright Electron (Node.js) | Works minimized via CDP |
| Desktop app, visible window | mss + ctypes (find by title) | ~33ms per capture |
| Desktop app, behind windows | Windows Graphics Capture API | Complex setup, Win10 1903+ |
| Quick full-screen | mss | ~68ms |

## Cypress Flake Fixer

<!-- source: github/awesome-copilot skills/cypress-flake-fixer/SKILL.md#gotchas -->

### Gotchas

- **Register `cy.intercept()` before the request can fire.** For requests made on page load that means before `cy.visit()`. An intercept registered after the request has left never matches, and `cy.wait('@alias')` times out intermittently depending on network speed.
- **Each `cy.wait('@alias')` consumes one request.** If the app calls the endpoint twice, the first wait resolves on the first call and the assertion runs against stale data. Wait once per expected call, or assert on the DOM.
- **GraphQL uses one URL for every operation.** Alias inside the handler: `cy.intercept('POST', '/graphql', (req) => { if (req.body.operationName === 'GetOrders') req.alias = 'getOrders' })`.
- **`.should('not.exist')` passes before the element has rendered.** Using it to wait for a spinner to disappear succeeds instantly on a slow page. Assert the positive end state.
- **Server-rendered apps accept clicks before handlers are attached.** In Next.js, Nuxt, SvelteKit, and Remix the button is visible and enabled in the server HTML, so Cypress clicks it during hydration and nothing happens. Have the app set a marker when hydration completes (for example a `data-hydrated` attribute on `<body>` from a mount effect) and assert on it after `cy.visit()`.
- **A `.should()` in the middle of a chain pins the subject.** Queries after it cannot re-query past the assertion, so a re-render produces a detached-DOM error. Split the chain at the assertion.
- **`.then()` breaks the retry chain even with no assertion inside.** Everything before it runs once.
- **Cypress 16 types with no delay between keys** (`keystrokeDelay` default changed from 10 to 0). Inputs that re-render per keystroke or debounce on input may now drop characters or fire once. Assert the field value after typing instead of restoring the delay.
- **Cypress 16 turned cookie and storage getters into queries.** `cy.getCookie()`, `cy.getCookies()`, `cy.getAllCookies()`, `cy.getAllLocalStorage()`, and `cy.getAllSessionStorage()` now retry chained `.should()` assertions, which removes the need for waits around auth cookies.
- **The page is blank after `cy.session()`.** A missing `cy.visit()` after it looks like a flaky selector failure.
- **`testIsolation: false` shares state across tests.** If the config sets it, every order-dependent failure is expected behavior, not flake. Check the config before diagnosing.
- **Retries hide flake unless configured to report it.** To find flaky tests instead of masking them, use the experimental strategy that retries and still fails:

  ```js
  retries: {
    experimentalStrategy: 'detect-flake-but-always-fail',
    experimentalOptions: { maxRetries: 2, stopIfAnyPassed: true },
    openMode: true,
    runMode: true,
  }
  ```

- **CY005 is a judgement call.** `cy.get(input).clear().type('x')` on an input that never re-renders is fine. Split the chain when the element belongs to a list, a form library that remounts fields, or anything driven by async state.
