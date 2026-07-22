#!/usr/bin/env bash
# provider/cloudflare-dns — apply.sh (reference / thin wrapper)
# CalVer: 2026-07-22  SemVer: 1.0.0
# Prefer apply.py for new work. This script is kept for compatibility.

set -euo pipefail

: "${CLOUDFLARE_API_TOKEN:?Set CLOUDFLARE_API_TOKEN before running}"
: "${CLOUDFLARE_ZONE_ID:?Set CLOUDFLARE_ZONE_ID before running}"
: "${VERCEL_TOKEN:?Set VERCEL_TOKEN before running}"
: "${VERCEL_PROJECT_ID:?Set VERCEL_PROJECT_ID before running}"

echo "This will create/update live DNS records on geomesh.net and bind a"
echo "Vercel custom domain. Confirm no other agent is applying concurrently."
read -r -p "Type 'apply' to continue: " CONFIRM
[ "$CONFIRM" = "apply" ] || { echo "Aborted."; exit 1; }

# Delegate to the Python implementation when available
if command -v python3 >/dev/null && [[ -f "$(dirname "$0")/apply.py" ]]; then
  exec python3 "$(dirname "$0")/apply.py" --apply
fi

echo "Python apply.py not found — falling back to pure bash (limited)."
# ... original curl logic can remain here if needed
echo "Please use apply.py"
exit 1
