"""Render README charts as PNGs, one pair per chart (light + dark).

GitHub READMEs cannot run JavaScript, so charts ship as committed images and
the README swaps them with <picture>. Palette is the validated 3-slot
categorical set; quantization also carries a marker shape so identity never
depends on colour alone.
"""
import csv, os, zlib
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRENT = os.path.join(ROOT, "data", "current", "prices.csv")
HISTORY = os.path.join(ROOT, "data", "history", "price_changes.csv")
OUT = os.path.join(ROOT, "charts")

THEMES = {
    "light": dict(surface="#fcfcfb", text="#0b0b0b", text2="#52514e", grid="#e4e3df",
                  series=["#2a78d6", "#eb6834", "#1baf7a"]),
    "dark":  dict(surface="#1a1a19", text="#ffffff", text2="#c3c2b7", grid="#3a3936",
                  series=["#3987e5", "#d95926", "#199e70"]),
}
QUANTS = ["FP4", "FP8", "BF16 / other"]
MARKERS = {"FP4": "o", "FP8": "s", "BF16 / other": "^"}


def qgroup(q):
    q = (q or "").lower()
    if "fp4" in q:
        return "FP4"
    if "fp8" in q:
        return "FP8"
    return "BF16 / other"


def load_current():
    if not os.path.exists(CURRENT):
        return []
    with open(CURRENT) as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["usd_per_1m"] = float(r["usd_per_1m"])
    return rows


def style(ax, th, title, subtitle="", xlabel=""):
    fig = ax.figure
    fig.patch.set_facecolor(th["surface"])
    ax.set_facecolor(th["surface"])
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(th["grid"])
    ax.tick_params(colors=th["text2"], labelsize=9, length=0)
    ax.grid(axis="x", color=th["grid"], linewidth=0.8, alpha=0.9)
    ax.set_axisbelow(True)
    if xlabel:
        ax.set_xlabel(xlabel, color=th["text2"], fontsize=9, labelpad=8)
    ax.set_title(title, color=th["text"], fontsize=13, fontweight="bold",
                 loc="left", pad=(16 + 17 * (subtitle.count("\n") + 1)) if subtitle else 10)
    if subtitle:
        ax.text(0, 1.02, subtitle, transform=ax.transAxes, color=th["text2"],
                fontsize=9, va="bottom", linespacing=1.6)


def top_open_models(rows, n, metric="input"):
    """Rank open-weight models by how many platforms serve them - a data-driven
    stand-in for 'models people care about', so no hand-maintained list rots."""
    by = defaultdict(list)
    for r in rows:
        if r["source"] == "openrouter" and r["open_weight"] == "True" and r["metric"] == metric:
            by[(r["model_key"], r["model_name"])].append(r)
    ranked = sorted(by.items(), key=lambda kv: -len(kv[1]))
    return [(k[1], v) for k, v in ranked if len(v) >= 3][:n]


def spread_stats(rows, min_platforms=5):
    """Headline numbers, computed from the data rather than asserted."""
    by = defaultdict(list)
    for r in rows:
        if r["source"] == "openrouter" and r["open_weight"] == "True" and r["metric"] == "input":
            by[r["model_key"]].append(r["usd_per_1m"])
    sp = sorted(max(v) / min(v) for v in by.values() if len(v) >= min_platforms)
    if not sp:
        return 0, 0, 0
    return len(sp), sp[len(sp) // 2], sp[-1]


def chart_dispersion(rows, mode):
    th = THEMES[mode]
    models = top_open_models(rows, 9)
    if not models:
        return None
    n_models, median_spread, _ = spread_stats(rows)
    fig, ax = plt.subplots(figsize=(11, 7), dpi=160)
    labels, shown_max = [], 1.0
    for y, (name, eps) in enumerate(reversed(models)):
        cheapest = min(e["usd_per_1m"] for e in eps)
        # Deterministic jitter keyed on platform name: separates overplotted
        # points without the chart reshuffling on every daily run.
        for e in eps:
            g = qgroup(e["variant"])
            # crc32, not hash(): Python randomizes string hashing per process,
            # which would repaint every chart on every run.
            jitter = ((zlib.crc32(e["platform"].encode()) % 1000) / 1000 - 0.5) * 0.34
            ax.plot(e["usd_per_1m"] / cheapest, y + jitter, MARKERS[g], markersize=7.5,
                    color=th["series"][QUANTS.index(g)], alpha=0.9,
                    markeredgecolor=th["surface"], markeredgewidth=1.1, zorder=3)
        spread = max(e["usd_per_1m"] for e in eps) / cheapest
        shown_max = max(shown_max, spread)
        ax.text(1.015, y, f"{spread:.1f}\N{MULTIPLICATION SIGN}", transform=ax.get_yaxis_transform(),
                va="center", ha="left", color=th["text"], fontsize=9.5, fontweight="bold")
        short = name.split(":")[-1].strip()
        labels.append(f"{short}\n{len(eps)} platforms \N{MIDDLE DOT} from ${cheapest:,.2f}/M")
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels(labels, color=th["text"], fontsize=9)
    ax.set_ylim(-0.7, len(models) - 0.3)
    ax.set_xscale("log")
    ticks = [t for t in (1, 1.5, 2, 3, 5, 8, 12, 20) if t <= shown_max * 1.25]
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{t:g}\N{MULTIPLICATION SIGN}" for t in ticks])
    ax.set_xlim(0.88, shown_max * 1.3)
    ax.axvline(1.0, color=th["grid"], linewidth=1.5, zorder=1)
    style(ax, th,
          f"The same open model costs up to {shown_max:.0f}\N{MULTIPLICATION SIGN} more depending on where you run it",
          f"Input price at each platform, relative to the cheapest platform for that model (log scale). Across all {n_models} open\n"
          f"models served by 5+ platforms the median spread is {median_spread:.1f}\N{MULTIPLICATION SIGN}. Quantization does not explain it \N{EM DASH} the\n"
          f"cheapest endpoint runs at full precision as often as not.",
          "price relative to cheapest platform")
    handles = [Line2D([], [], marker=MARKERS[q], linestyle="", markersize=8,
                      color=th["series"][i], label=q) for i, q in enumerate(QUANTS)]
    leg = ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=9,
                    ncol=3, bbox_to_anchor=(1.0, -0.18))
    for t in leg.get_texts():
        t.set_color(th["text2"])
    fig.tight_layout()
    fig.subplots_adjust(right=0.93, top=0.78)
    path = os.path.join(OUT, f"dispersion-{mode}.png")
    fig.savefig(path, facecolor=th["surface"], metadata={"Software": "llm-price-index"})
    plt.close(fig)
    return path


