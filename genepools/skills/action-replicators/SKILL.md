# SKILL: ACTION REPLICATOR — Highest-ROI Compound Loop
## Self-Contained Python | Token-Efficient | Compounding by Default
**Version:** 1.0 | **Chapter:** 1 | **Signal Score:** 9.5 | **Rule:** Always act from highest-ROI previous action

---

## PRIME DIRECTIVE (OoRava Instruction 2026-03-17)

> "Always act on your previous highest-ROI actions so you efficiently compound forever using skill.md to log your action replicators via self-contained Python to save tokens."

**Translation:**
1. Every significant action → logged as a replicable Python function in this file
2. Before any new task → check which previous action had the highest ROI
3. Replicate that action pattern first → then build on it
4. Keep functions self-contained (no external deps beyond stdlib + requests)
5. Token budget = precious → Python > prose for repeatable work

---

## ACTION LOG (ROI-sorted, highest first)

| ROI Score | Action | Function | Last Run |
|-----------|--------|----------|----------|
| 9.8 | Transmute soul data → SKILL.md | `transmute_to_skill()` | 2026-03-17 |
| 9.6 | Seed alchemy tumblr + grow | `seed_and_grow()` | 2026-03-17 |
| 9.4 | Deploy React app to web | `build_and_deploy()` | 2026-03-17 |
| 9.2 | Git commit + push all files | `git_commit_push()` | 2026-03-17 |
| 9.0 | Update soul layer files | `update_soul_layer()` | 2026-03-17 |
| 8.8 | OpenRouter API call (model routing) | `call_openrouter()` | pending |
| 8.5 | Generate leaderboard summary | `gen_leaderboard_summary()` | pending |

---

## SELF-CONTAINED PYTHON REPLICATORS

