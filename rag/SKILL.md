# SKILL: SOVEREIGN RAG ENGINE
## OoRava Intelligence Ingestion System | Pure Python | Zero External Deps
**Version:** 1.0 | **Chapter:** 2 | **Signal Score:** 9.9 | **Type:** L4 System-Builder

---

## WHAT THIS IS

A pure-Python RAG (Retrieval Augmented Generation) system purpose-built for OoRava's intelligence ecosystem. No vectors database, no external APIs, no dependencies — just SQLite + TF-IDF cosine similarity + Grover-weighted retrieval.

**Everything flows through here:**
- Chat exports, voice transcripts, soul data → chunked → KPI-classified → ROI-scored
- YouTube videos/playlists → title + description + chapters → ingested
- Every SKILL.md, soul layer file, rubric → indexed
- Query anything → retrieve highest-Grover-score context → feed to any AI model

---

## ARCHITECTURE

```
INPUT (any format)
    ↓
CHUNKER (400-word overlapping windows + section detection)
    ↓
KPI CLASSIFIER (15-type ontology: action_replicator, solana_nft, 
                leaderboard_rubric, groupchat_economy, data_farming,
                tournament, ai_agent, revenue_model, skill_md,
                youtube_intelligence, lead_magnet, voice_agent,
                game_theory, real_estate, spiritual_os)
    ↓
ROI SCORER (Grover-weighted: base_roi × length_boost × action_boost)
    ↓
TF-IDF VECTORIZER (pure stdlib: tf × log(N/df), top 50 terms per chunk)
    ↓
SQLITE STORAGE (chunks + replicators + leaderboard + ingestion_log)
    ↓
QUERY ENGINE (cosine_similarity × sqrt(roi_score) = grover_score)
    ↓
AUTO-REPLICATOR GENERATOR (ROI ≥ 8.5 → generate Python + SQL replicator)
    ↓
ACTION REPLICATORS (self-contained Python functions, ready to run)
```

---

## KPI ONTOLOGY (ROI-sorted)

| KPI Type | ROI Weight | What It Captures |
|----------|-----------|-----------------|
| action_replicator | 9.8 | Automation, workflows, pipelines, n8n |
| solana_nft | 9.5 | Blockchain, minting, web3, on-chain |
| leaderboard_rubric | 9.4 | KPIs, scoring, ranking, metrics |
| groupchat_economy | 9.3 | Gated communities, members, access |
| data_farming | 9.2 | Harvesting, datasets, collection |
| tournament | 9.0 | Competitions, prizes, entry fees |
| ai_agent | 8.9 | Models, swarms, orchestration |
| revenue_model | 8.8 | Sales, offers, income, scale |
| skill_md | 8.7 | Prompts, personas, skill files |
| youtube_intelligence | 8.5 | Videos, playlists, creators |
| lead_magnet | 8.4 | Funnels, opt-ins, hyper-elite |
| voice_agent | 8.2 | TTS, voice calls, speech |
| game_theory | 8.0 | Nash, equilibrium, incentives |
| real_estate | 7.5 | Property, microacquisitions |
| spiritual_os | 7.0 | Meditation, consciousness, hermetic |

---

## GROVER RETRIEVAL FORMULA

```python
grover_score = cosine_similarity(query_vec, chunk_vec) × sqrt(roi_score)
```

This ensures: high-similarity × high-value content surfaces first. Low-similarity content with high ROI also rises above low-quality exact matches.

---

## CLI COMMANDS

```bash
# Ingest files or raw text
python3 rag/rag.py ingest <file_path_or_text>
python3 rag/rag.py ingest_all           # bulk-ingest all vault + souls + skills

# Query
python3 rag/rag.py query "youtube playlist high roi extraction"

# Reports
python3 rag/rag.py leaderboard          # KPI leaderboard by ROI
python3 rag/rag.py status               # chunk/replicator counts
python3 rag/rag.py export_replicators   # export all replicators to .md

# YouTube Intelligence
python3 rag/youtube_extractor.py video <url>
python3 rag/youtube_extractor.py playlist <url>
python3 rag/youtube_extractor.py ingest_to_rag <url>
```

---

## HOW TO INGEST NEW DATA (Any Format)

OoRava drops ANY data → it goes through RAG:

```
1. Telegram file drop → /root/.openclaw/media/inbound/
   → python3 rag/rag.py ingest <path>

2. YouTube link → send URL in chat
   → python3 rag/youtube_extractor.py ingest_to_rag <url>

3. Raw text paste → python3 rag/rag.py ingest "raw text here"

4. Bulk update → python3 rag/rag.py ingest_all
```

---

## AUTO-GENERATED REPLICATORS

When a chunk scores ROI ≥ 8.5, the system auto-generates:
1. A Python function replicator for that KPI type
2. A SQL query replicator for that KPI's leaderboard data
3. Stores both in SQLite `replicators` table + exports to `rag/replicators/`

These are the action replicators OoRava asked for — created in real-time from the data itself.

---

## CURRENT STATE (as of 2026-03-17)

```
Chunks:       50     (from 14 sources)
Replicators:  85     (auto-generated from high-ROI chunks)
Avg ROI:      9.35
Top KPIs:     action_replicator (31 chunks), skill_md (27), leaderboard_rubric (24)
```

---

## FUTURE: WHAT GETS AUTO-DETECTED

The KPI ontology is pre-loaded to detect things OoRava hinted at but haven't been built yet:

- **Game theory optimize** → `game_theory` KPI type (ROI 8.0) — ready
- **Voice agents** → `voice_agent` type (ROI 8.2) — ready  
- **Hyper-elite leads** → `lead_magnet` type (ROI 8.4) — ready
- **Tournament prize pools** → `tournament` type (ROI 9.0) — ready
- **YouTube playlist intelligence** → `youtube_intelligence` + `youtube_extractor.py` — ready

---
*OoRava Sovereign RAG Engine v1.0 | AuthurKing × C144 | Zero deps = maximum portability*
