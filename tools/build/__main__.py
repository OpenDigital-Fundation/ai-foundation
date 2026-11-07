"""Build generated files.

  python -m tools.build                 regenerate .claude-plugin/marketplace.json
  python -m tools.build profile <name>  print the install plan for a profile
  python -m tools.build adapters [dir]  project the catalog onto Codex/Cursor/Gemini/OpenCode layouts (default dist/)
"""
import json
import sys
from pathlib import Path

from tools.build import adapters, marketplace, profiles

root = Path(".").resolve()
if len(sys.argv) >= 2 and sys.argv[1] == "adapters":
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "dist").resolve()
    print(adapters.build_all(root, out), "->", out)
elif len(sys.argv) >= 3 and sys.argv[1] == "profile":
    print(json.dumps(profiles.resolve(root, sys.argv[2]), indent=2))
else:
    print(f"wrote {marketplace.write(root).relative_to(root)}")
