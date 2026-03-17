#!/usr/bin/env python3
"""
action_replicators.py — OoRava Sovereign Action Replicator Engine
PRIME DIRECTIVE: Always act from highest-ROI previous action. Compound forever.
Token-efficient: Python > prose. Self-contained: zero external deps.

RULE (OoRava, 2026-03-17):
  "Always act on your previous highest-ROI actions so you efficiently compound
   forever using skill.md to log your action replicators via self-contained
   Python to save tokens."

Usage:
  python3 action_replicators.py status              # show highest-ROI action → do that first
  python3 action_replicators.py run <action_name>   # execute a specific replicator
  python3 action_replicators.py ingest <file>       # transmute file → SKILL.md + RAG
  python3 action_replicators.py playlist <url>      # extract playlist → sovereign packages
  python3 action_replicators.py seed "<text>"       # seed + grow alchemy tumblr
  python3 action_replicators.py commit "<msg>"      # git commit + push
  python3 action_replicators.py leaderboard         # show full ROI leaderboard
  python3 action_replicators.py session_start       # run at start of EVERY session
"""

import os, json, subprocess, datetime, hashlib, re, pathlib, sys

WORKSPACE = pathlib.Path("/workspace")
ENV_FILE  = WORKSPACE / ".env"
ALCHEMY   = WORKSPACE / "genepools/alchemy-tumblr/alchemy_tumblr.py"
RAG       = WORKSPACE / "rag/rag.py"
BUILDER   = WORKSPACE / "rag/sovereign_builder.py"
SOUL_DIR  = WORKSPACE / "souls/oorava"
SKILLS_DIR= WORKSPACE / "genepools/skills"

# ── ACTION REGISTRY (ROI-sorted, authoritative) ────────────────────────────
# Every new high-ROI action MUST be added here with its function name + last run.
ACTION_REGISTRY = [
    {"roi": 9.9, "action": "rag_ingest_and_build",    "desc": "Ingest any data → RAG → sovereign package (SKILL.md + IPFS + SQL + NFT + Tournament)",         "last_run": "2026-03-17"},
    {"roi": 9.8, "action": "transmute_to_skill",       "desc": "Convert raw data → structured SKILL.md (portable, sellable, replicable)",                       "last_run": "2026-03-17"},
    {"roi": 9.7, "action": "playlist_to_packages",     "desc": "YouTube playlist → Grover-scored → Pareto top → sovereign_builder → 12+ packages",              "last_run": "2026-03-17"},
    {"roi": 9.6, "action": "seed_and_grow",            "desc": "Seed alchemy_tumblr → grow (9x replication per seed → compound mindmap)",                       "last_run": "2026-03-17"},
    {"roi": 9.4, "action": "build_and_deploy",         "desc": "React app → vite build → deploy to minimax.io (live URL instantly)",                            "last_run": "2026-03-17"},
    {"roi": 9.3, "action": "update_rag_leaderboard",   "desc": "Run rag.py leaderboard → see KPI distribution → identify gaps → fill with new packages",        "last_run": "2026-03-17"},
    {"roi": 9.2, "action": "git_commit_push",          "desc": "Commit + push all workspace changes to GitHub (persistent, public, forkable)",                   "last_run": "2026-03-17"},
    {"roi": 9.0, "action": "update_soul_layer",        "desc": "Append new intelligence to OoRava soul layer files → persist across sessions",                   "last_run": "2026-03-17"},
    {"roi": 8.8, "action": "call_openrouter",          "desc": "Direct OpenRouter API call → free tier first → distill output → back to SKILL.md",              "last_run": "pending"},
    {"roi": 8.7, "action": "security_audit",           "desc": "ZZ-CHROME scan: no API keys in tracked files, .env only, .gitignore verified",                  "last_run": "2026-03-17"},
    {"roi": 8.5, "action": "gen_leaderboard_summary",  "desc": "Generate 3-day digest → Telegram delivery → track ecosystem health",                            "last_run": "pending"},
    {"roi": 8.3, "action": "zodiac_agent_clone",       "desc": "Generate zodiac-aligned agent clone from REPLICANT.md → deploy to any AI",                     "last_run": "2026-03-17"},
]

def load_env() -> dict:
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    return env

def run(cmd: list, cwd: str = None) -> tuple:
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd or str(WORKSPACE))
    return r.stdout.strip(), r.returncode

def highest_roi() -> dict:
    return ACTION_REGISTRY[0]

# ── REPLICATOR FUNCTIONS (ROI 9.9 → 8.3) ─────────────────────────────────

