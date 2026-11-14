"""Build generated files.

  python -m tools.build                 regenerate .claude-plugin/marketplace.json
  python -m tools.build profile <name>  print the install plan for a profile
  python -m tools.build docs            regenerate domains/*/README.md, docs/CATALOG.md and docs/SOURCES.md
  python -m tools.build adapters [dir]  project the catalog onto Codex/Cursor/Gemini/OpenCode layouts (default dist/)
  python -m tools.build release <new-dir>  build complete/per-client/per-skill ZIPs
"""
import json
import sys
from pathlib import Path

from tools.build import adapters, docs, marketplace, profiles

root = Path(".").resolve()
if len(sys.argv) >= 2 and sys.argv[1] == "release":
    from tools.build.release import main
    main(sys.argv[2:])
elif len(sys.argv) >= 2 and sys.argv[1] == "docs":
    print(f"wrote {len(docs.write_all(root))} index files")
elif len(sys.argv) >= 2 and sys.argv[1] == "adapters":
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "dist").resolve()
    print(adapters.build_all(root, out), "->", out)
elif len(sys.argv) >= 3 and sys.argv[1] == "profile":
    print(json.dumps(profiles.resolve(root, sys.argv[2]), indent=2))
else:
    print(f"wrote {marketplace.write(root).relative_to(root)}")
