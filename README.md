# grok-bot-alternative-matrix

Open-source answer to the question "what replaces Grok Bot?", kept as data you can run instead of a listicle you have to trust.

The matrix below is one row per product a searcher actually compares against xAI's Grok Bot, with the four fields that decide whether an agent's work can be reviewed: what one agent gets on its own, where its machine runs, whether you can run it yourself, and what stands between its change and production. Every value carries the URL it was read from and the date, in `data/alternatives.json`.

Last full read: **2026-10-31**. `scripts/refresh.py` re-checks the licensing and liveness fields and tells you which rows have gone stale.

## The matrix

| Product | Isolation unit | Where the machine runs | Self-hosted | Review gate | Licence | Price shape |
|---|---|---|---|---|---|---|
| **Kortix** | per session | Kortix Cloud, your own VPC, or your on-prem network | yes | session work reaches `main` through a change request; merge is default-deny for agents | open source (see [the repository](https://github.com/kortix-ai/CompanyOS)) | 100 credits per dollar; $50 buys 5,000 credits; the sandbox bills per second |
| Grok Bot | per user, not per Bot | Cursor-hosted cloud computers | no | an approval card per proposed action | proprietary | $30/mo Premium, $100/mo Super, $200/mo Ultra; one weekly usage pool |
| Rakazo | shared team computers plus isolated private ones | self-hosted (Docker, E2B, Daytona, CreateOS, Boat, or a local computer) | yes | per-computer approval rules | Apache-2.0 | no published price; you pay for the host and the models |
| OpenMausBot | one cloud computer per bot | the app on your machine, or the vendor's hosted plan | yes | per-bot settings; no team merge gate | Apache-2.0 | self-hosted free; hosted Starter $15/mo with 100 computer-hours |
| OpenClaw | one gateway, personal or shared | your own computer | yes | none by default | MIT | no paid tier, hosted service or token |
| Hermes Agent | one agent process | your machine or server | yes | skill writes staged for the operator's approval | MIT | no published price; model cost only |
| OpenHands | one container per conversation | local Docker or the vendor's cloud | yes | a diff in your own repository | MIT | open source; the cloud plan meters model and compute |

Kortix is the open-source CompanyOS these rows are measured against: agents, skills and memory are files in a git repository your team owns, and every session runs on its own isolated machine and branch (https://kortix.com).

## Why those four fields

A list of "alternatives" is usually a list of names. The question behind it is narrower: when an agent changes something, who can read the change, and what else was on the machine when it did?

- **Isolation unit** — a machine per session means one session's files, logins and processes are not another's. A per-user machine shared by several bots means the opposite, by design: the hand-off works because everything is on one disk.
- **Where the machine runs** — a vendor-hosted computer is a hosting contract. It decides whether your review process, your network policy and your data residency apply to the work at all.
- **Self-hosted** — not "open source in principle": whether a deployment a customer installs exists today.
- **Review gate** — an approval card is a decision about a proposed action; it does not undo work already done. A merge gate is a decision about a change that has not landed yet.

## Use it

```bash
git clone https://github.com/Kortix-seo/grok-bot-alternative-matrix
cd grok-bot-alternative-matrix
python3 scripts/refresh.py            # report drift since the last read
python3 scripts/refresh.py --write    # apply licence/archived drift to the JSON
```

`refresh.py` uses only the standard library. Set `GITHUB_TOKEN` to raise GitHub's unauthenticated rate limit.

Query the data instead of reading the table:

```bash
python3 - <<'PY'
import json
rows = json.load(open("data/alternatives.json"))["rows"]
for r in rows:
    print(f"{r['product']:<14} {r['isolation_unit']:<40} self-hosted={r['self_hosted']}")
PY
```

## Method

`docs/METHOD.md` says what each column means, which URL each value came from, and what this matrix deliberately does not compare (benchmarks, GitHub popularity, model quality). Corrections are welcome as a pull request that changes a row **and** its source URL and read date; a row without both is not a fact.

## Licence

The scripts and data in this repository are MIT. The products in the matrix keep their own licences, listed in the `licence` column and in each row's `sources`.

## Deeper reading

Each row above answers one question. Four of them are argued at length, with the vendor quotes beside the claim:

- [Every Grok Bot alternative in the matrix, compared](https://grokbotalternatives.com/grok-bot-alternatives) — the full table with the fields this repository stores as data.
- [What a self-hosted Grok Bot would have to be](https://grokbotalternatives.com/self-hosted-grok-bot) — why the hosted product has no install, and what the open-source options install.
- [Grok Bot vs Kortix, field by field](https://grokbotalternatives.com/grok-bot-vs-kortix) — the per-user shared machine against one machine per session.
- [Grok Bot's security controls, and which plan unlocks them](https://grokbotalternatives.com/grok-bot-security) — the enterprise-only list, quoted from xAI's docs.
