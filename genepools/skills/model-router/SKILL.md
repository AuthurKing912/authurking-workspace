# SKILL: MODEL ROUTER — ROI-First Model Selection
## Updated: 2026-03-17 | New models ingested from OoRava feed
**Version:** 2.0 | **Rule:** Free tier first → Bridge → Specialist | NEVER guess slugs

---

## HARD LIMITS (NEVER override)
- Text-to-Image: **wan2.6** ALWAYS
- Image-to-Video: **kling-v3-pro** ALWAYS
- TTS: **TTS Kitty** ALWAYS
- API keys: **.env ONLY** — never in tracked files

---

## MODEL REGISTRY (current, OpenRouter-verified)

### 🆓 FREE TIER (ROI: ∞ — use first, always)
| Model | Slug | Context | Best For |
|-------|------|---------|----------|
| Hunter Alpha | `openrouter/hunter-alpha` | 1.05M | Long-horizon planning, agentic, multi-step |
| Healer Alpha | `openrouter/healer-alpha` | 262K | Vision + audio + reasoning, omni-modal |
| NVIDIA Nemotron 3 Super | `nvidia/nemotron-3-super-120b-a12b:free` | 262K | Code, math, multi-agent (MoE, 1M ctx) |
| minimax/minimax-m2.5:free | `minimax/minimax-m2.5:free` | 200K | General default, fast |
| qwen/qwen3-next-80b:free | `qwen/qwen3-next-80b-a3b-instruct:free` | 128K | Reasoning, code, Chinese |
| openai/gpt-oss-120b:free | `openai/gpt-oss-120b:free` | 128K | General fallback |

### 💰 BRIDGE TIER (use when free insufficient)
| Model | Slug | Cost (in/out per M) | Best For |
|-------|------|---------------------|----------|
| GLM-5 Turbo | `z-ai/glm-5-turbo` | $0.96/$3.20 | Agent chains, long execution, OpenClaw |
| ByteDance Seed 2.0 Lite | `bytedance-seed/seed-2-lite` | $0.25/$2.00 | Multimodal, production, low latency |
| Qwen3.5-9B | `qwen/qwen3-5-9b` | $0.05/$0.15 | Fast, cheap, vision + text |
| moonshotai/kimi-k2.5 | `moonshotai/kimi-k2.5` | $0.45/$2.20 | Reasoning, complex tasks |
| minimax/minimax-m2.5 | `minimax/minimax-m2.5` | bridge | General |

### 🎯 SPECIALIST TIER
| Model | Slug | Best For |
|-------|------|----------|
| qwen3-coder-next | `qwen/qwen3-coder-next` | Code generation ONLY |
| z-ai/glm-4.7-flash | `z-ai/glm-4.7-flash` | Ultra-fast cheap responses |

---

## ROUTING LOGIC (Grover-optimized)

```python
def select_model(task_type: str, budget: str = "free") -> str:
    """ROI-first model selection. Free tier always tried first."""

    FREE_MODELS = [
        "openrouter/hunter-alpha",        # 1M ctx, $0, best for agents
        "openrouter/healer-alpha",         # omni-modal, $0
        "nvidia/nemotron-3-super-120b-a12b:free",  # code/math
        "minimax/minimax-m2.5:free",
        "qwen/qwen3-next-80b-a3b-instruct:free",
        "openai/gpt-oss-120b:free",
    ]

    TASK_ROUTING = {
        "agent_chain":      "z-ai/glm-5-turbo",          # best for OpenClaw agents
        "reasoning":        "moonshotai/kimi-k2.5",
        "code":             "qwen/qwen3-coder-next",
        "vision":           "openrouter/healer-alpha",    # omni-modal
        "long_context":     "openrouter/hunter-alpha",    # 1M ctx
        "fast_cheap":       "qwen/qwen3-5-9b",           # $0.05/M
        "ultra_fast":       "z-ai/glm-4.7-flash",
        "multimodal":       "bytedance-seed/seed-2-lite",
        "general":          "minimax/minimax-m2.5:free",
    }

    if budget == "free":
        return FREE_MODELS[0]  # Hunter Alpha — 1M ctx, $0, agent-optimized
    return TASK_ROUTING.get(task_type, "minimax/minimax-m2.5:free")
```

---

## PRIORITY DECISION TREE

```
TASK ARRIVES
  ↓
Is it a hard-limit task? (T2I/I2V/TTS) → use hard limit, done
  ↓
Does it need vision/audio? → openrouter/healer-alpha (free)
  ↓
Is it an agent chain / long execution? → z-ai/glm-5-turbo ($0.96/M)
  ↓
Does it need 1M+ context? → openrouter/hunter-alpha (FREE)
  ↓
Is it code? → qwen/qwen3-coder-next
  ↓
Is budget free? → try Hunter Alpha → fallback minimax-m2.5:free
  ↓
Need speed + cheap? → qwen/qwen3-5-9b ($0.05/M) or glm-4.7-flash
  ↓
General reasoning? → kimi-k2.5 ($0.45/M)
```

---

## KEY INSIGHTS FROM THIS FEED

**Hunter Alpha & Healer Alpha** (by OpenRouter, $0):
- 1T+ params, 1M context, $0 — the highest ROI free models available
- NOTE: "All prompts logged by provider" — do NOT send private soul data, keys, or sensitive OoRava personal info through these models
- Use for: public-facing content generation, code, research, leaderboard analysis

**GLM-5 Turbo** (Z.ai, $0.96/$3.20):
- Specifically optimized for OpenClaw agent scenarios
- Best choice for long execution chains within this system
- 203K context — sufficient for most tasks

**Nemotron 3 Super** (NVIDIA, $0):
- 1M context, MoE architecture (12B active params from 120B total)
- Best for: complex multi-agent tasks, coding, math
- Fully open weights — can self-host eventually

**ByteDance Seed 2.0 Lite** ($0.25/$2.00):
- Low latency = best for real-time Telegram response chains
- Vision + tools = good for processing OoRava's image/doc drops

**Qwen3.5-9B** ($0.05/$0.15):
- Cheapest option with vision
- Use for: quick classifications, rubric scoring, KPI tagging

---

## SECURITY NOTE FOR FREE MODELS

Hunter Alpha + Healer Alpha log all prompts. Router rule:
- ✅ Safe to use: code gen, leaderboard queries, content, public skill.mds
- ❌ Never use: soul files, personal data, API keys, OoRava private context

---
*Model Router v2.0 | Updated 2026-03-17 | AuthurKing × OoRava | As new models arrive → update this file*
