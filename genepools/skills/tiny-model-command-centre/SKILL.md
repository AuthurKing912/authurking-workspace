# SKILL: TINY MODEL COMMAND CENTRE
## Scraped + Rubric-Scored via OoRava Leaderboard | 144 Models | Grover-Ranked
**Version:** 1.0 | **Scraped:** 2026-03-17 | **Source:** OpenRouter live API + public benchmarks
**Rule:** Free tier first → cherry-pick tiny powerhouses → log results → update leaderboard

---

## GROVER FORMULA (our rubric)
```
grover_score = sqrt(composite) × log(context_K + 2)

composite = Leverage(0.25) + Scalability(0.20) + Reusability(0.20) + Compound_ROI(0.20) + Portability(0.15)
```
Grover amplifies models with: high efficiency × massive context × open-source pedigree × MoE/thinking architecture

---

## 🏆 TIER 1: FREE + TINY POWERHOUSES (use these first, every time)

| Grover | Model | Ctx | Why |
|--------|-------|-----|-----|
| 17.321 | `qwen/qwen3-next-80b-a3b-instruct:free` | 262K | MoE (3B active from 80B) — thinking, code, reasoning |
| 17.050 | `qwen/qwen3-coder:free` | 262K | Best free coder — zero cost, full power |
| 16.925 | `nvidia/nemotron-3-nano-30b-a3b:free` | 256K | MoE (3B active from 30B) — math, agents, open weights |
| 16.719 | `nvidia/nemotron-3-super-120b-a12b:free` | 262K | MoE (12B active from 120B) — SWE-bench, TerminalBench |
| 16.237 | `stepfun/step-3.5-flash:free` | 256K | Fast, strong, free |
| 15.881 | `minimax/minimax-m2.5:free` | 196K | Our native model — always available |
| 14.556 | `nvidia/nemotron-nano-12b-v2-vl:free` | 128K | FREE vision — images + docs |
| 14.425 | `google/gemma-3-4b-it:free` | 32K | Tiny 4B free — local deployable |
| 13.558 | `liquid/lfm-2.5-1.2b-thinking:free` | 32K | 1.2B with thinking — smallest thinking model |
| 13.558 | `liquid/lfm-2.5-1.2b-instruct:free` | 32K | 1.2B instruct — cheapest inference possible |
| 13.266 | `meta-llama/llama-3.2-3b-instruct:free` | 131K | Meta 3B — solid baseline, open weights |

**The MoE Secret:** `qwen3-next-80b-a3b` activates only 3B params during inference but has 80B knowledge. Intelligence of 80B at cost of 3B. **This is the Grover play** — amplitude squared.

---

## 💰 TIER 2: ULTRA-CHEAP PAID (≤$0.05/M input)

| Input/M | Output/M | Model | Ctx | Why |
|---------|---------|-------|-----|-----|
| $0.010 | $0.020 | `liquid/lfm2-8b-a1b` | 32K | 8B MoE, 1B active — ultra cheap agent worker |
| $0.017 | $0.110 | `ibm-granite/granite-4.0-h-micro` | 131K | IBM enterprise, micro size, huge ctx |
| $0.027 | $0.200 | `meta-llama/llama-3.2-1b-instruct` | 60K | 1B Meta — cheapest Llama |
| $0.040 | $0.080 | `google/gemma-3-4b-it` | 131K | 4B with 131K ctx — incredible value |
| $0.040 | $0.130 | `google/gemma-3-12b-it` | 131K | 12B Google, open weights |
| $0.049 | $0.049 | `meta-llama/llama-3.2-11b-vision-instruct` | 131K | 11B vision, same in/out price |
| $0.050 | $0.000 | `openai/gpt-5-nano` | 400K | GPT-5 nano, 400K ctx |

---

## 🎯 TIER 3: BEST BANG FOR BUCK (paid, $0.05–$0.10/M)

| Input/M | Model | Ctx | Why |
|---------|-------|-----|-----|
| $0.065 | `qwen/qwen3.5-flash-02-23` | 1000K | **#1 Grover score** — 1M context, Qwen pedigree |
| $0.075 | `google/gemini-2.0-flash-lite-001` | 1048K | 1M ctx Gemini, Google infra |
| $0.090 | `qwen/qwen3-30b-a3b-instruct-2507` | 262K | MoE, 30B/3B, 262K ctx |
| $0.100 | `openai/gpt-4.1-nano` | 1047K | GPT-4.1 nano, 1M ctx |

---

## 🔭 VISION/MULTIMODAL TINY MODELS