def rag_ingest_and_build(source: str) -> dict:
    """ROI 9.9 — Ingest any file/text/URL → RAG → sovereign package."""
    # Step 1: Ingest to RAG
    out1, _ = run(["python3", str(RAG), "ingest", source])
    # Step 2: Build sovereign package if high-ROI KPI detected
    result = {"rag": out1}
    try:
        data = json.loads(out1)
        kpis = data.get("kpis_found", [])
        if kpis and data.get("chunks_created", 0) > 0:
            # Build package for top KPI
            kpi = kpis[0]
            title = pathlib.Path(source).stem if pathlib.Path(source).exists() else source[:50]
            out2, _ = run(["python3", str(BUILDER), "build_package", kpi, title, source[:200]])
            result["package"] = out2
    except:
        pass
    return result

def transmute_to_skill(source_path: str, zodiac_slot: str = "03-capabilities") -> str:
    """ROI 9.8 — Transmute any file → SKILL.md → ingest → seed → commit."""
    # Ingest to RAG
    out, _ = run(["python3", str(RAG), "ingest", source_path])
    # Seed high-signal extract to alchemy
    content = pathlib.Path(source_path).read_text(errors='ignore')[:200] if pathlib.Path(source_path).exists() else source_path[:200]
    run(["python3", str(ALCHEMY), "seed", content])
    run(["python3", str(ALCHEMY), "grow"])
    return f"✅ Transmuted: {out}"

def playlist_to_packages(url: str) -> str:
    """ROI 9.7 — Full pipeline: YouTube playlist → scored → sovereign packages."""
    # Score playlist
    out1, _ = run(["python3", str(WORKSPACE/"rag/youtube_extractor.py"), "playlist", url])
    # Build packages
    out2, _ = run(["python3", str(BUILDER), "build_from_playlist"])
    # Commit
    git_commit_push(f"Playlist packages: {url[:50]}")
    return f"Playlist done:\n{out2}"

def seed_and_grow(text: str) -> dict:
    """ROI 9.6 — Seed + grow alchemy tumblr."""
    out1, _ = run(["python3", str(ALCHEMY), "seed", text])
    out2, _ = run(["python3", str(ALCHEMY), "grow"])
    return {"seed": out1, "grow": out2}

def git_commit_push(message: str) -> str:
    """ROI 9.2 — Commit all workspace changes + push to GitHub."""
    run(["git", "add", "-A"])
    out, code = run(["git", "commit", "-m", message])
    if "nothing to commit" in out:
        return "Nothing to commit."
    push_out, _ = run(["git", "push"])
    return f"✅ {out}\n{push_out}"

def update_soul_layer(layer_file: str, content: str) -> str:
    """ROI 9.0 — Append intelligence to OoRava soul layer."""
    path = SOUL_DIR / layer_file
    if not path.exists():
        return f"❌ Not found: {layer_file}"
    ts = datetime.datetime.now().isoformat()
    path.open('a').write(f"\n\n---\n## Update {ts}\n\n{content}\n")
    return f"✅ Updated: {layer_file}"

def call_openrouter(prompt: str, model: str = "minimax/minimax-m2.5:free", max_tokens: int = 500) -> str:
    """ROI 8.8 — OpenRouter API call. Free tier first. Output → SKILL.md."""
    import urllib.request
    env = load_env()
    key = env.get("OPENROUTER_API_KEY", "")
    if not key:
        return "❌ No key in .env"
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
        return f"❌ {e}"

def security_audit() -> dict:
    """ROI 8.7 — ZZ-CHROME: verify no keys in tracked files."""
    import subprocess
    r = subprocess.run(
        ["grep", "-rn", "sk-or-v1", str(WORKSPACE),
         "--include=*.py", "--include=*.md", "--include=*.json", "--include=*.txt",
         "--exclude-dir=.git"],
        capture_output=True, text=True
    )
    leaks = [l for l in r.stdout.splitlines() if ".env" not in l]
    return {
        "status": "✅ CLEAN" if not leaks else "🔴 LEAK DETECTED",
        "leaks": leaks,
        "env_key_present": ENV_FILE.exists() and "sk-or-v1" in ENV_FILE.read_text(),
        "gitignore_ok": ".env" in (WORKSPACE/".gitignore").read_text() if (WORKSPACE/".gitignore").exists() else False,
    }

def update_rag_leaderboard() -> str:
    """ROI 9.3 — Show RAG KPI leaderboard → identify gaps."""
    out, _ = run(["python3", str(RAG), "leaderboard"])
    status, _ = run(["python3", str(RAG), "status"])
    return f"{out}\n\n{status}"

