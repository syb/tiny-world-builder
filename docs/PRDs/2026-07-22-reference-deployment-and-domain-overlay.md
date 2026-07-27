# PRD — Reference deployment and domain-overlay collaboration workflow

Date: 2026-07-22
Status: Proposed
Owner: Sebastian Malcolm (`SebHuman`)

## 1. Summary

Create a repeatable collaboration and deployment pattern that allows the fork to
publish a first public reference deployment while preserving an upstream-clean
`main` branch.

The initial visible milestone is a canonical environment hostname served by
Vercel and delegated by Cloudflare DNS. The broader product intent also includes
multi-agent collaboration, edutainment-focused future work, and a reusable
pattern for additional domains and environments.

## 2. Problem statement

The fork currently needs both of the following to be true at the same time:

1. `main` should remain a realistic candidate for upstream PRs.
2. Private deployment automation must still be documented and executable.

Without a clear overlay strategy, private hosting details leak into the shared
codebase and create friction for upstream contribution.

## 3. Goals

- Keep `main` free of fork-owned infrastructure identifiers.
- Establish a private overlay branch pattern for domain-specific deployment.
- Store collaboration intent as documentation-as-code in ADRs, PRDs, glossary
  entries, and issue drafts.
- Reach a first public deployment milestone for a canonical environment
  hostname.
- Support later multi-agent refinement through repository contents and GitHub
  Issues.

## 4. Non-goals

- Implement wildcard preview-domain automation in the first milestone.
- Implement Cloudflare Access policies in the first milestone.
- Redesign the whole product roadmap around this infrastructure work.
- Move infrastructure into a separate repository during the first milestone.

## 5. Users and collaborators

- Sebastian Malcolm as owner and decision-maker
- AI collaborators working through GitHub Copilot, Claude, Grok, and related
  agentic tooling
- Future upstream maintainers who need a clean `main` diff surface

## 6. Functional requirements

### FR1 — Upstream-clean main

`main` must contain only domain-agnostic provider templates and deployment docs.

### FR2 — Overlay branches

A `domains/*` branch pattern must hold real domain-specific deployment values and
be documented as a one-way overlay from `main`.

### FR3 — Shared stigmergic artifacts

The repository must contain:

- ADRs that explain the governing decisions
- A PRD that explains the milestone and scope
- A glossary of shared terms
- File-per-issue drafts in `.github/Issues/`

### FR4 — Issue promotion path

Issue draft files must be structured so an operator can promote them into real
GitHub Issues using `gh issue create` with a file body.

### FR5 — Guarded deployment

Reference deployment automation must include preflight checks, a single-writer
mechanism, and post-deploy verification.

## 7. Success criteria

- Contributors can explain where private deployment values may live and where
  they may not.
- The repository contains reusable documentation artifacts for future AI and
  human collaborators.
- A future implementation pass can automate `domains/*` pushes without revisiting
  the core architecture decisions.

## 8. Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Private domains leak onto `main` | Enforce ADR-0001 and review for literal values |
| Overlay branch drift | Rebase schedule and CI visibility |
| Multi-agent write race | Workflow concurrency and explicit single-writer lock |
| False deployment success | DNS propagation and HTTP/TLS verification gates |
| Wildcard preview confusion | Make wildcard previews a later milestone |

## 9. Incremental milestone sequence

1. Make provider templates domain-agnostic on `main`.
2. Create and document `domains/*` overlay branches.
3. Add deploy workflow drafts and issue drafts.
4. Fix applicator correctness bugs before any live apply.
5. Run the first canonical environment deployment.
6. Later: Access policies, wildcard previews, secondary hosts.

## 10. GFSM mapping

- `G_001+` Intent Distillation — restate the deployment problem clearly.
- `G_002+` Reasoning Structuring — use ADR, PRD, glossary, and issues as stable
  reasoning surfaces.
- `G_003+` Edge-Case Preemption — identify script bugs, race conditions, and
  wildcard limitations before live deployment.
- `G_004+` Contextual Grounding — keep the work anchored to Cloudflare, Vercel,
  and the repo's actual provider paths.
- `G_005+` Primitive Generation — turn the branch topology and issue drafts into
  reusable collaboration primitives.
- `G_006*` Self-Evolution — refine these artifacts as implementation evidence and
  adversarial reviews accumulate.

## 11. Open questions

- Should the long-term end state remain branch overlays, or eventually become a
  separate private infrastructure repository?
- Which exact hostname should be treated as the first public canonical
  deployment once the provider templates are domain-agnostic?
- Should branch promotion into GitHub Issues be manual, scripted, or workflow-
  triggered?
