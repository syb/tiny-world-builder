Title: docs: formalise upstream-clean main and domains/* overlay rules in ADRs and PRDs
Labels: documentation, architecture
Assignees:
---
## Problem

The deployment-branch strategy and upstream-cleanliness constraints need durable
written artifacts so multiple humans and AI agents can collaborate through repo
contents over time.

## Proposal

Add:

- ADRs covering upstream-clean `main`, `domains/*` overlays, and deployment
  guards
- A PRD for the first reference deployment milestone
- A glossary for GFSM, PromptVer-TDD, SNEng, stigmergy, and related terms
- File-per-issue drafts under `.github/Issues/`

## Acceptance criteria

- New collaborators can understand the deployment collaboration model by reading
  repo docs.
- The repo contains stable documentation-as-code artifacts for this work.
