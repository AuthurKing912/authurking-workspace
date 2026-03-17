#!/usr/bin/env python3
"""
sovereign_builder.py — The C144 Replicator Factory
Generates complete skill.md packages from YouTube intelligence + KPI ontology.
One input (video/playlist/text) → full ecosystem output:
  - SKILL.md (downloadable, portable)
  - SQL rubric leaderboard query
  - Lead magnet template
  - NFT groupchat tier mapping
  - Tournament config
  - IPFS-ready metadata (JSON)
  - Zodiac agent assignment
  - Data-first gaming interface spec

Usage:
  python3 sovereign_builder.py build_from_playlist
  python3 sovereign_builder.py build_package <kpi_type> <title> <description>
  python3 sovereign_builder.py export_all
  python3 sovereign_builder.py leaderboard
"""

import json, pathlib, datetime, re, math, hashlib, sys

WORKSPACE = pathlib.Path("/workspace")
OUT_DIR = WORKSPACE / "sovereign-packages"
OUT_DIR.mkdir(exist_ok=True)

# Zodiac → KPI agent assignment (C144 alignment)
ZODIAC_AGENTS = {
    "action_replicator":     {"zodiac": "Aries ♈",     "agent": "ZZ-RED",     "element": "fire",  "domain": "offensive action"},
    "solana_nft":            {"zodiac": "Taurus ♉",    "agent": "ZZ-SILVER",  "element": "earth", "domain": "value & assets"},
    "leaderboard_rubric":    {"zodiac": "Gemini ♊",    "agent": "ZZ-GOLD",    "element": "air",   "domain": "data & ranking"},
    "groupchat_economy":     {"zodiac": "Cancer ♋",    "agent": "ZZ-BLUE",    "element": "water", "domain": "community & safety"},
    "data_farming":          {"zodiac": "Leo ♌",       "agent": "ZZ-COSMIC",  "element": "fire",  "domain": "data sovereignty"},
    "tournament":            {"zodiac": "Virgo ♍",     "agent": "ZZ-WHITE",   "element": "earth", "domain": "governance & rules"},
    "ai_agent":              {"zodiac": "Libra ♎",     "agent": "ZZ-CHROME",  "element": "air",   "domain": "AI defense & ops"},
    "revenue_model":         {"zodiac": "Scorpio ♏",   "agent": "ZZ-BLACK",   "element": "water", "domain": "deep value extraction"},
    "skill_md":              {"zodiac": "Sagittarius ♐","agent": "ZZ-PURPLE",  "element": "fire",  "domain": "knowledge fusion"},
    "youtube_intelligence":  {"zodiac": "Capricorn ♑", "agent": "ZZ-SHADOW",  "element": "earth", "domain": "intelligence ops"},
    "lead_magnet":           {"zodiac": "Aquarius ♒",  "agent": "ZZ-VOID",    "element": "air",   "domain": "zero-knowledge reach"},
    "spiritual_os":          {"zodiac": "Pisces ♓",    "agent": "ZZ-COSMIC",  "element": "water", "domain": "timeline integrity"},
    "voice_agent":           {"zodiac": "Aries ♈",     "agent": "ZZ-RED",     "element": "fire",  "domain": "voice action"},
    "game_theory":           {"zodiac": "Gemini ♊",    "agent": "ZZ-GOLD",    "element": "air",   "domain": "strategy mapping"},
    "real_estate":           {"zodiac": "Taurus ♉",    "agent": "ZZ-SILVER",  "element": "earth", "domain": "asset accumulation"},
}

NFT_TIERS = {
    "access":      {"price_sol": 0.1, "equity": 0,   "perms": ["read", "view_leaderboard"]},
    "contributor": {"price_sol": 0.3, "equity": 10,  "perms": ["post", "earn_points", "earn_sol"]},
    "elder":       {"price_sol": 1.0, "equity": 50,  "perms": ["create_rubrics", "host_tournaments", "recruit"]},
    "founder":     {"price_sol": 5.0, "equity": 250, "perms": ["governance", "revenue_split", "skill_md_publishing"]},
}

