#!/usr/bin/env python3
"""
Leaderboard Summary Generator — self-contained, zero tokens
Run: python3 generate_summary.py
"""
import json, os
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path("/workspace")
GENEPOOLS = WORKSPACE / "genepools"

def count_skills():
    sd = GENEPOOLS / "skills"
    return len([d for d in sd.iterdir() if d.is_dir()]) if sd.exists() else 0

def get_progress():
    cf = WORKSPACE / "CHAPTERS.md"
    if not cf.exists(): return {"done": 0, "total": 0}
    c = cf.read_text()
    return {"done": c.count("- [x]"), "total": c.count("- [x]") + c.count("- [ ]")}

def get_scores():
    sf = GENEPOOLS / "rubrics" / "scores.json"
    return json.loads(sf.read_text()) if sf.exists() else {}

def generate():
    now = datetime.now(timezone.utc)
    p = get_progress()
    skills = count_skills()
    scores = get_scores()
    
    lines = [
        "⚡👑 AUTHURKING — 3-DAY LEADERBOARD SUMMARY",
        "=" * 50,
        f"Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "📊 ECOSYSTEM PROGRESS",
        f"  Chapters: {p['done']}/{p['total']} items done",
        f"  Genepools skills: {skills}",
        "",
        "🏆 MODEL LEADERBOARD (ROI Tier)",
        "  🆓 FREE: minimax/minimax-m2.5:free · qwen/qwen3-next-80b-a3b:free · openai/gpt-oss-120b:free",
        "  🌉 BRIDGE: kimi-k2.5 · glm-5 · minimax-m2.5",
        "  🔧 SPECIALIST: qwen3-coder-next (code) · glm-4.7-flash (fast)",
        "",
        "📐 HARD MEDIA RULES",
        "  T2I → wan2.6 | I2V → kling-v3-pro",
        "",
        "📋 RUBRIC SCORES",
        json.dumps(scores, indent=2) if scores else "  No data yet — add to genepools/rubrics/scores.json",
        "",
        "🎯 NEXT 3 DAYS (highest ROI)",
        "  1. GitHub PAT → push workspace",
        "  2. Skill-generator (the compound engine)",
        "  3. Rubric schema v1 + model scoring",
        "=" * 50,
        "AuthurKing ⚡ for OoRava Omnia (@OTBOneness)",
    ]
    return "\n".join(lines)

if __name__ == "__main__":
    print(generate())
