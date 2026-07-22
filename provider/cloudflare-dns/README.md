# Cloudflare DNS IaC — tinyverse.dev.geomesh.net

Companion to the DNS Naming Convention Decision Record (Bezos Type-2).

## Purpose

Declarative, secret-free infrastructure-as-code for the environment-first
naming pattern:

| Branch / environment | URL |
|----------------------|-----|
| `main` | `https://tinyverse.dev.geomesh.net` |
| any other branch | `https://<sanitised-branch>.tinyverse.dev.geomesh.net` |

## Contents

| File | Role |
|------|------|
| `records.yaml` | Declarative manifest (no secrets) |
| `apply.py` | Preferred applicator — env-var driven, dry-run by default, idempotent |
| `apply.sh` | Thin wrapper / historical reference |
| `README.md` | This file |

## Required environment variables

```bash
export CLOUDFLARE_API_TOKEN=...
export CLOUDFLARE_ZONE_ID=737ef273e937a29b8baf60633359cb11   # geomesh.net
export VERCEL_TOKEN=...
export VERCEL_PROJECT_ID=...   # tiny-world-builder_upstream_main
```

Optional overrides (defaults shown):

```bash
DOMAIN_LABEL=tinyverse.dev
WILDCARD_LABEL=*.tinyverse.dev
VERCEL_CNAME_TARGET=cname.vercel-dns.com
FULL_DOMAIN=tinyverse.dev.geomesh.net
GIT_BRANCH=main
```

## Usage

```bash
# Dry-run (default)
python3 apply.py

# Apply for real
python3 apply.py --apply
```

## Single-writer rule

Both Claude and Grok currently hold live Cloudflare credentials on this
account. Only **one** agent may apply this manifest at a time. Always list
existing `tinyverse.dev*` records before writing.

## SSL / Certificate limitations (important)

Cloudflare Free Universal SSL covers only:
- `geomesh.net`
- `*.geomesh.net`

It does **not** cover:
- `tinyverse.dev.geomesh.net` (two labels deep)
- `*.tinyverse.dev.geomesh.net` (three labels deep)

**Practical strategy:**
1. Keep all CNAMEs `proxied: false` (grey-cloud).
2. Let Vercel issue the certificates (works for the apex after the domain is
   added in the Vercel project).
3. Branch previews can continue to use native `*.vercel.app` URLs until a
   more advanced setup (Cloudflare Advanced Certificate Manager or Vercel
   nameservers + DNS-01) is justified.

True automatic multi-level wildcards require either:
- Moving the zone nameservers to Vercel, or
- Cloudflare Advanced Certificate Manager + manual/automatic DNS-01 challenges.

## Status

Template only as of 2026-07-22. No live records have been created by this
commit. Apply deliberately after human review.
