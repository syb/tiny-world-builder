# ADR-0003 — Reference deployments require guarded automation and explicit preflight checks

Date: 2026-07-22
Status: Proposed

## Context

The first public reference deployment should prove that the fork can deploy from
Git to a real hostname on Vercel, with Cloudflare DNS supplying the delegation.
The current guidance and prototypes are directionally good, but live DNS and TLS
operations are unforgiving when a script is slightly wrong or when multiple
agents can write concurrently.

## Decision

The reference deployment must be executed through a guarded workflow with these
minimum checks:

1. Fix any known correctness bugs in the applicator before `--apply`.
2. Verify the Vercel project identity before binding a custom domain.
3. Enforce a single-writer path using workflow concurrency or an equivalent
   lock.
4. Validate DNS propagation before calling certificate issuance complete.
5. Treat wildcard preview domains as a separate milestone from the first apex or
   canonical environment hostname.

## Professional pushback on the candidate guidance

### Agreement

- A grey-cloud CNAME with Vercel-managed certificates is the correct baseline.
- Binding the canonical environment hostname first is the right milestone.
- Deferring Cloudflare Access is acceptable for the first public visibility
  milestone.

### Solutions Negation Engineering (what not to do)

- Do not run a live apply while known script bugs remain unresolved.
- Do not assume wildcard DNS is useful before Vercel is configured to recognise
  the same hostnames.
- Do not rely on a documentation-only single-writer rule when multiple agents
  hold credentials.
- Do not declare success based only on record creation; certificate issuance and
  HTTP reachability must also be checked.

### Critique of the Grok recommendation

Grok is broadly right that a second long-lived branch is the correct design, but
its answer is incomplete in four important ways:

1. It names the branch topology but does not define the operating rules clearly
   enough: one-way overlay, never merged back into `main`, and driven by CI.
2. It correctly identifies private identifiers as non-upstreamable, but it does
   not stress that examples and docs on `main` must also avoid fork-owned
   domains.
3. It does not call out the need for concurrency controls when more than one AI
   system can write to Cloudflare or Vercel.
4. It does not separate the first canonical deployment milestone from the later
   wildcard preview automation milestone.

### Enhancements

- Add branch-derived deployment automation for `domains/*` pushes.
- Add issue drafts and ADRs as the shared planning surface for multi-agent
  stigmergy.
- Add a DNS propagation gate and an HTTP/TLS verification gate after binding.
- Treat Cloudflare Access, wildcard previews, and any second host such as
  Cloudflare Pages as follow-on milestones.

## Consequences

This decision slightly slows the first deployment, but it materially lowers the
risk of writing incorrect records, binding the wrong project, or publishing a
false-positive success report.
