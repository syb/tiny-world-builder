---
name: tinyworld-domain-overlay-deployments
description: Use when changing domain-specific deployment overlays, `domains/*` branch rules, provider DNS templates, or issue/ADR/PRD artifacts that keep `main` upstream-clean.
---

# TinyWorld Domain Overlay Deployments

- `main` is the upstream-compatible surface and must not contain fork-owned
  domains, account-specific provider IDs, or private policy names.
- Private deployment state belongs on `domains/*` long-lived overlay branches,
  not on `main`.
- The branch naming convention is operational: automation should derive the
  target domain from the branch name before applying provider changes.
- Multi-agent deployment work must enforce a single-writer path with workflow
  concurrency or an equivalent lock; documentation-only warnings are not
  sufficient.
- `.github/Issues/` is the repo's file-per-issue draft surface for promoting
  planned work into live GitHub Issues with `gh issue create`.
- `docs/ADRs/`, `docs/PRDs/`, and `docs/GLOSSARY.md` are the durable
  documentation-as-code surfaces for this deployment/collaboration pattern.