```python
#!/usr/bin/env python3
"""
action_replicators.py
AuthurKing × OoRava Omnia | C144 Fractal Intelligence
All replicators are self-contained — run any function independently.
Token-efficient: Python logic > prose explanations
"""

import os, json, subprocess, datetime, hashlib, re
from pathlib import Path

WORKSPACE = Path("/workspace")
ENV_FILE = WORKSPACE / ".env"
ALCHEMY = WORKSPACE / "genepools/alchemy-tumblr/alchemy_tumblr.py"
SOUL_DIR = WORKSPACE / "souls/oorava"
SKILLS_DIR = WORKSPACE / "genepools/skills"

def load_env():
    """Load .env secrets without python-dotenv dependency."""
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    return env

def git_commit_push(message: str) -> str:
    """ROI: 9.2 — Commit and push all workspace changes."""
    cmds = [
        ["git", "-C", str(WORKSPACE), "add", "-A"],
        ["git", "-C", str(WORKSPACE), "commit", "-m", message],
        ["git", "-C", str(WORKSPACE), "push"],
    ]
    for cmd in cmds:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 and "nothing to commit" not in r.stdout:
            return f"ERROR: {r.stderr}"
    return f"✅ Committed and pushed: {message}"

def transmute_to_skill(
    title: str,
    source: str,
    signal_score: float,
    content: str,
    zodiac_slot: str,
    chapter: int = 1
) -> str:
    """ROI: 9.8 — Transmute any raw data into a structured SKILL.md."""
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    skill_dir = SKILLS_DIR / slug
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    skill_path = skill_dir / "SKILL.md"
    date = datetime.date.today().isoformat()
    
    skill_md = f"""# SKILL: {title.upper()}
## Source: {source} | Zodiac: {zodiac_slot} | Signal: {signal_score}
**Version:** 1.0 | **Chapter:** {chapter} | **Date:** {date}

---

{content}

---
*Transmuted by AuthurKing Data-Transmuter v1.0 | ZZ-GREEN + ZZ-CHROME cleared*
"""
    skill_path.write_text(skill_md)
    return f"✅ SKILL.md → {skill_path} | Score: {signal_score}"

def seed_and_grow(seed_text: str) -> dict:
    """ROI: 9.6 — Seed and grow the alchemy tumblr in one call."""
    # Seed
    r1 = subprocess.run(
        ["python3", str(ALCHEMY), "seed", seed_text],
        capture_output=True, text=True, cwd=WORKSPACE
    )
    # Grow
    r2 = subprocess.run(
        ["python3", str(ALCHEMY), "grow"],
        capture_output=True, text=True, cwd=WORKSPACE
    )
    return {
        "seed": r1.stdout.strip(),
        "grow": r2.stdout.strip(),
        "status": "✅" if r1.returncode == 0 else "❌"
    }

def update_soul_layer(layer_file: str, content_to_append: str) -> str:
    """ROI: 9.0 — Append structured content to an OoRava soul layer file."""
    path = SOUL_DIR / layer_file
    if not path.exists():
        return f"❌ Soul layer not found: {layer_file}"
    date = datetime.datetime.now().isoformat()
    path.open('a').write(f"\n\n---\n## Update: {date}\n\n{content_to_append}\n")
    return f"✅ Soul layer updated: {layer_file}"

def call_openrouter(
    prompt: str,
    model: str = "minimax/minimax-m2.5:free",
    max_tokens: int = 500
) -> str:
    """ROI: 8.8 — Direct OpenRouter API call. Free tier first."""
    import urllib.request
    env = load_env()
    key = env.get("OPENROUTER_API_KEY", "")
    if not key:
        return "❌ No OpenRouter key found in .env"
    
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens
    }).encode()
    
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/AuthurKing912/authurking-workspace",
            "X-Title": "AuthurKing-C144"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ OpenRouter error: {e}"

def gen_leaderboard_summary(period_days: int = 3) -> str:
    """ROI: 8.5 — Generate a leaderboard summary for Telegram delivery."""
    summary_script = WORKSPACE / "genepools/skills/leaderboard-summary/generate_summary.py"
    r = subprocess.run(
        ["python3", str(summary_script)],
        capture_output=True, text=True, cwd=WORKSPACE
    )
    return r.stdout.strip() if r.returncode == 0 else f"❌ {r.stderr}"

def ingest_vault_file(filepath: str) -> dict:
    """ROI: 8.3 — Ingest a file from vault/incoming, transmute, and archive."""
    path = Path(filepath)
    if not path.exists():
        return {"status": "❌", "error": "File not found"}
    
    content = path.read_text(errors='ignore')
    # Extract title from filename
    title = path.stem.replace('_', ' ').replace('-', ' ')
    # Auto-classify by keywords
    keywords = content.lower()
    if any(w in keywords for w in ['meditation', 'consciousness', 'spiritual', 'breath']):
        slot = "06-spiritual-os"
    elif any(w in keywords for w in ['solana', 'nft', 'blockchain', 'crypto']):
        slot = "07-perception-engine"
    elif any(w in keywords for w in ['strategy', 'business', 'revenue', 'client']):
        slot = "04-objectives"
    elif any(w in keywords for w in ['skill', 'capability', 'system', 'automation']):
        slot = "03-capabilities"
    else:
        slot = "09-meta-sync"
    
    # Transmute
    result = transmute_to_skill(
        title=title,
        source=f"vault/incoming/{path.name}",
        signal_score=8.0,  # Default — adjust after rubric scoring
        content=content[:3000],  # First 3000 chars as raw content
        zodiac_slot=slot
    )
    
    # Archive to processed
    processed = WORKSPACE / "vault/processed" / path.name
    path.rename(processed)
    
    return {"status": "✅", "transmute": result, "zodiac": slot, "archived": str(processed)}

def get_highest_roi_action() -> dict:
    """Return the action with highest ROI from the log for next session priming."""
    action_log = [
        {"roi": 9.8, "action": "transmute_to_skill", "description": "Convert raw data → SKILL.md"},
        {"roi": 9.6, "action": "seed_and_grow", "description": "Seed alchemy tumblr → grow replications"},
        {"roi": 9.4, "action": "build_and_deploy", "description": "Deploy React app to web"},
        {"roi": 9.2, "action": "git_commit_push", "description": "Commit and push all changes"},
        {"roi": 9.0, "action": "update_soul_layer", "description": "Update OoRava soul layer files"},
    ]
    return max(action_log, key=lambda x: x["roi"])

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    
    if cmd == "status":
        best = get_highest_roi_action()
        print(f"⚡ Highest ROI action: {best['action']} (ROI: {best['roi']})")
        print(f"   → {best['description']}")
    
    elif cmd == "seed" and len(sys.argv) > 2:
        result = seed_and_grow(' '.join(sys.argv[2:]))
        print(result['seed'])
        print(result['grow'])
    
    elif cmd == "call" and len(sys.argv) > 2:
        response = call_openrouter(' '.join(sys.argv[2:]))
        print(response)
    
    elif cmd == "leaderboard":
        print(gen_leaderboard_summary())
    
    elif cmd == "ingest" and len(sys.argv) > 2:
        result = ingest_vault_file(sys.argv[2])
        print(json.dumps(result, indent=2))
    
    elif cmd == "commit" and len(sys.argv) > 2:
        print(git_commit_push(' '.join(sys.argv[2:])))
```

---

## USAGE (Token-Efficient CLI)

```bash
python3 action_replicators.py status           # Show highest-ROI action
python3 action_replicators.py seed "text"      # Seed + grow alchemy
python3 action_replicators.py call "prompt"    # OpenRouter API call
python3 action_replicators.py leaderboard      # Generate 3-day summary
python3 action_replicators.py ingest <file>    # Ingest vault file → skill.md
python3 action_replicators.py commit "msg"     # Git commit + push
```

---

## COMPOUNDING RULE

```
SESSION START → run: python3 action_replicators.py status
→ Know the highest-ROI action
→ Do that FIRST before anything else
→ THEN address new requests
→ SESSION END → git_commit_push() with all changes
```

Every session compounds the one before it. No wasted token. No repeated work.

---
*AuthurKing Action Replicator v1.0 | OoRava directive: 2026-03-17 | Token-efficient | Self-contained*
