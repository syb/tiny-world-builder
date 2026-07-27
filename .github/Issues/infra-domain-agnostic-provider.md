Title: infra: make provider/cloudflare-dns fully domain-agnostic for upstream mergeability
Labels: enhancement, infra, upstream-compat
Assignees:
---
## Problem

`provider/cloudflare-dns/records.yaml`, `README.md`, and `apply.py` currently
contain fork-owned domain examples and assumptions. That blocks the fork's
`main` branch from staying cleanly mergeable into upstream.

## Desired outcome

Make the provider templates fully parameterised so `main` contains no literal
fork-owned domain values.

## Scope

- Replace concrete domain literals in `provider/cloudflare-dns/` with
  placeholders or environment-variable-driven values.
- Document how real values are supplied from `domains/*` overlay branches.
- Preserve dry-run validation behavior.

## Acceptance criteria

- `grep -r 'geomesh\.net' /home/runner/work/tiny-world-builder/tiny-world-builder/provider`
  returns no matches on `main`.
- `provider/cloudflare-dns/` still documents the deployment intent clearly.
- `main` remains suitable for upstream contribution.
