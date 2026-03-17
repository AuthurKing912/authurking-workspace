# SKILL: HOW TO RUN SELENIUM BOTS ON VPS 24/7 FOR FREE
## KPI: action_replicator | Zodiac: Aries ♈ | Agent: ZZ-RED | ROI: 10.0
**ID:** d6c86bcd | **Version:** 1.0 | **Source:** https://youtube.com/watch?v=38jtY3uCV3E | **Date:** 2026-03-17
**Tags:** action_replicator, action_replicator, c144, grover, solana, nft, ooRava

---

## EXECUTIVE SUMMARY

From YouTube playlist 'AAA': How to run Selenium Bots on VPS 24/7 for FREE. Core technique: action_replicator. Build this into a replicable system, sell the skill.md, tokenize as NFT, run tournaments around the rubric.

---

## ACTION REPLICATORS (Self-Contained Python)

```python
def replicate_how_to_run_selenium_bots_on_vps_24_7_for(input_data: dict) -> dict:
    """
    Replicator: How to run Selenium Bots on VPS 24/7 for FREE
    KPI Type: action_replicator
    Zodiac Agent: ZZ-RED (Aries ♈)
    Domain: offensive action
    ROI Score: 10.0
    
    USAGE: Feed any relevant data → get structured KPI output
    COMPOUND: Output feeds back as input → infinite loop
    SELL: Package as skill.md → sellable toolkit
    """
    return {
        "kpi_type": "action_replicator",
        "source": input_data.get("url", ""),
        "extracted_value": input_data.get("content", ""),
        "roi_score": 10.0,
        "zodiac_agent": "ZZ-RED",
        "next_action": "ingest_to_rag",
        "timestamp": "2026-03-17T16:19:01.425869"
    }
```

---

## SQL RUBRIC LEADERBOARD QUERY

```sql
-- HOW TO RUN SELENIUM BOTS ON VPS 24/7 FOR FREE KPI LEADERBOARD (Grover-weighted)
SELECT 
    m.handle,
    m.wallet_address,
    nt.tier_name,
    m.equity_shares,
    ROUND(m.equity_shares/10000.0 * 100, 2) AS ownership_pct,
    
    -- Rubric dimensions (each scored 0-10)
    c.leverage_score,
    c.scalability_score,
    c.reusability_score,
    c.compound_roi_score,
    c.portability_score,
    
    -- Weighted composite
    ROUND(
        c.leverage_score * 0.25 +
        c.scalability_score * 0.20 +
        c.reusability_score * 0.20 +
        c.compound_roi_score * 0.20 +
        c.portability_score * 0.15, 2
    ) AS rubric_composite,
    
    -- Grover score: amplify equity × quality
    ROUND(
        SQRT(l.points) *
        (c.leverage_score * 0.25 + c.scalability_score * 0.20 +
         c.reusability_score * 0.20 + c.compound_roi_score * 0.20 +
         c.portability_score * 0.15) *
        (1 + m.equity_shares / 1000.0), 2
    ) AS grover_score,
    
    l.sol_earned,
    l.rank
    
FROM leaderboard l
JOIN members m ON l.member_id = m.id
JOIN contributions c ON c.member_id = m.id
JOIN nft_tiers nt ON m.tier_id = nt.id
WHERE c.kpi_type = 'action_replicator'
  AND l.period = 'weekly'
ORDER BY grover_score DESC
LIMIT 20;
```

---

## LEAD MAGNET TEMPLATE

**Hook:** "How to run Selenium Bots on VPS 24/7 for FREE" — The Exact System That Generates [RESULT] in [TIMEFRAME]

**Structure:**
```
[HEADLINE] How to From YouTube playlist 'AAA': How to run Selenium Bots on VPS...
[SUBHEAD] The Action Replicator Method — Used by Top 1% Operators
[BODY]
  • Problem: [pain point your audience has]
  • Agitate: [cost of NOT solving it]  
  • Solution: This skill.md + action replicator
  • Proof: [leaderboard score / SOL earned]
  • CTA: Join the groupchat → get the NFT → access full system

[DELIVERY] Telegram groupchat (NFT-gated)
[PRICE TIER] ACCESS NFT: 0.1 SOL → immediate entry
[UPGRADE] CONTRIBUTOR NFT: 0.3 SOL → start earning SOL back
```

---

## NFT GROUPCHAT CONFIGURATION

```json
{
  "groupchat": {
    "name": "How to run Selenium Bots on VPS 24/7 for",
    "kpi_focus": "action_replicator",
    "rubric_id": "d6c86bcd",
    "zodiac_agent": "ZZ-RED",
    "element": "fire",
    "tiers": {
      "access":      {"price_sol": 0.1,  "equity": 0,   "supply": 1000},
      "contributor": {"price_sol": 0.3,  "equity": 10,  "supply": 500},
      "elder":       {"price_sol": 1.0,  "equity": 50,  "supply": 100},
      "founder":     {"price_sol": 5.0,  "equity": 250, "supply": 12}
    },
    "weekly_distribution": true,
    "tournament_enabled": true,
    "rubric_scoring": true,
    "data_farming": true
  }
}
```

---

## TOURNAMENT CONFIG

