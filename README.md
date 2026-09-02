# LLM Price Index

**A public, machine-readable record of what LLM inference actually costs — and how that price changes over time.** Refreshed every 6 hours.

<!-- BEGIN STATS -->
**13,376** price points · **883** models · **73** platforms · updated **2026-09-02 05:18 UTC** · history since **2026-09-02** (1 snapshot)
<!-- END STATS -->

Every provider publishes today's price. **Nobody publishes yesterday's.** This repo
fixes that by writing the number down every 6 hours, in git, forever.

---

## Same model, very different price

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="charts/dispersion-dark.png">
  <img alt="Input price per provider as a multiple of the cheapest provider, for the most widely-served open models" src="charts/dispersion-light.png">
</picture>

Open-weight models are served by dozens of platforms at wildly different prices for
what is nominally the same set of weights. Across the 44 open models served by 5 or
more platforms, the **median spread is 2.0×** and **48% of models span more than 2×**.

The obvious explanation — cheap endpoints are quantized harder — **does not hold**. Of
those 44 models, the cheapest endpoint runs at full BF16 precision in 20 cases, more
often than FP8 (14) or FP4 (10). The most expensive endpoint is the BF16 one in 31 of
44. What you are mostly paying for is hardware, margin and throughput: the priciest
gpt-oss-120b endpoint is Cerebras at 11.7× the cheapest, and it is selling speed, not
precision. The chart marks quantization by shape and colour so you can check this
yourself.

## What it costs to run each model today

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="charts/cheapest-dark.png">
  <img alt="Input and output price per 1M tokens at the cheapest platform for each popular open model" src="charts/cheapest-light.png">
</picture>

<!-- BEGIN TABLE -->
| Model | Platforms | Cheapest | Input $/M | Output $/M | Spread |
|---|--:|---|--:|--:|--:|
| DeepSeek: DeepSeek V4 Flash 0731 | 30 | OpenInference | $0.05 | $0.16 | 8.8× |
| Z.ai: GLM 5.2 | 26 | DeepInfra | $0.49 | $1.56 | 2.9× |
| Z.ai: GLM 5.3 | 24 | AkashML | $1.17 | $3.96 | 1.5× |
| Z.ai: GLM 5.3 Flash | 22 | DeepInfra | $0.07 | $0.25 | 2.0× |
| MoonshotAI: Kimi K2.6 | 20 | Inceptron | $0.53 | $3.39 | 2.1× |
| OpenAI: gpt-oss-120b | 18 | AkashML | $0.03 | $0.17 | 11.7× |
| DeepSeek: DeepSeek V4 Flash 0423 | 17 | DigitalOcean | $0.07 | $0.17 | 6.5× |
| DeepSeek: DeepSeek V4 Pro 0423 | 17 | DigitalOcean | $0.87 | $1.74 | 2.2× |
| DeepSeek: DeepSeek V4 Pro 0813 | 17 | DeepSeek | $0.66 | $1.98 | 2.2× |
| Z.ai: GLM 5.1 | 16 | GMICloud | $0.91 | $2.86 | 1.7× |
| DeepSeek: DeepSeek V3.2 | 15 | GMICloud | $0.21 | $0.31 | 14.4× |
| MoonshotAI: Kimi K2.7 Code | 15 | Inceptron | $0.66 | $3.40 | 1.4× |
| MoonshotAI: Kimi K3 | 15 | Makora | $2.55 | $12.75 | 1.4× |
| Google: Gemma 4 31B | 15 | DeepInfra | $0.09 | $0.38 | 11.0× |
| OpenAI: gpt-oss-20b | 13 | AkashML | $0.02 | $0.10 | 3.8× |
<!-- END TABLE -->

## Biggest price moves

<!-- BEGIN MOVES -->
_No price moves recorded yet. This table fills in as soon as any tracked price changes — the first run only establishes a baseline._
<!-- END MOVES -->

---

## Why this exists

OpenRouter already answers "what does this model cost right now, on 105 platforms",
and it does it well — this repo uses it as a primary source rather than competing with
it. What no public API answers is **"what did it cost last month?"**

Price history is the one dataset that cannot be backfilled. It only exists if somebody
starts writing it down. So: every 6 hours, fetch, diff, commit.

## The data

| File | What |
|---|---|
| `data/current/prices.csv` | Today's normalized snapshot, long format, one row per price |
| `data/history/price_changes.csv` | **Append-only change log** — a row only when a price actually moves |
| `data/raw/` | Verbatim provider payloads, so any parsing error can be re-run against the original |

Prices move rarely, so the change log stays small while still reconstructing a full
step-function series for any key. To rebuild a series, take the change rows for a key
in `observed_at` order — each row holds the value from that moment until the next.

**Schema** (`prices.csv`): `collected_at, source, platform, model_key, model_name,
author, open_weight, variant, region, metric, usd_per_1m, context_length, effective_date`

- `metric` — `input` · `output` · `cache_read` · `cache_write`
- `variant` — quantization (`fp8`, `fp4`, …) for inference platforms; tier
  (`standard`, `batch`, `priority`) for cloud providers
- `model_key` — Hugging Face repo id for open-weight models, so the same model joins
  across platforms without fuzzy name matching
- All prices are **USD per 1,000,000 tokens**

## Sources

| Source | Auth | Coverage |
|---|---|---|
| OpenRouter | none | ~105 platforms, per-model per-provider pricing incl. quantization |
| AWS Bedrock Price List API | none | Per-region, plus batch / priority tiers OpenRouter does not expose |
| Azure Retail Prices API | none | Foundry Models meters |
| Google Vertex AI | _planned_ | Billing Catalog API needs a free API key |

## Caveats

Read these before quoting a number.

- **Cheapest is not equivalent.** Providers differ in quantization, context window,
  throughput, rate limits and reliability. A 2× price gap is not automatically a 2×
  saving.
- **Azure meter names are heavily abbreviated** (`5.4 opt Dz 1M Tokens`). Meters that
  can't be parsed unambiguously are dropped rather than guessed at.
- **List prices only.** No committed-use discounts, negotiated rates or free tiers.
- Prices are collected automatically and may be wrong. **Verify with the provider
  before making a purchasing decision.** Not affiliated with any provider.

## Running it

```bash
python -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/python scripts/collect.py       # fetch raw payloads
./.venv/bin/python scripts/normalize.py     # normalize + append changes
./.venv/bin/python scripts/charts.py        # render README charts
./.venv/bin/python scripts/render_readme.py # inject tables
```

No API keys required.

## Development

CI owns everything under `data/` and `charts/` — it regenerates them every 6 hours
and commits. So local work should be **code-only commits**, branched from a freshly
fetched `origin/main`:

```bash
git fetch origin && git worktree add .worktrees/<name> -b <type>/<name> origin/main
```

If you ever hit a merge conflict in `prices.csv` or the raw JSON, do not resolve it
by hand — reset to origin and let the pipeline regenerate.

A healthy no-change run touches exactly two lines (the README timestamp and
`meta.json`). If a run with no price movement rewrites more than that, something
volatile is leaking into the archive; strip it in `stabilize()` rather than letting
it accumulate.

## License

Code: MIT. Data: CC BY 4.0 — attribution appreciated, corrections more so.
