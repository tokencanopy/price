"""Turn raw provider payloads into one long-format table, then record changes.

Two outputs:
  data/current/prices.csv        - today's normalized snapshot (overwritten)
  data/history/price_changes.csv - append-only; one row only when a price moves

The change log is the actual dataset. Prices move rarely, so appending only on
change keeps the repo small while still reconstructing a full step-function
series for any key.
"""
import csv, json, os, re
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
CURRENT = os.path.join(ROOT, "data", "current", "prices.csv")
META = os.path.join(ROOT, "data", "current", "meta.json")
HISTORY = os.path.join(ROOT, "data", "history", "price_changes.csv")
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FIELDS = ["source", "platform", "model_key", "model_name", "author",
          "open_weight", "variant", "region", "metric", "usd_per_1m",
          "context_length", "effective_date"]
# Identity of a price series. Everything else is descriptive.
KEY = ["source", "platform", "model_key", "variant", "region", "metric"]

OR_METRICS = {"prompt": "input", "completion": "output",
              "input_cache_read": "cache_read", "input_cache_write": "cache_write"}


def load(rel):
    path = os.path.join(RAW, rel)
    if not os.path.exists(path):
        print(f"  (skip, missing {rel})")
        return None
    with open(path) as f:
        return json.load(f)


def rows_openrouter():
    models = load("openrouter/models.json")
    eps = load("openrouter/endpoints.json")
    if not models or not eps:
        return []
    meta = {m["id"]: m for m in models["data"]}
    out = []
    for slug, data in eps["models"].items():
        m = meta.get(slug, {})
        hf = m.get("hugging_face_id")
        for ep in data.get("endpoints", []):
            pricing = ep.get("pricing") or {}
            quant = ep.get("quantization") or "unknown"
            for raw_metric, metric in OR_METRICS.items():
                val = pricing.get(raw_metric)
                if val in (None, "", "0", "-1"):
                    continue
                try:
                    usd = float(val) * 1_000_000      # OR quotes USD per token
                except ValueError:
                    continue
                if usd <= 0:
                    continue
                out.append({
                    "source": "openrouter",
                    "platform": ep.get("provider_name") or "unknown",
                    # hugging_face_id is a stable cross-platform join key for
                    # open-weight models; closed models fall back to the slug.
                    "model_key": (hf or slug).lower(),
                    "model_name": m.get("name") or slug,
                    "author": slug.split("/")[0],
                    "open_weight": bool(hf), "variant": quant, "region": "",
                    "metric": metric, "usd_per_1m": round(usd, 6),
                    "context_length": ep.get("context_length") or "",
                    "effective_date": "",
                })
    return out


AWS_SKIP = re.compile(r"video|image|embed|rerank|guardrail|storage|training|per second", re.I)


def rows_aws():
    out = []
    for region in ("us-east-1", "us-west-2", "eu-west-1"):
        data = load(f"aws/{region}.json")
        if not data:
            continue
        terms = data.get("terms", {}).get("OnDemand", {})
        for sku, prod in data.get("products", {}).items():
            a = prod.get("attributes", {})
            itype = (a.get("inferenceType") or "")
            model = (a.get("model") or "").strip()
            if not itype or not model or AWS_SKIP.search(itype):
                continue          # a few SKUs carry no model attribute at all
            low = itype.lower()
            if "cache" in low:
                metric = "cache_read" if "read" in low else "cache_write"
            elif "input" in low:
                metric = "input"
            elif "output" in low:
                metric = "output"
            else:
                continue
            usage = (a.get("usagetype") or "").lower()
            variant = ("batch" if "batch" in low or "batch" in usage else
                       "priority" if "priority" in low or "priority" in usage else
                       "cross-region" if "cross-region" in usage else "standard")
            for term in terms.get(sku, {}).values():
                for dim in term.get("priceDimensions", {}).values():
                    unit = (dim.get("unit") or "").lower()
                    try:
                        price = float(dim["pricePerUnit"]["USD"])
                    except (KeyError, ValueError):
                        continue
                    if price <= 0:
                        continue
                    if "1k" in unit:
                        usd = price * 1000
                    elif "1m" in unit:
                        usd = price
                    else:
                        continue           # unknown unit: drop rather than guess
                    out.append({
                        "source": "aws", "platform": "AWS Bedrock",
                        "model_key": f"bedrock:{model.lower()}",
                        "model_name": model, "author": a.get("provider") or "",
                        "open_weight": "", "variant": variant, "region": region,
                        "metric": metric, "usd_per_1m": round(usd, 6),
                        "context_length": "",
                        "effective_date": (term.get("effectiveDate") or "")[:10],
                    })
    return out


