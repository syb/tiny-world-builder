Title: infra: implement domains/* sentinel-prefix branch overlays for private deployment state
Labels: enhancement, infra, architecture, ci-cd
Assignees:
---
## Problem

The project needs private deployment automation and domain-specific
configuration, but `main` must remain upstream-clean.

## Proposal

Adopt `domains/*` long-lived branches as private overlays.

Examples:

- `domains/geomesh.net`
- `domains/geomesh.net/staging`

## Rules

1. `main` stays domain-agnostic.
2. `domains/*` branches are rebased or fast-forwarded from `main`.
3. `domains/*` branches are not merged back into `main`.
4. CI derives the target domain from the branch name.

## Acceptance criteria

- A documented overlay strategy exists in `docs/ADRs/`.
- Future deploy workflows can target `domains/*` branches directly.
- Private infrastructure state is isolated from the upstreamable surface.
