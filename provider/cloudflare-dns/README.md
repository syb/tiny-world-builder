# Cloudflare DNS IaC — domain-agnostic template

Companion to ADR-0001 / ADR-0002 and the DNS Naming Convention Decision Record (Bezos Type-2).

## Purpose

Declarative, secret-free infrastructure-as-code for an environment-first
naming pattern. Real domain values are **never** committed on `main`; they
are supplied at apply time via environment variables or from a `domains/*`
overlay branch.

| Branch / environment | Example URL (illustrative only) |
|----------------------|---------------------------------|
| `main` | `https://example.dev.your-zone.example` |
| any other branch | `https://<sanitised-branch>.example.dev.your-zone.example` |

## Contents

| File | Role |
|------|------|
| `records.yaml` | Declarative manifest (no secrets, placeholder defaults) |
| `apply.py` | Preferred applicator — env-var driven, dry-run by default, idempotent |
| `apply.sh` | Thin wrapper / historical reference |
| `README.md` | This file |

## Required environment variables

```bash
export CLOUDFLARE_API_TOKEN=...
export CLOUDFLARE_ZONE_ID=...          # from your Cloudflare zone
export VERCEL_TOKEN=...
export VERCEL_PROJECT_ID=...           # target Vercel project
```

Optional overrides (defaults are pure placeholders):

```bash
DOMAIN_LABEL=example.dev
WILDCARD_LABEL=*.example.dev
VERCEL_CNAME_TARGET=cname.vercel-dns.com
FULL_DOMAIN=example.dev.your-zone.example
GIT_BRANCH=main
```

## Usage

```bash
# Dry-run (default)
python3 apply.py

# Apply for real (only after single-writer confirmation)
python3 apply.py --apply
```

## Single-writer rule

Multiple agents may hold live Cloudflare credentials. Only **one** agent may
apply this manifest at a time. Always list existing records matching
DOMAIN_LABEL / WILDCARD_LABEL before writing. Prefer the GitHub Actions
workflow (issue #3) which enforces concurrency by domain.

## SSL / Certificate limitations (important)

Cloudflare Free Universal SSL covers only the zone apex and a single-level
wildcard (`*.your-zone.example`). Multi-level names require either:

1. Keep CNAMEs `proxied: false` (grey-cloud) and let Vercel issue certificates, or
2. Cloudflare Advanced Certificate Manager + DNS-01, or
3. Move nameservers to Vercel.

**Recommended for the first milestone:** grey-cloud + Vercel-managed certs.

## Status

Template only. No live records are created by commits on `main`. Real values
and apply runs happen exclusively from `domains/*` overlay branches under the
single-writer rule.
