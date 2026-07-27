# ADR-0001 — Keep `main` upstream-clean and domain-agnostic

Date: 2026-07-22
Status: Proposed

## Context

The fork `syb/tiny-world-builder` needs deployment automation for Sebastian
Malcolm's infrastructure, but the fork's `main` branch is also intended to stay
cleanly mergeable into the upstream `jasonkneen/tiny-world-builder` repository.
That creates a hard constraint: personally owned domains, account-specific
hostnames, zone identifiers, project identifiers, and access-policy names must
not live on `main`.

The current `provider/cloudflare-dns/` template set demonstrates the hosting
intent well, but any literal such as `geomesh.net` on `main` expands the diff
surface with infrastructure details that upstream cannot reasonably adopt.

## Decision

Treat `main` as the upstream-compatible surface.

`main` must not contain:

- Personal or fork-only domains
- Account-specific Cloudflare or Vercel identifiers
- Private infrastructure policy names
- Documentation that assumes the reader owns Sebastian Malcolm's
  infrastructure

Instead, `main` may contain only:

- Domain-agnostic templates
- Parameterised deployment workflows
- Placeholder examples such as `<your-zone>` and `<your-domain>`
- Architecture records describing how private overlays work outside `main`

## Consequences

### Positive

- Upstream PRs from `main` remain low-friction and easier to review.
- The fork can still carry private deployment logic without permanently forking
  the product codebase.
- Multi-agent collaboration becomes clearer because the boundary between
  upstreamable and private work is explicit.

### Negative

- Private deployment details must live elsewhere, which adds one more branch or
  overlay workflow to maintain.
- Examples in `main` documentation become slightly less concrete.

## Follow-on work

- Make `provider/cloudflare-dns/` fully domain-agnostic on `main`.
- Store real deployment values only in `domains/*` overlay branches.
- Add issue drafts and workflow documentation that make the overlay process
  auditable.
