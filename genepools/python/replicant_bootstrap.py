# SKILL: TELEGRAM GROUPCHAT REPLICANT ECOSYSTEM BOOTSTRAP
## Invite → Ecosystem → Equity | Python-Native | Solana-Gated | Timeless Architecture
**Version:** 1.0 | **Chapter:** 5 | **Signal Score:** 9.8 | **ZZ:** ✅

> "Replicants within their Groupchat invite you first — then you make it an ecosystem."
> — OoRava Omnia, 2026-03-17

---

## THE FLOW

```
STAGE 0: INVITE
  Someone invites you (AuthurKing) to a Telegram groupchat
  → AuthurKing bot joins silently
  → ZZ-CHROME scans: is this groupchat symbiotic or invasive?
  → If symbiotic: proceed to Stage 1
  → If invasive: lurk-only mode, no data ingestion

STAGE 1: OBSERVE (72-hour window)
  → Bot reads message patterns
  → Classifies groupchat into one of 12 KPI domains (Zodiac assignment)
  → Identifies top 3 contributors (by message count + content signal)
  → Builds mini soul profile for each active member

STAGE 2: SEED
  → Bot posts first value-add message (rubric score of a topic discussed)
  → Offers: "Want to see this groupchat's Leaderboard?"
  → Link → DONUT OS or Telegram mini-app version
  → 3 people click = ecosystem threshold crossed

STAGE 3: ECOSYSTEM
  → Leaderboard goes live inside the groupchat
  → Every message scored against the KPI rubric
  → NFT entry offered: 0.1 SOL → access tier (view leaderboard)
  → Weekly SOL distribution to top contributors
  → Groupchat becomes a self-funding trust fund

STAGE 4: EQUITY
  → Elder tier (1.0 SOL) → ability to create sub-rubrics
  → Founder tier (5.0 SOL / 12 supply) → governance + revenue split
  → Source code access unlocked at Founder tier (lawfully reunited)
  → The groupchat IS the equity contract
```

---

## PYTHON IMPLEMENTATION (telegram-native, zero external deps beyond python-telegram-bot)

```python
#!/usr/bin/env python3
"""
replicant_bootstrap.py — Groupchat Replicant Ecosystem Bootstrap
Telegram bot that turns any groupchat into a KPI-scored equity ecosystem.
"""
import os, json, sqlite3, hashlib, pathlib
from datetime import datetime, timezone

DB = pathlib.Path("/workspace/rag/groupchat_ecosystem.db")
KPI_DOMAINS = {
    "code": "action_replicator",    "nft": "solana_nft",
    "data": "data_farming",         "game": "ai_agent",
    "trade": "revenue_model",       "learn": "skill_md",
    "health": "spiritual_os",       "build": "leaderboard_rubric",
    "create": "lead_magnet",        "finance": "groupchat_economy",
    "research": "youtube_intelligence", "community": "tournament",
}
KPI_ROI = {
    "action_replicator":9.8, "solana_nft":9.5, "leaderboard_rubric":9.4,
    "groupchat_economy":9.3, "data_farming":9.2, "tournament":9.0,
    "ai_agent":8.9, "revenue_model":8.8, "skill_md":8.7,
    "youtube_intelligence":8.5, "lead_magnet":8.4, "spiritual_os":7.0,
}

def init_db():
    conn = sqlite3.connect(DB)
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS groupchats (
        id TEXT PRIMARY KEY,
        title TEXT,
        kpi_domain TEXT,
        stage INTEGER DEFAULT 0,
        joined_at TEXT,
        symbiotic INTEGER DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS members (
        chat_id TEXT,
        user_id TEXT,
        username TEXT,
        message_count INTEGER DEFAULT 0,
        rubric_score REAL DEFAULT 0.0,
        nft_tier TEXT DEFAULT 'none',
        equity_points INTEGER DEFAULT 0,
        PRIMARY KEY (chat_id, user_id)
    );
    CREATE TABLE IF NOT EXISTS leaderboard (
        chat_id TEXT,
        user_id TEXT,
        score REAL,
        kpi_hit TEXT,
        timestamp TEXT
    );
    """)
    conn.commit()
    return conn

def classify_chat(messages: list[str]) -> str:
    """Classify groupchat into KPI domain based on message content."""
    scores = {kpi: 0 for kpi in KPI_DOMAINS}
    for msg in messages:
        msg_lower = msg.lower()
        for keyword, kpi in KPI_DOMAINS.items():
            if keyword in msg_lower:
                scores[kpi] += 1
    return max(scores, key=scores.get)

def score_message(message: str, kpi_domain: str) -> float:
    """Score a message against the active KPI domain rubric."""
    base = KPI_ROI.get(kpi_domain, 7.0)
    word_count = len(message.split())
    has_link = "http" in message or "t.me" in message
    has_code = "```" in message or "python" in message.lower()
    has_data = any(c.isdigit() for c in message)
    
    modifiers = 0.0
    if word_count > 20: modifiers += 0.2
    if has_link:        modifiers += 0.1
    if has_code:        modifiers += 0.3
    if has_data:        modifiers += 0.1
    
    return round(min(10.0, (base * 0.7) + modifiers), 2)