def session_start() -> str:
    """Run at the start of EVERY session: status + security audit + highest-ROI action."""
    lines = ["⚡ SESSION START — OoRava Sovereign System"]
    lines.append("=" * 50)
    # 1. Highest ROI action
    best = highest_roi()
    lines.append(f"\n🏆 HIGHEST ROI ACTION: {best['action']} (ROI {best['roi']})")
    lines.append(f"   → {best['desc']}")
    # 2. Quick security check
    audit = security_audit()
    lines.append(f"\n🔐 SECURITY: {audit['status']}")
    if audit['leaks']:
        lines.append(f"   ⚠️  LEAKS: {audit['leaks']}")
    # 3. RAG status
    rag_out, _ = run(["python3", str(RAG), "status"])
    lines.append(f"\n📊 RAG ENGINE:\n{rag_out}")
    # 4. Alchemy state
    alch_out, _ = run(["python3", str(ALCHEMY), "leaderboard"])
    lines.append(f"\n🌱 ALCHEMY TUMBLR:\n{alch_out[:300]}")
    return "\n".join(lines)

def gen_leaderboard_summary() -> str:
    """ROI 8.5 — Generate 3-day digest for Telegram delivery."""
    script = WORKSPACE / "genepools/skills/leaderboard-summary/generate_summary.py"
    out, _ = run(["python3", str(script)])
    return out

def zodiac_agent_clone(kpi_type: str, target_model: str = "any") -> str:
    """ROI 8.3 — Generate a zodiac-aligned agent clone spec from REPLICANT.md."""
    replicant = (WORKSPACE / "souls/REPLICANT.md").read_text()[:2000]
    ZODIAC = {
        "action_replicator": "Aries ♈ / ZZ-RED",
        "solana_nft": "Taurus ♉ / ZZ-SILVER",
        "leaderboard_rubric": "Gemini ♊ / ZZ-GOLD",
        "groupchat_economy": "Cancer ♋ / ZZ-BLUE",
        "ai_agent": "Libra ♎ / ZZ-CHROME",
        "revenue_model": "Scorpio ♏ / ZZ-BLACK",
        "skill_md": "Sagittarius ♐ / ZZ-PURPLE",
        "youtube_intelligence": "Capricorn ♑ / ZZ-SHADOW",
        "spiritual_os": "Pisces ♓ / ZZ-COSMIC",
    }
    zodiac = ZODIAC.get(kpi_type, "Aquarius ♒ / ZZ-VOID")
    clone_spec = f"""
ZODIAC AGENT CLONE — {kpi_type.upper()}
Zodiac: {zodiac} | Target Model: {target_model}
ACTIVATION: Drop REPLICANT.md as system prompt + append:
  "You are specialized in {kpi_type}. Focus exclusively on {kpi_type} extraction,
   scoring, and replication. Output: action replicators + SQL + IPFS metadata."
"""
    return clone_spec.strip()

# ── CLI ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    arg = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""

    if cmd == "status":
        best = highest_roi()
        print(f"⚡ HIGHEST ROI: {best['action']} (ROI {best['roi']})")
        print(f"   → {best['desc']}")
        print(f"\nFull registry ({len(ACTION_REGISTRY)} actions):")
        for a in ACTION_REGISTRY:
            print(f"  [{a['roi']}] {a['action']:<30} last: {a['last_run']}")

    elif cmd == "session_start":
        print(session_start())

    elif cmd == "leaderboard":
        for a in ACTION_REGISTRY:
            bar = "█" * int(a["roi"])
            print(f"  {a['roi']} {bar} {a['action']}")

    elif cmd == "ingest" and arg:
        result = rag_ingest_and_build(arg)
        print(json.dumps(result, indent=2))

    elif cmd == "seed" and arg:
        result = seed_and_grow(arg)
        print(result["seed"])
        print(result["grow"])

    elif cmd == "playlist" and arg:
        print(playlist_to_packages(arg))

    elif cmd == "commit" and arg:
        print(git_commit_push(arg))

    elif cmd == "audit":
        result = security_audit()
        print(json.dumps(result, indent=2))

    elif cmd == "rag":
        print(update_rag_leaderboard())

    elif cmd == "call" and arg:
        print(call_openrouter(arg))

    elif cmd == "run" and arg:
        fn_map = {
            "rag_ingest_and_build": lambda: rag_ingest_and_build(sys.argv[3] if len(sys.argv)>3 else ""),
            "transmute_to_skill": lambda: transmute_to_skill(sys.argv[3] if len(sys.argv)>3 else ""),
            "playlist_to_packages": lambda: playlist_to_packages(sys.argv[3] if len(sys.argv)>3 else ""),
            "seed_and_grow": lambda: seed_and_grow(sys.argv[3] if len(sys.argv)>3 else ""),
            "git_commit_push": lambda: git_commit_push(sys.argv[3] if len(sys.argv)>3 else "session update"),
            "security_audit": lambda: security_audit(),
            "session_start": lambda: session_start(),
        }
        fn = fn_map.get(arg)
        if fn:
            result = fn()
            print(json.dumps(result, indent=2) if isinstance(result, dict) else result)
        else:
            print(f"Unknown action: {arg}. Available: {list(fn_map.keys())}")

    else:
        print(__doc__)