def chart_cheapest(rows, mode):
    th = THEMES[mode]
    models = top_open_models(rows, 10)
    if not models:
        return None
    outs = defaultdict(dict)
    for r in rows:
        if r["source"] == "openrouter" and r["metric"] == "output":
            outs[r["model_key"]][r["platform"]] = r["usd_per_1m"]
    data = []
    for name, eps in models:
        best = min(eps, key=lambda e: e["usd_per_1m"])
        o = outs.get(best["model_key"], {}).get(best["platform"])
        if o:
            data.append((name.split(":")[-1].strip(), best["platform"], best["usd_per_1m"], o))
    if not data:
        return None
    data.sort(key=lambda d: d[2] + d[3])
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=160)
    ys = range(len(data))
    h = 0.36
    for i, (name, plat, pin, pout) in enumerate(data):
        ax.barh(i + h / 2 + 0.02, pin, height=h, color=th["series"][0], zorder=3)
        ax.barh(i - h / 2 - 0.02, pout, height=h, color=th["series"][1], zorder=3)
        ax.text(pin + max(d[3] for d in data) * 0.012, i + h / 2 + 0.02, f"${pin:,.2f}",
                va="center", fontsize=8.5, color=th["text2"])
        ax.text(pout + max(d[3] for d in data) * 0.012, i - h / 2 - 0.02, f"${pout:,.2f}",
                va="center", fontsize=8.5, color=th["text2"])
    ax.set_xlim(0, max(d[3] for d in data) * 1.12)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([f"{n}\non {p}" for n, p, _, _ in data], color=th["text"], fontsize=9)
    style(ax, th, "Cheapest way to run each popular open model today",
          "For each model, the platform with the lowest input price, showing that "
          "platform's input and output rates.",
          "USD per 1M tokens")
    handles = [Line2D([], [], marker="s", linestyle="", markersize=9, color=th["series"][0], label="input"),
               Line2D([], [], marker="s", linestyle="", markersize=9, color=th["series"][1], label="output")]
    leg = ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=9, ncol=2,
                    bbox_to_anchor=(1.0, -0.20))
    for t in leg.get_texts():
        t.set_color(th["text2"])
    fig.tight_layout()
    path = os.path.join(OUT, f"cheapest-{mode}.png")
    fig.savefig(path, facecolor=th["surface"], metadata={"Software": "llm-price-index"})
    plt.close(fig)
    return path


def chart_history(mode):
    """Price over time. Deliberately renders nothing until real history exists -
    a single observation is not a trend and must not be drawn as one."""
    if not os.path.exists(HISTORY):
        return None
    with open(HISTORY) as f:
        rows = list(csv.DictReader(f))
    dates = {r["observed_at"][:10] for r in rows}
    if len(dates) < 2:
        print(f"  history: {len(dates)} date(s) collected - trend chart skipped until >= 2")
        return None
    return None      # implemented once the second day of data lands


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    rows = load_current()
    print(f"loaded {len(rows)} price rows")
    for mode in ("light", "dark"):
        for fn in (chart_dispersion, chart_cheapest):
            p = fn(rows, mode)
            if p:
                print("  wrote", os.path.relpath(p, ROOT))
        chart_history(mode)
