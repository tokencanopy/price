"""Render feed.xml — an Atom feed of price changes.

Subscribers poll this file, so unlike an email list it stores nothing about
who is reading. The feed is generated only from real price moves; first
observations are excluded, or day one would emit 13,000 entries.

The feed-level <updated> is the newest change, never now(), so a run where
nothing moved regenerates a byte-identical file.
"""
import csv, hashlib, os
from collections import defaultdict
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY = os.path.join(ROOT, "data", "history", "price_changes.csv")
OUT = os.path.join(ROOT, "feed.xml")

SITE = "https://tokencanopy.github.io/price"
REPO = "https://github.com/tokencanopy/price"
FEED_ID = "tag:tokencanopy.github.io,2026:price"
MAX_ENTRIES = 50
# Above this many moves in one run, emit a single summary entry instead of one
# per change - a provider repricing its whole catalogue should not flood a
# subscriber's reader with 200 notifications.
BURST = 5

METRIC = {"input": "input", "output": "output",
          "cache_read": "cached input", "cache_write": "cache write"}


def money(v):
    v = float(v)
    return f"${v:,.4f}".rstrip("0").rstrip(".") if v < 0.01 else f"${v:,.2f}"


def describe(c):
    verb = "cut" if float(c["pct_change"]) < 0 else "raised"
    pct = abs(float(c["pct_change"]))
    metric = METRIC.get(c["metric"], c["metric"])
    return (f"{c['platform']} {verb} {c['model_name']} {metric} {pct:.0f}%: "
            f"{money(c['old_usd_per_1m'])} → {money(c['new_usd_per_1m'])} per 1M tokens")


def entry_id(*parts):
    h = hashlib.sha1("|".join(parts).encode()).hexdigest()[:16]
    return f"{FEED_ID}/{h}"


def main():
    rows = []
    if os.path.exists(HISTORY):
        with open(HISTORY) as f:
            rows = [r for r in csv.DictReader(f)
                    if r.get("old_usd_per_1m") and r.get("new_usd_per_1m")
                    and r.get("pct_change")]

    by_run = defaultdict(list)
    for r in rows:
        by_run[r["observed_at"]].append(r)

    entries = []
    for run in sorted(by_run, reverse=True):
        changes = by_run[run]
        if len(changes) > BURST:
            top = sorted(changes, key=lambda c: -abs(float(c["pct_change"])))[:10]
            body = "".join(f"<li>{escape(describe(c))}</li>" for c in top)
            more = (f"<p>…and {len(changes)-len(top)} more.</p>"
                    if len(changes) > len(top) else "")
            entries.append({
                "id": entry_id(run, "summary"),
                "title": f"{len(changes)} price changes",
                "updated": run,
                "content": f"<ul>{body}</ul>{more}",
            })
        else:
            for c in sorted(changes, key=lambda c: -abs(float(c["pct_change"]))):
                entries.append({
                    "id": entry_id(run, c["platform"], c["model_key"], c["metric"]),
                    "title": describe(c),
                    "updated": run,
                    "content": (f"<p>{escape(describe(c))}</p>"
                                f"<p>Model: {escape(c['model_name'])} · "
                                f"Platform: {escape(c['platform'])}</p>"),
                })
        if len(entries) >= MAX_ENTRIES:
            break
    entries = entries[:MAX_ENTRIES]

    updated = entries[0]["updated"] if entries else "2026-09-02T00:00:00+00:00"
    parts = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        f"  <id>{FEED_ID}</id>",
        "  <title>LLM Price Index — price changes</title>",
        "  <subtitle>Every tracked change to LLM inference pricing, across 100+ platforms.</subtitle>",
        f"  <updated>{updated}</updated>",
        f'  <link rel="self" href="{SITE}/feed.xml"/>',
        f'  <link rel="alternate" type="text/html" href="{REPO}"/>',
        "  <author><name>LLM Price Index</name></author>",
    ]
    if not entries:
        parts += [
            "  <entry>",
            f"    <id>{FEED_ID}/baseline</id>",
            "    <title>Tracking started — no price changes recorded yet</title>",
            f"    <updated>{updated}</updated>",
            f'    <link rel="alternate" href="{REPO}"/>',
            '    <content type="html">Baseline captured. This feed publishes an '
            "entry whenever a tracked price moves.</content>",
            "  </entry>",
        ]
    for e in entries:
        parts += [
            "  <entry>",
            f"    <id>{e['id']}</id>",
            f"    <title>{escape(e['title'])}</title>",
            f"    <updated>{e['updated']}</updated>",
            f'    <link rel="alternate" type="text/html" href="{REPO}#biggest-price-moves"/>',
            f'    <content type="html">{escape(e["content"])}</content>',
            "  </entry>",
        ]
    parts.append("</feed>")

    with open(OUT, "w") as f:
        f.write("\n".join(parts) + "\n")
    print(f"feed.xml: {len(entries)} entr{'y' if len(entries)==1 else 'ies'} "
          f"from {len(rows)} recorded change(s)")


if __name__ == "__main__":
    main()
