# Model Router - ROI-First Model Selection
Version: 0.1 | ROI: Max | Cost: Zero tokens

## Rules (Hard Limits)
- Text-to-Image: wan2.6 ALWAYS
- Image-to-Video: kling-v3-pro ALWAYS
- TTS: TTS Kitty ALWAYS

## Selection Logic by Task
- Heavy reasoning/research: Kimi-K2 or minimax-text-01
- Code generation: CodeQuest (tiny, cheap, excellent)
- Fast summarization: smallest model that passes rubric
- Vision tasks: GLM-Z1 or minimax-text-01
- Default fallback: current configured default

## Priority Order
1. Does task have a hard rule? Use it.
2. Check rubric leaderboard for task type - use top ROI model
3. If no data: use bridge tier default
4. Log result to leaderboard for future routing

## OpenRouter Models Prioritized
- kimi-k2: moonshot/moonshot-v1-128k (check openrouter slug)
- GLM-Z1: thudm/glm-z1-32b (check openrouter)
- CodeQuest: use best tiny coding model on openrouter <7B params
- TTS Kitty: check openrouter audio models
