# GitHub Issue drafts

Each file in this directory is a draft intended to be promoted into a live
GitHub Issue with the official GitHub CLI.

## File format

Each issue draft starts with lightweight metadata:

```text
Title: <issue title>
Labels: label-one, label-two
Assignees:
---
<body markdown>
```

## Creating an issue with `gh`

```bash
FILE=.github/Issues/example.md
TITLE="$(sed -n '1s/^Title: //p' "$FILE")"
BODY_FILE="$(mktemp)"
tail -n +5 "$FILE" > "$BODY_FILE"
gh issue create --title "$TITLE" --body-file "$BODY_FILE"
```

If labels are wanted at creation time, read the second line manually or add them
with a follow-up `gh issue edit` command.

## Naming guidance

Use concise kebab-case file names grouped by concern, for example:

- `infra-*.md`
- `bug-*.md`
- `docs-*.md`
- `ci-*.md`
