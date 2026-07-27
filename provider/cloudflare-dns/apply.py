#!/usr/bin/env python3
"""provider/cloudflare-dns/apply.py
CalVer: 2026-07-23  SemVer: 1.2.0

Idempotent, env-var-driven applicator for domain-agnostic DNS + Vercel binding.
Dry-run by default. Requires explicit --apply.

Required env:
  CLOUDFLARE_API_TOKEN
  CLOUDFLARE_ZONE_ID
  VERCEL_TOKEN
  VERCEL_PROJECT_ID

Optional env (defaults are placeholders only — override for real use):
  DOMAIN_LABEL=example.dev
  WILDCARD_LABEL=*.example.dev
  VERCEL_CNAME_TARGET=cname.vercel-dns.com
  FULL_DOMAIN=example.dev.your-zone.example
  GIT_BRANCH=main
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any


def env(name: str, default: str | None = None, required: bool = False) -> str:
    val = os.environ.get(name, default)
    if required and not val:
        sys.exit(f"ERROR: Missing required environment variable: {name}")
    return val or ""


def http_json(method: str, url: str, token: str, body: dict | None = None) -> dict[str, Any]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "domain-overlay-dns-apply/1.2",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        sys.exit(f"HTTP {e.code} on {method} {url}\n{err_body}")


def cf_list_records(zone_id: str, token: str, name: str) -> list[dict]:
    """List DNS records whose name matches exactly (supports wildcards)."""
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?name={name}&per_page=50"
    result = http_json("GET", url, token)
    if not result.get("success"):
        sys.exit(f"Cloudflare list failed: {result}")
    return result.get("result") or []


def cf_create_cname(zone_id: str, token: str, name: str, content: str, comment: str) -> dict:
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    body = {
        "type": "CNAME",
        "name": name,
        "content": content,
        "proxied": False,
        "ttl": 300,
        "comment": comment,
    }
    return http_json("POST", url, token, body)


def vercel_add_domain(project_id: str, token: str, domain: str, git_branch: str) -> dict:
    url = f"https://api.vercel.com/v10/projects/{project_id}/domains"
    body = {"name": domain, "gitBranch": git_branch}
    return http_json("POST", url, token, body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply Cloudflare DNS + Vercel domain binding (domain-agnostic)")
    parser.add_argument("--apply", action="store_true", help="Actually perform writes (default is dry-run)")
    args = parser.parse_args()
    dry_run = not args.apply

    cf_token = env("CLOUDFLARE_API_TOKEN", required=True)
    zone_id = env("CLOUDFLARE_ZONE_ID", required=True)
    vercel_token = env("VERCEL_TOKEN", required=True)
    vercel_project = env("VERCEL_PROJECT_ID", required=True)

    # Placeholders only — real values supplied via env or domains/* overlay
    domain_label = env("DOMAIN_LABEL", "example.dev")
    wildcard_label = env("WILDCARD_LABEL", "*.example.dev")
    cname_target = env("VERCEL_CNAME_TARGET", "cname.vercel-dns.com")
    full_domain = env("FULL_DOMAIN", "example.dev.your-zone.example")
    git_branch = env("GIT_BRANCH", "main")

    print("=== Cloudflare DNS + Vercel Domain Binding (domain-agnostic) ===")
    print(f"Mode          : {'DRY-RUN (no changes)' if dry_run else 'APPLY'}")
    print(f"Zone ID       : {zone_id}")
    print(f"CNAME target  : {cname_target}")
    print(f"Records       : {domain_label} , {wildcard_label}")
    print(f"Vercel domain : {full_domain}  (gitBranch={git_branch})")
    print()
    print("SINGLE-WRITER RULE: Confirm no other agent (Claude/Grok/human) is")
    print("applying this same manifest concurrently.")
    print()

    if dry_run:
        print("[DRY-RUN] Exiting without changes. Re-run with --apply to execute.")
        return

    # --- Cloudflare CNAMEs ---
    # Use the label exactly as supplied. Cloudflare accepts both relative
    # names and FQDNs; wildcards are stored with the leading *.
    for label, comment in [
        (domain_label, "Apex / canonical environment hostname"),
        (wildcard_label, "Wildcard for future branch previews"),
    ]:
        existing = cf_list_records(zone_id, cf_token, label)
        if existing:
            print(f"EXISTS  {label} → already present, skipping create")
        else:
            print(f"CREATE  {label} → {cname_target}")
            res = cf_create_cname(zone_id, cf_token, label, cname_target, comment)
            if not res.get("success"):
                sys.exit(f"Failed to create {label}: {res}")
            print(f"         created id={res['result']['id']}")

    # --- Vercel domain binding ---
    print(f"BIND    {full_domain} → project {vercel_project} (branch={git_branch})")
    try:
        vres = vercel_add_domain(vercel_project, vercel_token, full_domain, git_branch)
        print(f"         Vercel response: {json.dumps(vres)[:200]}...")
    except SystemExit as e:
        # Domain may already exist — treat as success for idempotency
        if "already" in str(e).lower() or "409" in str(e):
            print("         (domain already bound — ok)")
        else:
            raise

    print()
    print("Done. Cloudflare Access (Google / OTP) remains a separate manual step.")
    print("Note: multi-level wildcard SSL is limited — see README.md")


if __name__ == "__main__":
    main()
