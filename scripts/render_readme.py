"""Inject generated tables and stats into README.md between HTML markers."""
import csv, json, os
from collections import defaultdict
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRENT = os.path.join(ROOT, "data", "current", "prices.csv")
META = os.path.join(ROOT, "data", "current", "meta.json")
HISTORY = os.path.join(ROOT, "data", "history", "price_changes.csv")
README = os.path.join(ROOT, "README.md")


def read(path):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return list(csv.DictReader(f))


def block(name, body):
    return f"<!-- BEGIN {name} -->\n{body}\n<!-- END {name} -->"


def replace(text, name, body):
    start, end = f"<!-- BEGIN {name} -->", f"<!-- END {name} -->"
    i, j = text.find(start), text.find(end)
    if i == -1 or j == -1:
        return text
    return text[:i] + block(name, body) + text[j + len(end):]


def main():
    rows = read(CURRENT)
    hist = read(HISTORY)
    for r in rows:
        r["usd_per_1m"] = float(r["usd_per_1m"])

    platforms = {r["platform"] for r in rows}
    models = {r["model_key"] for r in rows}
    updated = datetime.now(timezone.utc).isoformat()
    if os.path.exists(META):
        with open(META) as f:
            updated = json.load(f).get("collected_at", updated)
    dates = sorted({h["observed_at"][:10] for h in hist})

    stats = (f"**{len(rows):,}** price points · **{len(models):,}** models · "
             f"**{len(platforms)}** platforms · updated **{updated[:16].replace('T', ' ')} UTC** · "
             f"history since **{dates[0] if dates else 'today'}** ({len(dates)} snapshot"
             f"{'s' if len(dates) != 1 else ''})")

    # Cheapest platform per popular open model.
    by = defaultdict(list)
    for r in rows:
        if r["source"] == "openrouter" and r["open_weight"] == "True" and r["metric"] == "input":
            by[(r["model_key"], r["model_name"])].append(r)
    outs = defaultdict(dict)
    for r in rows:
        if r["source"] == "openrouter" and r["metric"] == "output":
            outs[r["model_key"]][r["platform"]] = r["usd_per_1m"]

    lines = ["| Model | Platforms | Cheapest | Input $/M | Output $/M | Spread |",
             "|---|--:|---|--:|--:|--:|"]
    ranked = sorted(by.items(), key=lambda kv: -len(kv[1]))[:15]
    for (key, name), eps in ranked:
        best = min(eps, key=lambda e: e["usd_per_1m"])
        hi = max(e["usd_per_1m"] for e in eps)
        o = outs.get(key, {}).get(best["platform"])
        lines.append(f"| {name} | {len(eps)} | {best['platform']} | "
                     f"${best['usd_per_1m']:,.2f} | {'—' if not o else f'${o:,.2f}'} | "
                     f"{hi / best['usd_per_1m']:.1f}× |")
    table = "\n".join(lines)

    moves = [h for h in hist if h["old_usd_per_1m"] and h["new_usd_per_1m"] and h["pct_change"]]
    moves.sort(key=lambda h: abs(float(h["pct_change"])), reverse=True)
    if moves:
        ml = ["| Date | Model | Platform | Metric | Old | New | Change |", "|---|---|---|---|--:|--:|--:|"]
        for h in moves[:10]:
            pct = float(h["pct_change"])
            ml.append(f"| {h['observed_at'][:10]} | {h['model_name']} | {h['platform']} | "
                      f"{h['metric']} | ${float(h['old_usd_per_1m']):,.2f} | "
                      f"${float(h['new_usd_per_1m']):,.2f} | {pct:+.1f}% |")
        moves_md = "\n".join(ml)
    else:
        moves_md = ("_No price moves recorded yet. This table fills in as soon as any tracked "
                    "price changes — the first run only establishes a baseline._")

    with open(README) as f:
        text = f.read()
    text = replace(text, "STATS", stats)
    text = replace(text, "TABLE", table)
    text = replace(text, "MOVES", moves_md)
    with open(README, "w") as f:
        f.write(text)
    print(f"README updated: {len(rows)} rows, {len(ranked)} table entries, {len(moves)} moves")


if __name__ == "__main__":
    main()
