"""Read-only lexical search of the bundled Foundation catalog (standard library only).

python3 scripts/find.py "design instrucional" --json
The snapshot describes catalog availability, not what is installed on this machine.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import unicodedata

STOP = set("a an and as at by for from in is of on or the to use when with what which can i me my our skill skills agent agents de da do das dos e em o os para por com um uma qual quais quero nosso nossa".split())


def normalize(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", unicodedata.normalize("NFKD", text.casefold()).encode("ascii", "ignore").decode()))


def search(index: dict, query: str, *, domain: str | None = None, kind: str | None = None,
           limit: int = 5, include_deprecated: bool = False) -> dict:
    if index.get("version") != 1 or not isinstance(index.get("artifacts"), list):
        raise ValueError("unsupported catalog index")
    if not 1 <= limit <= 50:
        raise ValueError("limit must be between 1 and 50")
    entries = index["artifacts"]
    if domain is not None and domain not in {a["domain"] for a in entries}:
        raise ValueError(f"unknown domain: {domain}")
    if kind is not None and kind not in {a["type"] for a in entries}:
        raise ValueError(f"unknown artifact type: {kind}")
    words = set(normalize(query).split()) - STOP
    normalized = normalize(query)
    matches = []
    considered = 0
    for a in entries:
        if domain is not None and a["domain"] != domain:
            continue
        if kind is not None and a["type"] != kind:
            continue
        if not include_deprecated and a["status"] == "deprecated":
            continue
        considered += 1
        fields = {"id": (a["id"], 20), "terms": (" ".join(a.get("terms", [])), 14),
                  "description": (a["description"], 6), "domain": (a["domain"], 4),
                  "facets": (" ".join(a.get("facets", [])), 2),
                  "sources": (" ".join(a.get("sources", [])), 1)}
        tokens = {key: set(normalize(value).split()) for key, (value, _) in fields.items()}
        reasons = {word: [key for key in fields if word in tokens[key]] for word in sorted(words)}
        if words and not all(reasons.values()):
            continue
        score = sum(max(fields[key][1] for key in keys) for keys in reasons.values())
        if normalized and normalized == normalize(a["id"]):
            score += 1000
        matches.append({"id": a["id"], "type": a["type"], "status": a["status"],
                        "description": a["description"], "source_path": a["path"],
                        "lexical_score": score, "matched_fields": reasons})
    matches.sort(key=lambda a: (-a["lexical_score"], a["id"]))
    return {"query": query, "catalog_size": len(entries), "searched": considered,
            "total_matches": len(matches), "returned": min(limit, len(matches)),
            "source_digest": index.get("source_digest"),
            "availability": "Catalog entries only; local installation was not checked.",
            "ranking": "Deterministic lexical matches, not quality or effectiveness scores.",
            "results": matches[:limit]}


def main(argv: list[str] | None = None, *, index: dict | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="*", help="short keywords, canonical ID or curated pt/en terms")
    parser.add_argument("--domain")
    parser.add_argument("--type", dest="kind")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--include-deprecated", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    if index is None:
        parser.add_argument("--index", type=Path, default=Path(__file__).resolve().parents[1] / "assets/catalog-index.json")
    args = parser.parse_args(argv)
    try:
        if index is None:
            index = json.loads(args.index.read_text(encoding="utf-8"))
        result = search(index, " ".join(args.query), domain=args.domain, kind=args.kind,
                        limit=args.limit, include_deprecated=args.include_deprecated)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['total_matches']} matches in {result['searched']} / {result['catalog_size']} catalog entries; showing {result['returned']}.")
        for a in result["results"]:
            print(f"{a['id']} [{a['type']}, {a['status']}]\n  {a['description']}\n  {a['source_path']}")
        print(result["availability"])
        if not result["results"]:
            print("Try fewer keywords or another curated pt/en term; no external search was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