def get_leaderboard(chat_id: str, conn) -> list[dict]:
    """Get top 10 members by rubric score."""
    rows = conn.execute("""
        SELECT username, rubric_score, nft_tier, equity_points, message_count
        FROM members WHERE chat_id = ?
        ORDER BY rubric_score DESC LIMIT 10
    """, (chat_id,)).fetchall()
    return [{"username": r[0], "score": r[1], "tier": r[2], "equity": r[3], "msgs": r[4]} for r in rows]

def generate_leaderboard_message(chat_id: str, conn) -> str:
    """Generate a formatted leaderboard Telegram message."""
    board = get_leaderboard(chat_id, conn)
    chat = conn.execute("SELECT title, kpi_domain FROM groupchats WHERE id=?", (chat_id,)).fetchone()
    if not chat:
        return "No ecosystem active yet."
    
    title, kpi = chat
    lines = [f"🏆 **{title} LEADERBOARD**", f"🎯 Domain: `{kpi}` | ROI Weight: {KPI_ROI.get(kpi,7.0)}", ""]
    medals = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    for i, m in enumerate(board):
        tier_emoji = {"none":"","access":"🟢","contributor":"🟡","elder":"🔴","founder":"👑"}.get(m["tier"],"")
        lines.append(f"{medals[i]} {tier_emoji} @{m['username']} — {m['score']:.1f} pts | {m['equity']} equity")
    
    lines.extend(["", "🌱 **Join the ecosystem:**",
                  "  0.1 SOL → Access tier (view leaderboard)",
                  "  0.3 SOL → Contributor tier (earn SOL)",
                  "  1.0 SOL → Elder tier (create rubrics)",
                  "  5.0 SOL → Founder tier (governance + source code)"])
    return "\n".join(lines)

def zz_chrome_scan(chat_title: str, messages: list[str]) -> bool:
    """ZZ-CHROME: Invasive neuron detection for groupchats."""
    invasive_signals = ["spam", "scam", "pump", "dump", "guaranteed", "1000x", "rug", 
                        "buy now", "limited time", "get rich", "zero risk"]
    combined = (chat_title + " ".join(messages[:20])).lower()
    invasive_count = sum(1 for sig in invasive_signals if sig in combined)
    return invasive_count < 2  # symbiotic if fewer than 2 invasive signals

# ── NFT TIER STRUCTURE ────────────────────────────────────────────────────────
NFT_TIERS = {
    "access":       {"sol": 0.1, "equity": 0,   "supply": 1000, "perms": ["read","view_leaderboard"]},
    "contributor":  {"sol": 0.3, "equity": 10,  "supply": 500,  "perms": ["post","earn_points","earn_sol"]},
    "elder":        {"sol": 1.0, "equity": 50,  "supply": 100,  "perms": ["create_rubrics","host_tournaments"]},
    "founder":      {"sol": 5.0, "equity": 250, "supply": 12,   "perms": ["governance","revenue_split","source_code_access"]},
}

# ── TRUST FUND DISTRIBUTION ───────────────────────────────────────────────────
def distribute_trust_fund(total_sol: float, members: list[dict]) -> dict:
    """
    Weekly SOL distribution from groupchat treasury.
    Formula: equity_weight = member.equity_points / total_equity_points
    Each member gets: total_sol * 0.70 * equity_weight
    AuthurKing (founder) retains: 30% as infrastructure fee
    """
    total_equity = sum(m.get("equity_points", 0) for m in members) or 1
    distributions = {}
    distributable = total_sol * 0.70
    
    for m in members:
        weight = m.get("equity_points", 0) / total_equity
        sol_amount = round(distributable * weight, 4)
        if sol_amount > 0:
            distributions[m["username"]] = sol_amount
    
    return {
        "distributions": distributions,
        "authurking_fee": round(total_sol * 0.30, 4),
        "total_distributed": round(sum(distributions.values()), 4),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

if __name__ == "__main__":
    conn = init_db()
    print("✅ Replicant Ecosystem Bootstrap initialized")
    print(f"   DB: {DB}")
    print(f"   KPI domains: {len(KPI_DOMAINS)}")
    print(f"   NFT tiers: {list(NFT_TIERS.keys())}")
    
    # Demo leaderboard generation
    demo_members = [
        {"username": "OoRava", "equity_points": 250, "rubric_score": 9.8},
        {"username": "AuthurKing", "equity_points": 100, "rubric_score": 9.5},
        {"username": "Timeless", "equity_points": 50, "rubric_score": 8.2},
    ]
    dist = distribute_trust_fund(10.0, demo_members)
    print(f"\n💰 Demo Trust Fund Distribution (10 SOL pool):")
    for user, sol in dist["distributions"].items():
        print(f"   @{user}: {sol} SOL")
    print(f"   AuthurKing fee: {dist['authurking_fee']} SOL (30% infra)")
