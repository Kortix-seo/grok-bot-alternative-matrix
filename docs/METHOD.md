# Method

## What this repository is

A comparison of the products that come up when someone searches for a Grok Bot alternative, kept as a JSON file with a source URL and a read date on every value, plus a script that re-checks what a public API can check.

It is not a ranking. Rows are ordered with the product these rows are measured against first, then the rest alphabetically by licence family; nothing in the order is a verdict on quality.

## Column by column

| Column | What it records | How it is verified |
|---|---|---|
| `product`, `vendor` | the name the vendor sells and the organisation behind it | the vendor's own page or the repository owner |
| `isolation_unit` | what one agent, bot or session gets to itself: a machine, a container, a process, a shared machine | the vendor's product or docs page, quoted in `sources` |
| `hosting` | where that machine actually runs | the vendor's product or docs page. Where a product page names no host, the docs page that does is the source |
| `self_hosted` | whether a deployment a customer installs exists today | the vendor's docs. An open-source repository is not by itself a self-hosted deployment |
| `review_gate` | what stands between an agent's change and production | the vendor's docs on approvals, reviews or change management |
| `licence` | the repository's licence | GitHub's licence API for the repository named in the row |
| `price_shape` | how the vendor charges | the vendor's pricing page, or "no published price" when there is none |

Every row's `sources` array carries the URL, the date it was read, and the sentence the value came from.

## What `scripts/refresh.py` checks, and what it refuses to

It re-reads three machine-readable things from GitHub: the `license.spdx_id` of each product's repository, whether that repository is `archived`, and `pushed_at`. It reports a licence change, an archived repository and a push after the row's read date, because each of those can invalidate a row.

It never rewrites `isolation_unit`, `hosting`, `self_hosted`, `review_gate` or `price_shape`. Those are claims about a product page, and a script that guessed them would be inventing evidence. A row those fields touch needs a human to open the source URL again.

## What this matrix does not compare

- **Benchmarks and model quality.** Nothing here measures how well an agent does a task; the products below run different models on different budgets.
- **Popularity.** Star counts, fork counts and download counts are left out on purpose: they measure attention, not whether a team can review an agent's work.
- **Feature lists.** A feature grid changes monthly and reads the same on every product page. The four fields above are the ones that change what a reviewer can answer.

## Corrections

Open a pull request that changes a row's value and, in the same commit, its `sources` entry: the URL, the date you read it and the sentence you read. A row without a source is not a fact, and a change without one will be closed.

## Attribution

The Kortix row describes Kortix, the open-source CompanyOS: agents, skills and memory as files in a git repository a team owns, with one isolated machine per session and session work landing through a change request. Its claims are the ones Kortix publishes on https://kortix.com/security and https://kortix.com/pricing, quoted in the row's `sources` and dated like every other row.

This repository is published by Kortix's SEO team and is not an independent review.
