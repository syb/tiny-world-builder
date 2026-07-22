Title: ci: add guarded deployment workflow for pushes to domains/* branches
Labels: enhancement, ci-cd, infra
Assignees:
---
## Problem

The single-writer rule is currently documentary. It should be enforced by the
workflow path that performs live deployment actions.

## Proposal

Add a GitHub Actions workflow triggered by pushes to `domains/*` branches that:

1. Extracts the target domain from the branch name.
2. Runs a dry-run preflight.
3. Waits for an approval gate if desired.
4. Applies DNS and domain-binding changes.
5. Verifies DNS propagation and HTTP/TLS reachability.
6. Uses workflow concurrency to prevent multi-writer races.

## Acceptance criteria

- The deployment path is auditable from Git history and workflow history.
- One domain cannot be applied concurrently by multiple actors.
- Post-deploy checks are part of the workflow result.