def rows_azure():
    data = load("azure/retail_prices.json")
    if not data:
        return []
    out = []
    for it in data["items"]:
        if it.get("type") != "Consumption" or it.get("currencyCode") != "USD":
            continue
        if (it.get("unitOfMeasure") or "").strip() != "1M":
            continue                      # only per-1M-token meters
        meter = (it.get("meterName") or "").lower()
        # Azure meter names are heavily abbreviated ('5.4 opt Dz 1M Tokens').
        # Parse only the unambiguous ones; drop the rest rather than guess.
        if "token" not in meter:
            continue
        if re.search(r"\b(cach)", meter):
            metric = "cache_read"
        elif re.search(r"\b(inp|in)\b", meter):
            metric = "input"
        elif re.search(r"\b(opt|out)\b", meter):
            metric = "output"
        else:
            continue
        price = it.get("retailPrice")
        if not price or price <= 0:
            continue
        sku = (it.get("skuName") or "").strip()
        out.append({
            "source": "azure", "platform": "Azure Foundry",
            "model_key": f"azure:{(it.get('productName') or '').lower()}|{sku.lower()}",
            "model_name": it.get("productName") or "", "author": "",
            "open_weight": "", "variant": sku, "region": it.get("armRegionName") or "",
            "metric": metric, "usd_per_1m": round(float(price), 6),
            "context_length": "",
            "effective_date": (it.get("effectiveStartDate") or "")[:10],
        })
    return out


def dedupe(rows):
    """Same key can appear twice (e.g. a provider listing two tiers). Keep the
    cheapest so a series is deterministic."""
    best = {}
    for r in rows:
        k = tuple(str(r[c]) for c in KEY)
        if k not in best or r["usd_per_1m"] < best[k]["usd_per_1m"]:
            best[k] = r
    return best


def main():
    rows = []
    for name, fn in (("openrouter", rows_openrouter), ("aws", rows_aws), ("azure", rows_azure)):
        got = fn()
        print(f"[{name}] {len(got)} rows")
        rows += got
    best = dedupe(rows)
    print(f"total unique series: {len(best)}")

    prev = {}
    if os.path.exists(CURRENT):
        with open(CURRENT) as f:
            for r in csv.DictReader(f):
                prev[tuple(r[c] for c in KEY)] = r

    os.makedirs(os.path.dirname(CURRENT), exist_ok=True)
    with open(CURRENT, "w", newline="") as f:
        w = csv.DictWriter(f, FIELDS)
        w.writeheader()
        for k in sorted(best):
            w.writerow(best[k])

    changes = []
    for k, r in best.items():
        old = prev.get(k)
        old_val = float(old["usd_per_1m"]) if old else None
        new_val = float(r["usd_per_1m"])
        if old_val is not None and abs(old_val - new_val) < 1e-9:
            continue                       # unchanged: write nothing
        changes.append({
            "observed_at": NOW, **{c: r[c] for c in KEY},
            "model_name": r["model_name"],
            "old_usd_per_1m": "" if old_val is None else old_val,
            "new_usd_per_1m": new_val,
            "pct_change": "" if not old_val else round((new_val - old_val) / old_val * 100, 2),
        })
    for k, old in prev.items():
        if k not in best:
            changes.append({
                "observed_at": NOW, **{c: old[c] for c in KEY},
                "model_name": old.get("model_name", ""),
                "old_usd_per_1m": old["usd_per_1m"], "new_usd_per_1m": "",
                "pct_change": "", })   # delisted

    hfields = ["observed_at"] + KEY + ["model_name", "old_usd_per_1m", "new_usd_per_1m", "pct_change"]
    new_file = not os.path.exists(HISTORY)
    os.makedirs(os.path.dirname(HISTORY), exist_ok=True)
    with open(HISTORY, "a", newline="") as f:
        w = csv.DictWriter(f, hfields)
        if new_file:
            w.writeheader()
        for c in changes:
            w.writerow(c)
    with open(META, "w") as f:
        json.dump({"collected_at": NOW, "rows": len(best),
                   "platforms": len({r["platform"] for r in best.values()}),
                   "models": len({r["model_key"] for r in best.values()}),
                   "sources": sorted({r["source"] for r in best.values()})},
                  f, indent=1, sort_keys=True)

    firsts = sum(1 for c in changes if c["old_usd_per_1m"] == "")
    print(f"changes appended: {len(changes)} ({firsts} first observations, "
          f"{len(changes)-firsts} actual moves)")


if __name__ == "__main__":
    main()
