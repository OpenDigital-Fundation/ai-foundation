"""Build generated files.

  python -m tools.build                 regenerate .claude-plugin/marketplace.json
  python -m tools.build profile <name>  print the install plan for a profile
"""
import json
import sys
from pathlib import Path

from tools.build import marketplace, profiles

root = Path(".").resolve()
if len(sys.argv) >= 3 and sys.argv[1] == "profile":
    print(json.dumps(profiles.resolve(root, sys.argv[2]), indent=2))
else:
    print(f"wrote {marketplace.write(root).relative_to(root)}")
