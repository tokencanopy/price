# LLM Price Index

**A public, machine-readable record of what LLM inference actually costs — and how that price changes over time.** Refreshed every 6 hours.

<!-- BEGIN STATS -->
**14,539** price points · **947** models · **78** platforms · updated **2026-09-23 18:34 UTC** · history since **2026-09-02** (22 snapshots)
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
| Z.ai: GLM 5.3 | 32 | [Baidu](https://intl.cloud.baidu.com/) | $0.56 | $1.76 | 3.7× |
| Z.ai: GLM 5.3 Flash | 30 | [DeepInfra](https://deepinfra.com/) | $0.07 | $0.25 | 6.0× |
| DeepSeek: DeepSeek V4 Flash 0731 | 29 | [Sail Research](https://www.sailresearch.com/) | $0.04 | $0.55 | 11.6× |
| DeepSeek: DeepSeek V4.1 Flash | 25 | [DekaLLM](https://docs.cloudeka.ai/) | $0.10 | $1.00 | 3.8× |
| Z.ai: GLM 5.2 | 23 | [Baidu](https://intl.cloud.baidu.com/) | $0.56 | $1.76 | 4.0× |
| DeepSeek: DeepSeek V4 Pro 0813 | 22 | [Baidu](https://intl.cloud.baidu.com/) | $0.40 | $1.20 | 4.1× |
| OpenAI: gpt-oss-120b | 21 | [AkashML](https://akashml.com/) | $0.03 | $0.17 | 11.7× |
| MoonshotAI: Kimi K2.6 | 21 | [Inceptron](https://www.inceptron.io/) | $0.43 | $2.38 | 2.5× |
| MoonshotAI: Kimi K3 | 17 | [Sail Research](https://www.sailresearch.com/) | $1.50 | $10.76 | 2.3× |
| Qwen: Qwen3.8 27B | 16 | [Darkbloom](https://www.darkbloom.dev/) | $0.10 | $1.80 | 4.5× |
| DeepSeek: DeepSeek V3.2 | 15 | [GMICloud](https://gmicloud.ai/) | $0.21 | $0.31 | 14.4× |
| DeepSeek: DeepSeek V4 Flash 0423 | 15 | [StreamLake](https://www.streamlake.ai/) | $0.08 | $0.16 | 2.5× |
| DeepSeek: DeepSeek V4 Pro 0423 | 15 | [StreamLake](https://www.streamlake.ai/) | $0.95 | $1.90 | 2.0× |
| MoonshotAI: Kimi K2.7 Code | 14 | [DeepInfra](https://deepinfra.com/) | $0.68 | $3.40 | 1.4× |
| Z.ai: GLM 5.1 | 14 | [Baidu](https://intl.cloud.baidu.com/) | $0.96 | $3.03 | 1.5× |
<!-- END TABLE -->

## Biggest price moves

<!-- BEGIN MOVES -->
| Date | Model | Platform | Metric | Old | New | Change |
|---|---|---|---|--:|--:|--:|
| 2026-09-14 | DeepSeek: DeepSeek V4 Flash 0731 | [Baidu](https://intl.cloud.baidu.com/) | input | $0.04 | $0.44 | +1150.0% |
| 2026-09-14 | DeepSeek: DeepSeek V4 Flash 0731 | [Baidu](https://intl.cloud.baidu.com/) | output | $0.11 | $1.32 | +1150.0% |
| 2026-09-14 | DeepSeek: DeepSeek V4 Flash 0731 | [Baidu](https://intl.cloud.baidu.com/) | cache_read | $0.00 | $0.01 | +1150.0% |
| 2026-09-14 | DeepSeek: DeepSeek V4 Flash 0423 | [OpenInference](https://www.openinference.ai/) | cache_read | $0.00 | $0.01 | +1066.7% |
| 2026-09-06 | Qwen: Qwen3.8 27B | [Darkbloom](https://www.darkbloom.dev/) | output | $0.20 | $2.00 | +900.0% |
| 2026-09-21 | DeepSeek: DeepSeek V4 Flash 0731 | [Baidu](https://intl.cloud.baidu.com/) | input | $0.05 | $0.44 | +817.4% |
| 2026-09-21 | DeepSeek: DeepSeek V4 Flash 0731 | [Baidu](https://intl.cloud.baidu.com/) | output | $0.14 | $1.32 | +817.4% |
| 2026-09-21 | DeepSeek: DeepSeek V4 Flash 0731 | [Baidu](https://intl.cloud.baidu.com/) | cache_read | $0.00 | $0.01 | +817.4% |
| 2026-09-16 | Qwen: Qwen3.8 27B | [Mancer 2](https://mancer.tech/) | input | $0.25 | $2.25 | +800.0% |
| 2026-09-16 | DeepSeek: DeepSeek V4 Flash 0731 | [Baidu](https://intl.cloud.baidu.com/) | input | $0.06 | $0.44 | +635.3% |
<!-- END MOVES -->

---

## Subscribe

Price changes are published as an **[Atom feed](https://tokencanopy.github.io/price/feed.xml)** —
one entry per move, or a single summary entry when a platform reprices its whole catalogue.

```
https://tokencanopy.github.io/price/feed.xml
```

Drop that into any feed reader, or into a Slack or Discord channel with
`/feed subscribe <url>` to get price-drop alerts where your team already works. The feed
stores nothing about who is reading it — there is no subscriber list.

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
| `data/current/providers.csv` | Platform → verified homepage, status page, HQ |
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

Every platform below links to its own site where we could verify one resolves, and
to its OpenRouter page otherwise. The mapping lives in `data/current/providers.csv`.

<!-- BEGIN PLATFORMS -->
<details>
<summary><b>All 111 platforms</b> (number of models priced, where we track any)</summary>

[AI21](https://www.ai21.com/) · [AionLabs](https://www.aionlabs.ai/) (6) · [AkashML](https://akashml.com/) (6) · [Alibaba](https://www.alibabacloud.com/) (56) · [Amazon Bedrock](https://aws.amazon.com/) (36) · [Amazon Nova](https://openrouter.ai/provider/amazon-nova) · [Ambient](https://openrouter.ai/provider/ambient) · [Anthropic](https://www.anthropic.com/) (12) · [Arcee AI](https://openrouter.ai/provider/arcee-ai) (1) · [AssemblyAI](https://www.assemblyai.com/) · [AtlasCloud](https://www.atlascloud.ai/) (28) · [Avian](https://avian.io/) · [AWS Bedrock](https://aws.amazon.com/bedrock/pricing/) (77) · [Azure](https://www.microsoft.com/) (52) · [Azure Foundry](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/) (532) · [Baidu](https://intl.cloud.baidu.com/) (10) · [BaseTen](https://www.baseten.co/) (14) · [Black Forest Labs](https://bfl.ai/) · [Cerebras](https://www.cerebras.ai/) (1) · [Chutes](https://chutes.ai/) (6) · [Cirrascale](https://www.cirrascale.com/) · [Clarifai](https://openrouter.ai/provider/clarifai) · [Claude Platform on AWS](https://www.anthropic.com/) (10) · [Cloudflare](https://cloudflare.com/) (18) · [Cohere](https://cohere.com/) (6) · [CoreWeave](https://coreweave.com/) (19) · [Cosine](https://openrouter.ai/provider/cosine) · [Crucible](https://openrouter.ai/provider/crucible) · [Crusoe](https://legal.crusoe.ai/) (6) · [Darkbloom](https://www.darkbloom.dev/) (8) · [Databricks](https://www.databricks.com/) · [Decart](https://cogito.decart.ai/) (3) · [Deepgram](https://deepgram.com/) · [DeepInfra](https://deepinfra.com/) (80) · [DeepSeek](https://deepseek.com/) (2) · [DekaLLM](https://docs.cloudeka.ai/) (8) · [DigitalOcean](https://www.digitalocean.com/) (16) · [FakeProvider](https://openrouter.ai/provider/fake-provider) · [Featherless](https://featherless.ai/) · [Fireworks](https://fireworks.ai/) (11) · [Fish Audio](https://fish.audio/) · [Friendli](https://friendli.ai/) (7) · [GMICloud](https://gmicloud.ai/) (23) · [Google](https://google.com/) (43) · [Google AI Studio](https://google.com/) (20) · [Groq](https://groq.com/) (6) · [HeyGen](https://www.heygen.com/) · [Inception](https://www.inceptionlabs.ai/) (2) · [Inceptron](https://www.inceptron.io/) (6) · [Inferact vLLM](https://openrouter.ai/provider/inferact-vllm) · [InferenceNet](https://inference.net/) (5) · [Infermatic](https://infermatic.ai/) · [Inflection](https://inflection.ai/) · [Io Net](https://io.net/) (2) · [Ionstream](https://ionstream.ai/) (2) · [Krea](https://www.krea.ai/) (1) · [Liquid](https://www.liquid.ai/) · [Makora](https://makora.statuspage.io/) (5) · [Mancer 2](https://mancer.tech/) (9) · [Mara](https://www.mara.com/) (5) · [Meta](https://www.facebook.com/) (5) · [Minimax](https://www.minimax.io/) (8) · [Mistral](https://mistral.ai/) (14) · [Modal](https://modal.com/) (5) · [ModelRun](https://www.modular.com/) (3) · [Modular](https://www.runmodelrun.com/) · [Moonshot AI](https://moonshot.ai/) (3) · [Morph](https://morphllm.com/) (7) · [Near AI](https://near.ai/) (1) · [Nebius](https://nebius.com/) (8) · [Nex AGI](https://nex-agi.cn/) (2) · [NextBit](https://www.nextbit256.com/) (10) · [Novita](https://novita.ai/) (73) · [Nvidia](https://www.nvidia.com/) · [Ollama](https://openrouter.ai/provider/ollama) · [OpenAI](https://openai.com/) (54) · [OpenInference](https://www.openinference.ai/) (4) · [Parasail](https://www.parasail.io/) (38) · [Perceptron](https://www.perceptron.inc/) (1) · [Perplexity](https://perplexity.ai/) (5) · [Phala](https://redpill.ai/) (20) · [Poolside](https://poolside.ai/) (2) · [PrimeIntellect](https://openrouter.ai/provider/prime-intellect) (1) · [Quiver](https://openrouter.ai/provider/quiver) · [Recraft](https://openrouter.ai/provider/recraft) · [Reka](https://reka.ai/) (6) · [Relace](https://www.relace.ai/) (6) · [Runway](https://runwayml.com/) · [Sail Research](https://www.sailresearch.com/) (7) · [Sakana AI](https://sakana.ai/) (4) · [SambaNova](https://sambanova.ai/) (7) · [Seed](https://byteplus.com/) (6) · [SiliconFlow](https://siliconflow.com/) (40) · [Sourceful](https://www.sourceful.com/) · [Stealth](https://openrouter.ai/) · [StepFun](https://stepfun.ai/) (1) · [StreamLake](https://www.streamlake.ai/) (23) · [Switchpoint](https://openrouter.ai/provider/switchpoint) · [Tencent](https://www.tencentcloud.com/) (5) · [Tenstorrent](https://tenstorrent.com/) · [Thinking Machines](https://thinkingmachines.ai/) · [Together](https://www.together.ai/) (14) · [TypeSafe](https://typesafe.ai/) · [Unbiased](https://unbiased.ai/) (1) · [Upstage](https://www.upstage.ai/) (3) · [Venice](https://venice.ai/) (36) · [VoyageAI by MongoDB](https://www.voyageai.com/) · [Wafer](https://www.wafer.ai/) (8) · [xAI](https://x.ai/) (7) · [Xiaomi](https://platform.xiaomimimo.com/) (5) · [Z.AI](https://z.ai/) (14)

</details>
<!-- END PLATFORMS -->

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
