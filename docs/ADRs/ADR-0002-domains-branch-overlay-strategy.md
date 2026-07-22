# ADR-0002 — Use `domains/*` long-lived branches as private deployment overlays

Date: 2026-07-22
Status: Proposed

## Context

The project needs a durable place to store deployment-specific infrastructure as
code without contaminating `main`. The requirement is not temporary: multiple AI
agents and humans may collaborate asynchronously through repository contents,
issue trackers, and other planning artifacts, so the branch topology must make
private deployment intent obvious and safe.

## Decision

Adopt sentinel-prefixed long-lived branches for private domain overlays.

Recommended structure:

```text
main
platform/vercel-compat
domains/<apex-domain>
domains/<apex-domain>/<environment>
```

Examples:

```text
domains/geomesh.net
domains/geomesh.net/staging
```

Rules:

1. `main` stays upstream-clean per ADR-0001.
2. `domains/*` branches are one-way overlays rebased or fast-forwarded from
   `main`; they are not merged back into `main`.
3. Real domain values, zone values, and hosting bindings may exist only on the
   corresponding `domains/*` branch.
4. Automation reads the target domain from the branch name before applying any
   provider-specific changes.
5. Human and agent operators use issue drafts and ADR/PRD artifacts as the
   shared stigmergic surface for refinement.

## Why this over alternatives

### Better than hardcoding on `main`

Hardcoding private values on `main` defeats upstream cleanliness immediately.

### Better than a purely local `.env` file

A local-only file is not sufficiently auditable for multi-agent collaboration.
The branch itself must communicate deployment intent.

### Better than a separate repository right now

A separate infrastructure repository could be cleaner later, but it adds
operational fragmentation before the first reference deployment exists.

## Consequences

### Positive

- Domain-specific deployment work is isolated and reviewable.
- More than one future domain can be supported without rewriting `main`.
- The branch name itself documents the deployment target.

### Risks to manage

- Overlay branches can drift behind `main`.
- Rebase conflicts may occur if provider templates evolve frequently.
- Multi-writer races still need workflow-level concurrency protection.

## Follow-on work

- Add CI workflows for pushes to `domains/*`.
- Keep issue drafts in `.github/Issues/` so agents can promote them into live
  GitHub Issues consistently.
- Add branch protection and concurrency rules before live apply steps.