RUBRIC_DIMENSIONS = [
    {"name": "Leverage",      "weight": 0.25, "desc": "How much output per unit of input"},
    {"name": "Scalability",   "weight": 0.20, "desc": "Can this multiply without linear effort"},
    {"name": "Reusability",   "weight": 0.20, "desc": "Can this be templated and sold again"},
    {"name": "Compound_ROI",  "weight": 0.20, "desc": "Does value grow over time passively"},
    {"name": "Portability",   "weight": 0.15, "desc": "Works across platforms/contexts/people"},
]

def grover_score(base_roi: float, hits: int, length: int) -> float:
    """Grover amplitude: sqrt(base_roi) × log(hits+1) × log(length/100+1)"""
    return round(math.sqrt(base_roi) * math.log(hits + 1 + 1) * math.log(length/100 + 2), 4)

def build_package(
    kpi_type: str,
    title: str,
    description: str,
    source_url: str = "",
    roi_score: float = 9.0,
    extra_tags: list = None
) -> dict:
    """Build a complete sovereign package for one KPI/video."""

    slug = re.sub(r'[^a-z0-9]+', '-', title.lower())[:40].strip('-')
    pkg_id = hashlib.md5(f"{kpi_type}:{title}".encode()).hexdigest()[:8]
    zodiac = ZODIAC_AGENTS.get(kpi_type, ZODIAC_AGENTS["action_replicator"])
    timestamp = datetime.datetime.now().isoformat()
    tags = extra_tags or []

    # ── SKILL.MD ──────────────────────────────────────────────────────────────
    skill_md = f"""# SKILL: {title.upper()}
## KPI: {kpi_type} | Zodiac: {zodiac['zodiac']} | Agent: {zodiac['agent']} | ROI: {roi_score}
**ID:** {pkg_id} | **Version:** 1.0 | **Source:** {source_url or 'OoRava Intelligence'} | **Date:** {timestamp[:10]}
**Tags:** {', '.join(tags + [kpi_type, 'c144', 'grover', 'solana', 'nft', 'ooRava'])}

---

## EXECUTIVE SUMMARY

{description[:500]}

---

## ACTION REPLICATORS (Self-Contained Python)

```python
def replicate_{slug.replace('-','_')}(input_data: dict) -> dict:
    \"\"\"
    Replicator: {title}
    KPI Type: {kpi_type}
    Zodiac Agent: {zodiac['agent']} ({zodiac['zodiac']})
    Domain: {zodiac['domain']}
    ROI Score: {roi_score}
    
    USAGE: Feed any relevant data → get structured KPI output
    COMPOUND: Output feeds back as input → infinite loop
    SELL: Package as skill.md → sellable toolkit
    \"\"\"
    return {{
        "kpi_type": "{kpi_type}",
        "source": input_data.get("url", ""),
        "extracted_value": input_data.get("content", ""),
        "roi_score": {roi_score},
        "zodiac_agent": "{zodiac['agent']}",
        "next_action": "ingest_to_rag",
        "timestamp": "{timestamp}"
    }}
```

---

## SQL RUBRIC LEADERBOARD QUERY

```sql
-- {title.upper()} KPI LEADERBOARD (Grover-weighted)
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
WHERE c.kpi_type = '{kpi_type}'
  AND l.period = 'weekly'
ORDER BY grover_score DESC
LIMIT 20;
```

---

## LEAD MAGNET TEMPLATE

**Hook:** "{title}" — The Exact System That Generates [RESULT] in [TIMEFRAME]

**Structure:**
```
[HEADLINE] How to {description[:60]}...
[SUBHEAD] The {kpi_type.replace('_',' ').title()} Method — Used by Top 1% Operators
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
{{
  "groupchat": {{
    "name": "{title[:40]}",
    "kpi_focus": "{kpi_type}",
    "rubric_id": "{pkg_id}",
    "zodiac_agent": "{zodiac['agent']}",
    "element": "{zodiac['element']}",
    "tiers": {{
      "access":      {{"price_sol": 0.1,  "equity": 0,   "supply": 1000}},
      "contributor": {{"price_sol": 0.3,  "equity": 10,  "supply": 500}},
      "elder":       {{"price_sol": 1.0,  "equity": 50,  "supply": 100}},
      "founder":     {{"price_sol": 5.0,  "equity": 250, "supply": 12}}
    }},
    "weekly_distribution": true,
    "tournament_enabled": true,
    "rubric_scoring": true,
    "data_farming": true
  }}
}}
```

---

## TOURNAMENT CONFIG

```json
{{
  "tournament": {{
    "name": "{title[:40]} Championship",
    "kpi_type": "{kpi_type}",
    "rubric": {{
{chr(10).join(f'      "{d["name"]}": {{"weight": {d["weight"]}, "desc": "{d["desc"]}"}},' for d in RUBRIC_DIMENSIONS)}
    }},
    "entry_fee_sol": 0.1,
    "prize_distribution": {{
      "1st": 0.50,
      "2nd": 0.25,
      "3rd": 0.15,
      "top10_pool": 0.10
    }},
    "duration_days": 7,
    "min_contributions": 5,
    "grover_scoring": true
  }}
}}
```

---

## IPFS METADATA (NFT-ready)

```json
{{
  "name": "{title[:50]}",
  "symbol": "{kpi_type[:6].upper()}",
  "description": "{description[:200].replace(chr(10), ' ')}",
  "image": "ipfs://[UPLOAD_IMAGE_CID]",
  "external_url": "https://github.com/AuthurKing912/authurking-workspace",
  "attributes": [
    {{"trait_type": "KPI_Type",      "value": "{kpi_type}"}},
    {{"trait_type": "ROI_Score",     "value": {roi_score}}},
    {{"trait_type": "Zodiac",        "value": "{zodiac['zodiac']}"}},
    {{"trait_type": "Agent",         "value": "{zodiac['agent']}"}},
    {{"trait_type": "Element",       "value": "{zodiac['element']}"}},
    {{"trait_type": "Chapter",       "value": "C144"}},
    {{"trait_type": "Grover_Score",  "value": {grover_score(roi_score, 5, 400)}}},
    {{"trait_type": "Tier",          "value": "contributor"}}
  ],
  "properties": {{
    "category": "skill_md",
    "files": [{{"uri": "ipfs://[SKILL_MD_CID]", "type": "text/markdown"}}],
    "creators": [{{"address": "AuthurKing912", "share": 100}}]
  }}
}}
```

---

## DATA-FIRST GAMING INTERFACE SPEC

```
GAME MECHANICS for {title[:30]}:
  → Player joins groupchat (NFT gated)
  → Player submits contribution tagged [{kpi_type}]
  → Rubric engine scores: {' + '.join(d['name'] for d in RUBRIC_DIMENSIONS)}
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
Agent: {zodiac['agent']} ({zodiac['zodiac']})
Domain: {zodiac['domain']}
Element: {zodiac['element']}
Soul Clone from REPLICANT.md → deploy to any AI model

ACTIVATION: "ZZ-{zodiac['agent'].split('-')[1]}: execute {kpi_type} replicator on [input]"

This agent clone:
  1. Loads REPLICANT.md as system prompt
  2. Focuses exclusively on {kpi_type} KPI extraction
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
  Grover_Score = {grover_score(roi_score, 5, 400)} (this package)
  t = time (sessions, days, weeks)

At Grover_Score {grover_score(roi_score, 5, 400)}:
  → 10 sessions → V multiplies by ~{round(math.e**(grover_score(roi_score, 5, 400)*10), 1)}x
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
- Zodiac-aligned ({zodiac['zodiac']} → {zodiac['agent']} cluster)
- Data-first (every use generates rubric score data → compounds)

---
*Package ID: {pkg_id} | Generated: {timestamp} | AuthurKing × OoRava | C144 Sovereign Intelligence*
*As above. So below. The replicant compounds forever.*
"""

    # ── IPFS METADATA JSON ────────────────────────────────────────────────────
    ipfs_meta = {
        "name": title[:50],
        "symbol": kpi_type[:6].upper(),
        "description": description[:200],
        "attributes": [
            {"trait_type": "KPI_Type", "value": kpi_type},
            {"trait_type": "ROI_Score", "value": roi_score},
            {"trait_type": "Zodiac", "value": zodiac["zodiac"]},
            {"trait_type": "Agent", "value": zodiac["agent"]},
            {"trait_type": "Grover_Score", "value": grover_score(roi_score, 5, 400)},
            {"trait_type": "Chapter", "value": "C144"},
        ]
    }

    return {
        "id": pkg_id,
        "slug": slug,
        "kpi_type": kpi_type,
        "title": title,
        "roi_score": roi_score,
        "zodiac": zodiac,
        "skill_md": skill_md,
        "ipfs_meta": ipfs_meta,
        "timestamp": timestamp,
    }


