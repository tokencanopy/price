# LLM Price Index

**A public, machine-readable record of what LLM inference actually costs — and how that price changes over time.** Refreshed every 6 hours.

<!-- BEGIN STATS -->
**17,174** price points · **1,068** models · **83** platforms · updated **2026-10-30 12:32 UTC** · history since **2026-09-02** (59 snapshots)
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
| Z.ai: GLM 5.3 | 39 | [Wafer](https://www.wafer.ai/) | $0.07 | $1.40 | 30.0× |
| DeepSeek: DeepSeek V4.1 Flash 1017 | 35 | [Morph](https://morphllm.com/) | $0.03 | $0.27 | 10.6× |
| Z.ai: GLM 5.3 Flash | 35 | [Relace](https://www.relace.ai/) | $0.02 | $0.11 | 7.9× |
| DeepSeek: DeepSeek V4.1 Flash | 32 | [Morph](https://morphllm.com/) | $0.03 | $0.27 | 10.6× |
| Z.ai: GLM 5.2 | 27 | [Wafer](https://www.wafer.ai/) | $0.01 | $7.00 | 375.0× |
| OpenAI: gpt-oss-120b | 24 | [AkashML](https://akashml.com/) | $0.03 | $0.19 | 11.7× |
| DeepSeek: DeepSeek V4 Flash 0731 | 23 | [Wafer](https://www.wafer.ai/) | $0.06 | $0.23 | 7.9× |
| DeepSeek: DeepSeek V4 Pro 0813 | 23 | [Relace](https://www.relace.ai/) | $0.10 | $4.00 | 15.9× |
| MoonshotAI: Kimi K3 | 21 | [Relace](https://www.relace.ai/) | $0.15 | $10.16 | 22.6× |
| Qwen: Qwen3.8 27B | 21 | [Darkbloom](https://www.darkbloom.dev/) | $0.04 | $1.50 | 28.3× |
| DeepSeek: DeepSeek V4 Flash 0423 | 17 | [Relace](https://www.relace.ai/) | $0.05 | $0.45 | 12.0× |
| MoonshotAI: Kimi K2.6 | 17 | [Chutes](https://chutes.ai/) | $0.39 | $1.80 | 2.8× |
| Google: Gemma 4 26B A4B  | 15 | [PrimeIntellect](https://openrouter.ai/provider/prime-intellect) | $0.03 | $0.09 | 5.0× |
| DeepSeek: DeepSeek V4 Pro 0423 | 14 | [StreamLake](https://www.streamlake.ai/) | $0.82 | $1.63 | 2.3× |
| Google: Gemma 4 31B | 14 | [CoreWeave](https://coreweave.com/) | $0.10 | $0.34 | 7.5× |
<!-- END TABLE -->

## Biggest price moves

<!-- BEGIN MOVES -->
| Date | Model | Platform | Metric | Old | New | Change |
|---|---|---|---|--:|--:|--:|
| 2026-10-11 | DeepSeek: DeepSeek V4.1 Flash | [OpenInference](https://www.openinference.ai/) | input | $0.00 | $0.06 | +49900.0% |
| 2026-10-11 | DeepSeek: DeepSeek V4.1 Flash | [Relace](https://www.relace.ai/) | input | $0.00 | $0.05 | +49900.0% |
| 2026-10-10 | DeepSeek: DeepSeek V4 Flash 0423 | [OpenInference](https://www.openinference.ai/) | output | $0.01 | $1.54 | +10370.4% |
| 2026-10-10 | DeepSeek: DeepSeek V4 Flash 0731 | [OpenInference](https://www.openinference.ai/) | output | $0.01 | $1.54 | +10370.4% |
| 2026-10-27 | DeepSeek: DeepSeek V4.1 Flash | [OpenInference](https://www.openinference.ai/) | output | $0.01 | $1.00 | +9900.0% |
| 2026-10-27 | DeepSeek: DeepSeek V4.1 Flash 1017 | [OpenInference](https://www.openinference.ai/) | output | $0.01 | $1.00 | +9900.0% |
| 2026-10-07 | DeepSeek: DeepSeek V4 Flash 0423 | [Relace](https://www.relace.ai/) | input | $0.00 | $0.03 | +5900.0% |
| 2026-10-07 | DeepSeek: DeepSeek V4 Flash 0423 | [Relace](https://www.relace.ai/) | cache_read | $0.00 | $0.03 | +5900.0% |
| 2026-10-30 | MoonshotAI: Kimi K3 | [InferenceNet](https://inference.net/) | output | $0.15 | $7.50 | +4900.0% |
| 2026-10-30 | MoonshotAI: Kimi K3 | [InferenceNet](https://inference.net/) | cache_read | $0.00 | $0.15 | +4900.0% |
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
<summary><b>All 119 platforms</b> (number of models priced, where we track any)</summary>

[AI21](https://www.ai21.com/) · [AionLabs](https://www.aionlabs.ai/) (6) · [AkashML](https://akashml.com/) (8) · [Alibaba](https://www.alibabacloud.com/) (33) · [Amazon Bedrock](https://aws.amazon.com/) (39) · [Amazon Nova](https://openrouter.ai/provider/amazon-nova) · [Ambient](https://openrouter.ai/provider/ambient) (1) · [Anthropic](https://www.anthropic.com/) (14) · [Arcee AI](https://openrouter.ai/provider/arcee-ai) · [AssemblyAI](https://www.assemblyai.com/) · [AtlasCloud](https://www.atlascloud.ai/) (25) · [Avian](https://avian.io/) · [AWS Bedrock](https://aws.amazon.com/bedrock/pricing/) (79) · [Azure](https://www.microsoft.com/) (58) · [Azure Foundry](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/) (649) · [Baidu](https://intl.cloud.baidu.com/) (12) · [BaseTen](https://www.baseten.co/) (13) · [Black Forest Labs](https://bfl.ai/) · [Cerebras](https://www.cerebras.ai/) (2) · [Chutes](https://chutes.ai/) (6) · [Cirrascale](https://www.cirrascale.com/) · [Clarifai](https://openrouter.ai/provider/clarifai) · [Claude Platform on AWS](https://www.anthropic.com/) (12) · [Cloudflare](https://cloudflare.com/) (18) · [Cohere](https://cohere.com/) (11) · [CoreWeave](https://coreweave.com/) (22) · [Cosine](https://openrouter.ai/provider/cosine) · [Crucible](https://openrouter.ai/provider/crucible) · [Crusoe](https://legal.crusoe.ai/) (11) · [Darkbloom](https://www.darkbloom.dev/) (12) · [Databricks](https://www.databricks.com/) · [Decart](https://cogito.decart.ai/) (5) · [Deepgram](https://deepgram.com/) · [DeepInfra](https://deepinfra.com/) (69) · [DeepSeek](https://deepseek.com/) (2) · [DekaLLM](https://docs.cloudeka.ai/) (11) · [DigitalOcean](https://www.digitalocean.com/) (19) · [ElevenLabs](https://elevenlabs.io/) · [FakeProvider](https://openrouter.ai/provider/fake-provider) · [Featherless](https://featherless.ai/) (1) · [Fireworks](https://fireworks.ai/) (9) · [Fish Audio](https://fish.audio/) · [Friendli](https://friendli.ai/) (5) · [GMICloud](https://gmicloud.ai/) (30) · [Google](https://google.com/) (33) · [Google AI Studio](https://google.com/) (21) · [Groq](https://groq.com/) (6) · [HeyGen](https://www.heygen.com/) · [Inception](https://www.inceptionlabs.ai/) (3) · [Inceptron](https://www.inceptron.io/) (6) · [Inferact vLLM](https://openrouter.ai/provider/inferact-vllm) · [InferenceNet](https://inference.net/) (8) · [Infermatic](https://infermatic.ai/) · [Inflection](https://inflection.ai/) · [Io Net](https://io.net/) (7) · [Ionstream](https://ionstream.ai/) (3) · [Krea](https://www.krea.ai/) · [KT](https://openrouter.ai/provider/kt) · [Liquid](https://www.liquid.ai/) (2) · [Makora](https://makora.statuspage.io/) (8) · [Mancer 2](https://mancer.tech/) (10) · [Mara](https://www.mara.com/) (4) · [Meta](https://www.facebook.com/) (6) · [Minimax](https://www.minimax.io/) (9) · [Mistral](https://mistral.ai/) (22) · [Modal](https://modal.com/) (7) · [ModelRun](https://www.modular.com/) (6) · [Modular](https://www.runmodelrun.com/) · [Moonshot AI](https://moonshot.ai/) (4) · [Morph](https://morphllm.com/) (8) · [Near AI](https://near.ai/) (3) · [Nebius](https://nebius.com/) (15) · [Nex AGI](https://nex-agi.cn/) (2) · [NextBit](https://www.nextbit256.com/) (6) · [Novita](https://novita.ai/) (47) · [Nvidia](https://www.nvidia.com/) · [Ollama](https://openrouter.ai/provider/ollama) · [OpenAI](https://openai.com/) (46) · [OpenInference](https://www.openinference.ai/) (3) · [Parasail](https://www.parasail.io/) (40) · [ParetoAlpha](https://paretoalphainference.com/) (1) · [Particle AI](https://particle.ai/) (3) · [Perceptron](https://www.perceptron.inc/) (2) · [Perplexity](https://perplexity.ai/) (5) · [Phala](https://redpill.ai/) (18) · [Poolside](https://poolside.ai/) (2) · [PrimaLabs](https://openrouter.ai/provider/primalabs) · [PrimeIntellect](https://openrouter.ai/provider/prime-intellect) (8) · [Quiver](https://openrouter.ai/provider/quiver) · [Recraft](https://openrouter.ai/provider/recraft) · [Recursive](https://recursive.com/) · [Reka](https://reka.ai/) (9) · [Relace](https://www.relace.ai/) (13) · [Respan](https://respan.ai/) · [Runway](https://runwayml.com/) · [Sail Research](https://www.sailresearch.com/) (8) · [Sakana AI](https://sakana.ai/) (4) · [SambaNova](https://sambanova.ai/) (6) · [ScaleDown](https://scaledown.ai/) (2) · [Seed](https://byteplus.com/) (6) · [SiliconFlow](https://siliconflow.com/) (41) · [Sourceful](https://www.sourceful.com/) · [Stealth](https://openrouter.ai/) · [StepFun](https://stepfun.ai/) (2) · [StreamLake](https://www.streamlake.ai/) (19) · [Switchpoint](https://openrouter.ai/provider/switchpoint) · [Tencent](https://www.tencentcloud.com/) (5) · [Tenstorrent](https://tenstorrent.com/) (3) · [Thinking Machines](https://thinkingmachines.ai/) · [Together](https://www.together.ai/) (17) · [TypeSafe](https://typesafe.ai/) · [Unbiased](https://unbiased.ai/) (2) · [Upstage](https://www.upstage.ai/) (2) · [Venice](https://venice.ai/) (37) · [VoyageAI by MongoDB](https://www.voyageai.com/) · [Wafer](https://www.wafer.ai/) (10) · [xAI](https://x.ai/) (7) · [Xiaomi](https://platform.xiaomimimo.com/) (3) · [Z.AI](https://z.ai/) (14)

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
