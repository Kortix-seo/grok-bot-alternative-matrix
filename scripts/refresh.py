#!/usr/bin/env python3
"""Re-read the machine-checkable fields of data/alternatives.json from GitHub.

What it checks, and why only these: a product's licence, whether its repository
is archived, and when it last took a push are the only comparison fields a
public API states without interpretation. The rest of the matrix (isolation
unit, hosting, review gate, price shape) is a claim about a product page, so
this script prints those rows for a human to re-read and never rewrites them.

    python3 scripts/refresh.py            # report drift, exit 1 if any
    python3 scripts/refresh.py --write    # apply licence/archived drift

No dependencies: urllib from the standard library. Set GITHUB_TOKEN to raise
the unauthenticated 60 requests/hour ceiling for a full sweep of the matrix.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
MATRIX = HERE / "data" / "alternatives.json"

# product -> repository the licence column is read from. A product with no
# repository (a hosted service) is not in this map: its licence is not a
# machine-readable fact, so it is left for a human to re-read.
REPOS = {
    "Rakazo": "elie222/rakazo",
    "OpenMausBot": "milind-soni/OpenMausBot",
    "OpenClaw": "openclaw/openclaw",
    "Hermes Agent": "NousResearch/hermes-agent",
    "OpenHands": "OpenHands/OpenHands",
    "Kortix": "kortix-ai/suna",
}


def get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("AGENT_KORTIX_GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main(argv: list[str]) -> int:
    write = "--write" in argv
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    drift = 0
    for row in matrix["rows"]:
        repo = REPOS.get(row["product"])
        if not repo:
            print(f"{row['product']}: no repository — re-read {row['sources'][0]['url']} by hand")
            continue
        try:
            meta = get(f"https://api.github.com/repos/{repo}")
        except urllib.error.HTTPError as e:
            print(f"{row['product']}: GitHub API {e.code} for {repo}")
            drift += 1
            continue
        licence = ((meta.get("license") or {}).get("spdx_id") or "NOASSERTION")
        archived = bool(meta.get("archived"))
        pushed = (meta.get("pushed_at") or "")[:10]
        stale = row["sources"][0]["read"]
        # a licence change or an archived repository changes what the row says
        if row["product"] != "Kortix" and licence != row["licence"]:
            print(f"{row['product']}: licence {row['licence']} -> {licence} ({repo})")
            if write:
                row["licence"] = licence
            drift += 1
        if archived:
            print(f"{row['product']}: repository archived — the row needs a human re-read")
            drift += 1
        if pushed and stale and pushed > stale:
            print(f"{row['product']}: pushed {pushed} after the row's read date {stale} — re-read its page")
            drift += 1
        print(f"{row['product']}: {licence}, archived={archived}, last push {pushed}")
    if write and drift:
        matrix["built"] = date.today().isoformat()
        MATRIX.write_text(json.dumps(matrix, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {MATRIX}")
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