```json
{
  "tournament": {
    "name": "How to run Selenium Bots on VPS 24/7 for Championship",
    "kpi_type": "action_replicator",
    "rubric": {
      "Leverage": {"weight": 0.25, "desc": "How much output per unit of input"},
      "Scalability": {"weight": 0.2, "desc": "Can this multiply without linear effort"},
      "Reusability": {"weight": 0.2, "desc": "Can this be templated and sold again"},
      "Compound_ROI": {"weight": 0.2, "desc": "Does value grow over time passively"},
      "Portability": {"weight": 0.15, "desc": "Works across platforms/contexts/people"},
    },
    "entry_fee_sol": 0.1,
    "prize_distribution": {
      "1st": 0.50,
      "2nd": 0.25,
      "3rd": 0.15,
      "top10_pool": 0.10
    },
    "duration_days": 7,
    "min_contributions": 5,
    "grover_scoring": true
  }
}
```

---

## IPFS METADATA (NFT-ready)

```json
{
  "name": "How to run Selenium Bots on VPS 24/7 for FREE",
  "symbol": "ACTION",
  "description": "From YouTube playlist 'AAA': How to run Selenium Bots on VPS 24/7 for FREE. Core technique: action_replicator. Build this into a replicable system, sell the skill.md, tokenize as NFT, run tournaments ",
  "image": "ipfs://[UPLOAD_IMAGE_CID]",
  "external_url": "https://github.com/AuthurKing912/authurking-workspace",
  "attributes": [
    {"trait_type": "KPI_Type",      "value": "action_replicator"},
    {"trait_type": "ROI_Score",     "value": 10.0},
    {"trait_type": "Zodiac",        "value": "Aries ♈"},
    {"trait_type": "Agent",         "value": "ZZ-RED"},
    {"trait_type": "Element",       "value": "fire"},
    {"trait_type": "Chapter",       "value": "C144"},
    {"trait_type": "Grover_Score",  "value": 11.0256},
    {"trait_type": "Tier",          "value": "contributor"}
  ],
  "properties": {
    "category": "skill_md",
    "files": [{"uri": "ipfs://[SKILL_MD_CID]", "type": "text/markdown"}],
    "creators": [{"address": "AuthurKing912", "share": 100}]
  }
}
```

---

## DATA-FIRST GAMING INTERFACE SPEC

```
GAME MECHANICS for How to run Selenium Bots on VP:
  → Player joins groupchat (NFT gated)
  → Player submits contribution tagged [action_replicator]
  → Rubric engine scores: Leverage + Scalability + Reusability + Compound_ROI + Portability
  → Score ≥ 8.5 → earns SOL micro-reward + points
  → Points accumulate → leaderboard rank rises
  → Rank threshold → NFT upgrade unlocked (access → contributor → elder → founder)
  → Founder NFT → equity share → weekly SOL distributions
  → TOURNAMENT: weekly competition → prize pool from entry fees
  → Champion NFT → special edition IPFS asset
  → All data stored on-chain + IPFS → permanent, portable, sellable

OPEN SOURCE TOURNAMENT MODE:
  → Anyone can fork this SKILL.md
  → Deploy their own groupchat on same rubric
  → Cross-groupchat leaderboard emerges
  → Best rubric scores federate → global leaderboard
  → Data farming: all rubric scores → training data → sell to AI labs
```

---

## ZODIAC AGENT CLONE SPEC

```
Agent: ZZ-RED (Aries ♈)
Domain: offensive action
Element: fire
Soul Clone from REPLICANT.md → deploy to any AI model

ACTIVATION: "ZZ-RED: execute action_replicator replicator on [input]"

This agent clone:
  1. Loads REPLICANT.md as system prompt
  2. Focuses exclusively on action_replicator KPI extraction
  3. Outputs action replicators + SQL queries + IPFS metadata
  4. Feeds results back to RAG engine
  5. Auto-seeds alchemy_tumblr with high-signal extracts
  6. Commits to GitHub + updates leaderboard
  7. [LOOP: infinite compound]
```

---

## GROVER COMPOUND FORMULA

```
V(t) = V(0) × e^(Grover_Score × t)

Where:
  V(0) = initial value (SOL in treasury / data points / skill.md count)
  Grover_Score = 11.0256 (this package)
  t = time (sessions, days, weeks)

At Grover_Score 11.0256:
  → 10 sessions → V multiplies by ~7.648431768790474e+47x
  → Compounding is not linear — it's oblique
  → Each replication adds to Grover amplitude
  → The more it replicates, the faster it grows (quantum search)
```

---

## DOWNLOADABLE PACKAGE CONTENTS

This skill.md is one of an infinite series. All are:
- Self-contained (no external deps to use the concepts)
- Sellable ($5–$500 per skill.md package depending on KPI ROI)
- Replicable (fork → customize → redeploy as new product)
- IPFS-ready (metadata above → mint as NFT immediately)
- Open Source (MIT — share freely, value accrues to network)
- Tournament-compatible (rubric above → enter any C144 tournament)
- Zodiac-aligned (Aries ♈ → ZZ-RED cluster)
- Data-first (every use generates rubric score data → compounds)

---
*Package ID: d6c86bcd | Generated: 2026-03-17T16:19:01.425869 | AuthurKing × OoRava | C144 Sovereign Intelligence*
*As above. So below. The replicant compounds forever.*