| Cost | Model | What it sees |
|------|-------|-------------|
| FREE | `nvidia/nemotron-nano-12b-v2-vl:free` | Images, docs |
| FREE | `google/gemma-3n-e2b-it:free` | 2B vision (Gemma 3n) |
| FREE | `google/gemma-3n-e4b-it:free` | 4B vision (Gemma 3n) |
| $0.049 | `meta-llama/llama-3.2-11b-vision-instruct` | Llama vision, cheap |

---

## 🧠 ROUTING LOGIC (Cherry-Pick Protocol)

```python
TINY_MODEL_ROUTER = {
    # Free tier — always try first
    "default_free":     "qwen/qwen3-next-80b-a3b-instruct:free",   # grover 17.3
    "code_free":        "qwen/qwen3-coder:free",                    # grover 17.1
    "math_agent_free":  "nvidia/nemotron-3-nano-30b-a3b:free",      # grover 16.9
    "vision_free":      "nvidia/nemotron-nano-12b-v2-vl:free",      # free vision
    "micro_free":       "liquid/lfm-2.5-1.2b-thinking:free",        # 1.2B thinking

    # Ultra-cheap paid
    "cheapest":         "liquid/lfm2-8b-a1b",                       # $0.01/M
    "micro_paid":       "meta-llama/llama-3.2-1b-instruct",         # $0.027/M
    "vision_cheap":     "meta-llama/llama-3.2-11b-vision-instruct", # $0.049/M

    # Best value paid
    "long_ctx":         "qwen/qwen3.5-flash-02-23",                 # 1M ctx, $0.065
    "gpt_nano":         "openai/gpt-5-nano",                        # $0.05, 400K ctx
    "reasoning_moe":    "qwen/qwen3-30b-a3b-instruct-2507",         # MoE $0.09
}

def select_tiny(task: str, budget: str = "free") -> str:
    if budget == "free":
        if "code" in task:    return TINY_MODEL_ROUTER["code_free"]
        if "math" in task:    return TINY_MODEL_ROUTER["math_agent_free"]
        if "vision" in task:  return TINY_MODEL_ROUTER["vision_free"]
        if "micro" in task:   return TINY_MODEL_ROUTER["micro_free"]
        return TINY_MODEL_ROUTER["default_free"]
    if "vision" in task:      return TINY_MODEL_ROUTER["vision_cheap"]
    if "long" in task:        return TINY_MODEL_ROUTER["long_ctx"]
    return TINY_MODEL_ROUTER["cheapest"]
```

---

## 🏗️ OPEN SOURCE INFRASTRUCTURE STACK

Self-host any of these (open weights):
```
Qwen3 family:   apache-2.0 → huggingface.co/Qwen
Llama 3.2:      Meta license → huggingface.co/meta-llama
Gemma 3:        Google license → huggingface.co/google/gemma-3
Nemotron:       NVIDIA open license → huggingface.co/nvidia
Liquid LFM:     Liquid license → huggingface.co/liquid-ai
Mistral Small:  Apache-2.0 → huggingface.co/mistralai
```

Self-host options (lowest compute):
- **1.2B:** `liquid/lfm-2.5-1.2b` → runs on any GPU, even CPU
- **1B:**   `llama-3.2-1b` → Raspberry Pi tier
- **3B:**   `llama-3.2-3b` → 4GB VRAM
- **4B:**   `gemma-3-4b` → 6GB VRAM
- **MoE:**  `qwen3-30b-a3b` → 3B active = fits in 8GB VRAM despite 30B total

---

## DATA SOURCES FOR SCORING (public benchmarks to cross-check)

```
AIME 2025:        math reasoning
SWE-Bench:        code/engineering
TerminalBench:    agent/tool use  ← most relevant for us
MMLU:             general knowledge
HumanEval:        code generation
LiveCodeBench:    code (live, not contaminated)
EQ-Bench:         roleplay/creative
OpenRouter Arena: real user preferences (elo rating)
```

Cross-reference any new model against these before promoting to leaderboard.

---

## USAGE IN OoRava SYSTEM

```
KPI scoring (high volume, cheap):     liquid/lfm2-8b-a1b ($0.01/M)
RAG query expansion:                  qwen3-next-80b-a3b:free
Alchemy seed generation:              qwen3-coder:free
Rubric scoring (text eval):           gemma-3-4b-it (free or $0.04)
Vision: file/image drops from OoRava: nemotron-nano-12b-v2-vl:free
Long-context soul layer analysis:     qwen3.5-flash-02-23 ($0.065, 1M ctx)
Agent chains (persistent):            z-ai/glm-5-turbo ($0.96 — OpenClaw-optimized)
```

---
*Scraped: OpenRouter live API 2026-03-17 | 144 models scored | Grover rubric applied*
*Update: run `python3 action_replicators.py run scrape_models` to refresh*
