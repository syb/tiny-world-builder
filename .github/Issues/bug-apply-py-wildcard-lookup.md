Title: bug: fix wildcard lookup and duplicate record query in provider/cloudflare-dns/apply.py
Labels: bug, infra, blocker
Assignees:
---
## Problem

`provider/cloudflare-dns/apply.py` has a wildcard lookup bug and a duplicate
record-query assignment.

## Details

- `label.lstrip('*')` leaves a leading `.` for wildcard labels such as
  `*.tinyverse.dev`, which can produce an invalid lookup name.
- The script assigns `existing = cf_list_records(...)` twice in sequence, making
  the first result dead code.

## Why it matters

This blocks confidence in any live `--apply` step and can lead to duplicate or
mis-targeted record-creation attempts.

## Acceptance criteria

- Wildcard labels use a correct prefix removal strategy.
- The duplicate dead assignment is removed.
- Dry-run and apply paths are both reviewed after the fix.