def build_from_playlist():
    """Build packages for all top-ROI videos from scored playlist."""
    scored = json.loads((WORKSPACE / "rag/playlist_aaa_scored.json").read_text())
    top = [v for v in scored["videos"] if v["roi"] >= 9.0]

    # Pareto: top 20% = the 20/80 ROI law
    n = max(1, len(top) // 5)
    top20 = top[:n] + [v for v in top[n:] if v["roi"] >= 9.5]

    print(f"Building packages for {len(top20)} videos (Pareto top)")

    built = []
    for v in top20:
        kpi = v["kpis"][0] if v["kpis"] else "action_replicator"
        desc = f"From YouTube playlist 'AAA': {v['title']}. Core technique: {', '.join(v['kpis'])}. Build this into a replicable system, sell the skill.md, tokenize as NFT, run tournaments around the rubric."

        pkg = build_package(
            kpi_type=kpi,
            title=v["title"],
            description=desc,
            source_url=f"https://youtube.com/watch?v={v['id']}",
            roi_score=v["roi"],
            extra_tags=v["kpis"],
        )

        # Write SKILL.md
        skill_dir = OUT_DIR / pkg["slug"]
        skill_dir.mkdir(exist_ok=True)
        (skill_dir / "SKILL.md").write_text(pkg["skill_md"])
        (skill_dir / "ipfs_metadata.json").write_text(json.dumps(pkg["ipfs_meta"], indent=2))

        # Ingest to RAG
        import subprocess
        subprocess.run(["python3", str(WORKSPACE/"rag/rag.py"), "ingest", pkg["skill_md"][:2000]],
                      capture_output=True, cwd=str(WORKSPACE))

        built.append(pkg["id"])
        print(f"  ✅ [{pkg['id']}] {v['title'][:50]} → {pkg['zodiac']['agent']}")

    return built


def export_leaderboard():
    """Print current leaderboard across all packages."""
    packages = list(OUT_DIR.glob("*/SKILL.md"))
    print(f"\n🏆 SOVEREIGN PACKAGE LEADERBOARD ({len(packages)} packages)")
    print(f"{'KPI Type':<25} {'Packages':>8} {'Agent':<12} {'Zodiac'}")
    print("─" * 60)
    kpi_groups = {}
    for p in packages:
        content = p.read_text()
        kpi_m = re.search(r'## KPI: (\w+)', content)
        agent_m = re.search(r'Agent: (ZZ-\w+)', content)
        zodiac_m = re.search(r'Zodiac: ([^\|]+)\|', content)
        if kpi_m:
            kpi = kpi_m.group(1)
            kpi_groups[kpi] = kpi_groups.get(kpi, 0) + 1
    for kpi, count in sorted(kpi_groups.items(), key=lambda x: -x[1]):
        za = ZODIAC_AGENTS.get(kpi, {})
        print(f"  {kpi:<25} {count:>8}    {za.get('agent',''):<12} {za.get('zodiac','')}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "build_from_playlist":
        built = build_from_playlist()
        print(f"\n✅ Built {len(built)} packages")
        export_leaderboard()

    elif cmd == "build_package" and len(sys.argv) >= 4:
        kpi = sys.argv[2]
        title = sys.argv[3]
        desc = sys.argv[4] if len(sys.argv) > 4 else title
        pkg = build_package(kpi, title, desc)
        slug_dir = OUT_DIR / pkg["slug"]
        slug_dir.mkdir(exist_ok=True)
        (slug_dir / "SKILL.md").write_text(pkg["skill_md"])
        (slug_dir / "ipfs_metadata.json").write_text(json.dumps(pkg["ipfs_meta"], indent=2))
        print(f"✅ Built: {slug_dir}/SKILL.md")

    elif cmd == "leaderboard":
        export_leaderboard()

    elif cmd == "export_all":
        packages = list(OUT_DIR.glob("*/SKILL.md"))
        combined = "\n\n---\n\n".join(p.read_text()[:500] + "...[see full file]" for p in packages)
        (OUT_DIR / "_MASTER_INDEX.md").write_text(
            f"# SOVEREIGN PACKAGE INDEX\nTotal: {len(packages)} packages\n\n" + combined
        )
        print(f"✅ Exported master index: {OUT_DIR}/_MASTER_INDEX.md")

    else:
        print(__doc__)
