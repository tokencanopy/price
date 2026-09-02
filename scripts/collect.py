"""Fetch raw pricing from public, unauthenticated sources into data/raw/.

Every collector writes the provider's payload verbatim. Normalization happens
later, so a parsing mistake can always be re-run against the archived original.
"""
import json, os, re, sys, time, urllib.parse
from datetime import datetime, timezone
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
UA = {"User-Agent": "llm-price-index/0.1 (+https://github.com/llm-price-index)"}
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get(url, timeout=30, tries=3):
    for attempt in range(tries):
        try:
            r = requests.get(url, headers=UA, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if attempt == tries - 1:
                print(f"    FAIL {url}: {e}", file=sys.stderr)
                return None
            time.sleep(2 * (attempt + 1))


# Rolling-window telemetry (uptime_last_30m, latency_last_30m, ...). It moves
# every minute and has nothing to do with price, so archiving it would add
# thousands of meaningless diff lines to every single run.
VOLATILE = re.compile(r"_last_\d+[a-z]$")


def stabilize(obj):
    """Sort every list we archive by a stable key.

    Providers return list order that varies run to run. Left alone, git would
    see a rewritten file every day and the repo would balloon; sorted, the daily
    delta is just the lines whose prices actually moved.
    """
    if isinstance(obj, dict):
        return {k: stabilize(v) for k, v in obj.items() if not VOLATILE.search(k)}
    if isinstance(obj, list):
        items = [stabilize(v) for v in obj]
        def key(v):
            if isinstance(v, dict):
                for k in ("meterId", "id", "slug", "sku", "provider_name", "name", "model_name"):
                    if isinstance(v.get(k), str):
                        return (0, v[k])
                return (1, json.dumps(v, sort_keys=True)[:200])
            return (2, str(v))
        try:
            return sorted(items, key=key)
        except TypeError:
            return items
    return obj


def write(relpath, obj):
    path = os.path.join(RAW, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(stabilize(obj), f, indent=1, sort_keys=True)
    return path


def collect_openrouter():
    """Models list + per-provider endpoints. Endpoints is the valuable part:
    it is the only public source for the same model priced across platforms."""
    print("[openrouter] models + providers")
    models = get("https://openrouter.ai/api/v1/models")
    providers = get("https://openrouter.ai/api/v1/providers")
    if not models:
        return 0
    write("openrouter/models.json", models)
    if providers:
        write("openrouter/providers.json", providers)

    # ':free' / ':batch' suffixed ids are variants of a base model; the base
    # model's endpoint list already covers them.
    targets = [m["id"] for m in models["data"] if ":" not in m["id"]]
    print(f"[openrouter] fetching endpoints for {len(targets)} models")
    out, ok = {}, 0
    for i, slug in enumerate(targets, 1):
        data = get(f"https://openrouter.ai/api/v1/models/{slug}/endpoints", timeout=20, tries=2)
        if data:
            out[slug] = data.get("data", {})
            ok += 1
        if i % 50 == 0:
            print(f"    {i}/{len(targets)}")
        time.sleep(0.25)          # be a polite guest
    write("openrouter/endpoints.json", {"models": out})
    print(f"[openrouter] {ok}/{len(targets)} endpoint sets")
    return ok


def collect_aws():
    """AWS Price List API: public, no auth, and carries batch/priority tiers
    plus per-region pricing that OpenRouter does not expose."""
    print("[aws] bedrock price list")
    idx = get("https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonBedrock/current/region_index.json")
    if not idx:
        return 0
    write("aws/region_index.json", idx)
    # Start with the regions that carry the full model catalogue. More regions
    # are mostly duplicate SKUs at identical prices.
    regions = [r for r in ("us-east-1", "us-west-2", "eu-west-1") if r in idx.get("regions", {})]
    n = 0
    for region in regions:
        url = "https://pricing.us-east-1.amazonaws.com" + idx["regions"][region]["currentVersionUrl"]
        data = get(url, timeout=90)
        if data:
            write(f"aws/{region}.json", data)
            n += len(data.get("products", {}))
            print(f"    {region}: {len(data.get('products', {}))} products")
    return n


def collect_azure():
    """Azure Retail Prices API: public OData, paged 100 at a time."""
    print("[azure] retail prices (AI + Machine Learning)")
    flt = urllib.parse.quote("serviceFamily eq 'AI + Machine Learning'")
    url = f"https://prices.azure.com/api/retail/prices?$filter={flt}"
    items, pages = [], 0
    while url and pages < 60:                    # ~6k meters is plenty
        page = get(url)
        if not page:
            break
        items.extend(page.get("Items", []))
        url = page.get("NextPageLink")
        pages += 1
    if items:
        write("azure/retail_prices.json", {"items": items})
    print(f"    {len(items)} meters over {pages} pages")
    return len(items)


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    jobs = {"openrouter": collect_openrouter, "aws": collect_aws, "azure": collect_azure}
    for name, fn in jobs.items():
        if only and only != name:
            continue
        try:
            fn()
        except Exception as e:
            print(f"[{name}] ERROR {e}", file=sys.stderr)
    print("done", NOW)
