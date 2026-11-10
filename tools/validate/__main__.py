"""Run all static catalog checks: python -m tools.validate [repo-root]"""
import sys
from pathlib import Path

from tools.validate.checks import run_all


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errs, warns = run_all(root)
    for w in warns:
        print(f"warning: {w}")
    for e in errs:
        print(f"error: {e}")
    print(f"{len(errs)} error(s), {len(warns)} warning(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
