"""Resolve a real, working link for every platform we quote a price for.

OpenRouter publishes policy URLs but no homepage, so the homepage is derived from
the policy URL's domain and then actually fetched to prove it resolves. Anything
that fails falls back to the provider's OpenRouter page, which always exists.

Results are cached in data/current/providers.csv and only new platforms are
checked. Re-verifying every run would mean a provider having a bad afternoon
silently flips its link, which is exactly the kind of churn this repo avoids.
"""
import csv, json, os, sys, urllib.parse
import concurrent.futures as cf
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw", "openrouter", "providers.json")
OUT = os.path.join(ROOT, "data", "current", "providers.csv")
FIELDS = ["platform", "slug", "url", "url_kind", "status_page", "headquarters"]
UA = {"User-Agent": "Mozilla/5.0 (compatible; llm-price-index/0.1; +https://github.com/tokencanopy/price)"}

# Policy pages often live on an app or docs host; the marketing site is the parent.
APP_SUBDOMAINS = {"chat", "api", "docs", "platform", "console", "dashboard",
                  "help", "support", "status", "app", "cloud", "developer", "developers"}

# Sources that are not OpenRouter providers and so have no slug to fall back to.
STATIC = {
    "AWS Bedrock":   ("https://aws.amazon.com/bedrock/pricing/", "own", "https://health.aws.amazon.com/health/status", "US"),
    "Azure Foundry": ("https://azure.microsoft.com/en-us/pricing/details/ai-foundry/", "own", "https://azure.status.microsoft/en-us/status", "US"),
}


def candidates(p):
    """Homepage guesses for one provider, best first."""
    seen, out = set(), []
    for key in ("privacy_policy_url", "terms_of_service_url", "status_page_url"):
        u = p.get(key)
        if not u:
            continue
        s = urllib.parse.urlsplit(u)
        if not (s.scheme and s.netloc):
            continue
        host = s.netloc
        labels = host.split(".")
        if labels[0] in APP_SUBDOMAINS and len(labels) > 2:
            parent = ".".join(labels[1:])
            for h in (parent, f"www.{parent}"):
                if h not in seen:
                    seen.add(h)
                    out.append(f"{s.scheme}://{h}/")
        if host not in seen and not host.startswith("status."):
            seen.add(host)
            out.append(f"{s.scheme}://{host}/")
    return out


def first_live(urls):
    for u in urls:
        try:
            r = requests.get(u, timeout=10, allow_redirects=True, headers=UA)
            if r.status_code < 400:
                return u
        except requests.RequestException:
            continue
    return None


def main():
    with open(RAW) as f:
        data = json.load(f)
    providers = data.get("data", data)

    cache = {}
    if os.path.exists(OUT):
        with open(OUT) as f:
            for r in csv.DictReader(f):
                if r.get("url"):
                    cache[r["platform"]] = r

    todo = [p for p in providers if p["name"] not in cache]
    print(f"{len(cache)} cached, resolving {len(todo)} new platform(s)")

    resolved = {}
    if todo:
        with cf.ThreadPoolExecutor(12) as ex:
            for p, url in zip(todo, ex.map(lambda q: first_live(candidates(q)), todo)):
                resolved[p["name"]] = url

    rows = []
    for p in providers:
        name = p["name"]
        if name in cache:
            rows.append({k: cache[name].get(k, "") for k in FIELDS})
            continue
        url = resolved.get(name)
        rows.append({
            "platform": name, "slug": p.get("slug", ""),
            "url": url or f"https://openrouter.ai/provider/{p.get('slug','')}",
            "url_kind": "own" if url else "openrouter",
            "status_page": p.get("status_page_url") or "",
            "headquarters": p.get("headquarters") or "",
        })
    for name, (url, kind, status, hq) in STATIC.items():
        if name in cache:
            rows.append({k: cache[name].get(k, "") for k in FIELDS})
        else:
            rows.append({"platform": name, "slug": "", "url": url,
                         "url_kind": kind, "status_page": status, "headquarters": hq})

    rows.sort(key=lambda r: r["platform"].lower())
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, FIELDS)
        w.writeheader()
        w.writerows(rows)
    own = sum(1 for r in rows if r["url_kind"] == "own")
    print(f"wrote {len(rows)} platforms: {own} link to their own site, "
          f"{len(rows)-own} fall back to their OpenRouter page")


if __name__ == "__main__":
    main()
