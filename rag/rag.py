#!/usr/bin/env python3
"""
RAG.py — OoRava Sovereign RAG Engine
Pure stdlib (sqlite3 + TF-IDF) — zero external deps, fully portable.
Ingest any data type → chunk → vectorize → store → query → action replicator

Usage:
  python3 rag.py ingest <file_or_text>
  python3 rag.py query "<question>"
  python3 rag.py extract_kpis "<text_or_path>"
  python3 rag.py status
  python3 rag.py leaderboard
  python3 rag.py export_replicators
"""

import sqlite3, json, re, math, hashlib, os, sys, datetime, pathlib
from collections import Counter

WORKSPACE = pathlib.Path("/workspace")
DB_PATH = WORKSPACE / "rag/rag.db"
CHUNKS_DIR = WORKSPACE / "rag/chunks"
REPLICATORS_DIR = WORKSPACE / "rag/replicators"
TOP_K = 7  # default retrieval count

# ── KPI TAXONOMY — OoRava's value extraction ontology ──────────────────────────
KPI_ONTOLOGY = {
    "action_replicator": [
        r"replicate?", r"automat", r"workflow", r"system", r"pipeline",
        r"n8n", r"zapier", r"trigger", r"action", r"scrape", r"extract"
    ],
    "solana_nft": [
        r"solana", r"nft", r"mint", r"token", r"wallet", r"anchor",
        r"web3", r"blockchain", r"crypto", r"on.chain", r"smart contract"
    ],
    "groupchat_economy": [
        r"groupchat", r"group chat", r"telegram group", r"community",
        r"gated", r"access", r"member", r"subscription"
    ],
    "leaderboard_rubric": [
        r"rubric", r"leaderboard", r"score", r"rank", r"kpi",
        r"metric", r"benchmark", r"roi", r"performance"
    ],
    "data_farming": [
        r"data farm", r"harvest", r"collect", r"dataset", r"corpus",
        r"knowledge base", r"export", r"dump", r"archive"
    ],
    "tournament": [
        r"tournament", r"contest", r"competition", r"prize", r"winner",
        r"champion", r"challenge", r"entry fee"
    ],
    "youtube_intelligence": [
        r"youtube", r"playlist", r"video", r"channel", r"watch",
        r"subscribe", r"views", r"creator", r"content"
    ],
    "ai_agent": [
        r"agent", r"llm", r"gpt", r"claude", r"model", r"prompt",
        r"swarm", r"multi.agent", r"orchestrat"
    ],
    "revenue_model": [
        r"revenue", r"monetiz", r"billion", r"income", r"profit",
        r"sales", r"high.ticket", r"sell", r"offer", r"price"
    ],
    "spiritual_os": [
        r"meditation", r"consciousness", r"spiritual", r"divine",
        r"akashic", r"hermetic", r"zodiac", r"quantum", r"fractal"
    ],
    "skill_md": [
        r"skill\.md", r"skill file", r"replicant", r"soul", r"prompt",
        r"system prompt", r"persona", r"identity"
    ],
    "voice_agent": [
        r"voice", r"audio", r"tts", r"speech", r"call", r"phone",
        r"eleven.?labs", r"whisper", r"transcrib"
    ],
    "real_estate": [
        r"real estate", r"property", r"microacquisition", r"mortgage",
        r"listing", r"agent", r"deal", r"house"
    ],
    "lead_magnet": [
        r"lead", r"funnel", r"magnet", r"opt.in", r"email list",
        r"audience", r"prospect", r"hyper.elite"
    ],
    "game_theory": [
        r"game theory", r"nash", r"equilibrium", r"strategy",
        r"dominant", r"payoff", r"incentive", r"defect", r"cooperat"
    ],
}

# ROI weights by KPI type (Grover-aligned: high multiplier = surface first)
KPI_ROI_WEIGHT = {
    "action_replicator": 9.8, "solana_nft": 9.5, "leaderboard_rubric": 9.4,
    "groupchat_economy": 9.3, "data_farming": 9.2, "tournament": 9.0,
    "ai_agent": 8.9, "revenue_model": 8.8, "skill_md": 8.7,
    "youtube_intelligence": 8.5, "lead_magnet": 8.4, "voice_agent": 8.2,
    "game_theory": 8.0, "real_estate": 7.5, "spiritual_os": 7.0,
}

# ── DB SETUP ─────────────────────────────────────────────────────────────────
def init_db():
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    REPLICATORS_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS chunks (
            id TEXT PRIMARY KEY,
            source TEXT,
            source_type TEXT,
            content TEXT,
            kpi_tags TEXT,
            roi_score REAL,
            word_count INTEGER,
            tfidf_terms TEXT,
            created_at TEXT
        );
        CREATE TABLE IF NOT EXISTS replicators (
            id TEXT PRIMARY KEY,
            kpi_type TEXT,
            title TEXT,
            python_code TEXT,
            sql_query TEXT,
            roi_score REAL,
            usage_count INTEGER DEFAULT 0,
            created_at TEXT,
            last_used TEXT
        );
        CREATE TABLE IF NOT EXISTS ingestion_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            chunks_created INTEGER,
            kpis_found TEXT,
            replicators_created INTEGER,
            ingested_at TEXT
        );
        CREATE TABLE IF NOT EXISTS leaderboard (
            kpi_type TEXT PRIMARY KEY,
            chunk_count INTEGER,
            total_words INTEGER,
            avg_roi REAL,
            replicator_count INTEGER,
            last_updated TEXT
        );
    """)
    conn.commit()
    return conn

# ── TF-IDF VECTORIZER (pure stdlib) ──────────────────────────────────────────
def tokenize(text: str) -> list:
    text = re.sub(r'[^a-z0-9\s]', ' ', text.lower())
    return [w for w in text.split() if len(w) > 2]

def compute_tfidf(text: str, top_n: int = 50) -> dict:
    tokens = tokenize(text)
    if not tokens:
        return {}
    tf = Counter(tokens)
    total = len(tokens)
    # simplified IDF: log(1 + 1/freq_ratio) → rare terms score higher
    tfidf = {}
    for term, count in tf.items():
        tf_score = count / total
        idf = math.log(1 + (total / count))
        tfidf[term] = round(tf_score * idf, 6)
    top = sorted(tfidf.items(), key=lambda x: -x[1])[:top_n]
    return dict(top)

def cosine_similarity(vec_a: dict, vec_b: dict) -> float:
    if not vec_a or not vec_b:
        return 0.0
    common = set(vec_a) & set(vec_b)
    if not common:
        return 0.0
    dot = sum(vec_a[k] * vec_b[k] for k in common)
    mag_a = math.sqrt(sum(v**2 for v in vec_a.values()))
    mag_b = math.sqrt(sum(v**2 for v in vec_b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)

# ── KPI EXTRACTION ────────────────────────────────────────────────────────────
def extract_kpi_tags(text: str) -> list:
    """Classify text against KPI ontology. Returns sorted tags by ROI weight."""
    text_lower = text.lower()
    found = []
    for kpi_type, patterns in KPI_ONTOLOGY.items():
        hits = sum(1 for p in patterns if re.search(p, text_lower))
        if hits >= 2:  # require ≥2 pattern matches to qualify
            found.append((kpi_type, hits))
    # sort by ROI weight × hit count
    found.sort(key=lambda x: KPI_ROI_WEIGHT.get(x[0], 5.0) * x[1], reverse=True)
    return [f[0] for f in found]

def compute_roi_score(text: str, kpi_tags: list) -> float:
    """Grover-weighted ROI score for a chunk."""
    if not kpi_tags:
        base = 5.0
    else:
        # Weighted average of top 3 KPI types
        weights = [KPI_ROI_WEIGHT.get(t, 5.0) for t in kpi_tags[:3]]
        base = sum(weights) / len(weights)
    # Boost for length (more content = more value)
    words = len(text.split())
    length_boost = min(1.2, 1.0 + (words / 1000) * 0.2)
    # Boost for action-oriented language
    action_words = len(re.findall(r'\b(build|create|deploy|automate|generate|extract|replicate|mint|launch|scale)\b', text.lower()))
    action_boost = min(1.15, 1.0 + action_words * 0.015)
    return round(min(10.0, base * length_boost * action_boost), 2)

# ── CHUNKING ─────────────────────────────────────────────────────────────────
def chunk_text(text: str, chunk_size: int = 400, overlap: int = 80) -> list:
    """Split text into overlapping chunks by words."""
    words = text.split()
    if len(words) <= chunk_size:
        return [text]
    chunks = []
    i = 0
    while i < len(words):
        chunk = ' '.join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def chunk_by_section(text: str) -> list:
    """Also split by markdown headers/sections for structured data."""
    sections = re.split(r'\n#{1,4}\s+', text)
    chunks = []
    for section in sections:
        section = section.strip()
        if len(section.split()) < 20:
            continue
        if len(section.split()) > 400:
            chunks.extend(chunk_text(section))
        else:
            chunks.append(section)
    return chunks if chunks else chunk_text(text)

# ── REPLICATOR AUTO-GENERATOR ─────────────────────────────────────────────────
def auto_generate_replicator(kpi_type: str, chunk_content: str, roi_score: float) -> dict | None:
    """Generate a Python action replicator for high-value KPI chunks (ROI ≥ 8.5)."""
    if roi_score < 8.5:
        return None

    templates = {
        "youtube_intelligence": {
            "title": "YouTube Intelligence Extractor",
            "python_code": '''
def extract_youtube_kpis(url_or_playlist: str) -> dict:
    """Extract KPI data from YouTube video/playlist: title, description,
    key timestamps, high-ROI concepts, action items."""
    import urllib.request, re, json
    # Get video ID
    vid_match = re.search(r'(?:v=|youtu.be/|/embed/)([a-zA-Z0-9_-]{11})', url_or_playlist)
    if not vid_match:
        return {"error": "No video ID found"}
    vid_id = vid_match.group(1)
    # Fetch page for title + description
    url = f"https://www.youtube.com/watch?v={vid_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        title = re.search(r'"title":"([^"]+)"', html)
        desc = re.search(r'"shortDescription":"([^"]{0,500})"', html)
        return {
            "video_id": vid_id,
            "title": title.group(1) if title else "Unknown",
            "description": desc.group(1).replace("\\n", " ") if desc else "",
            "kpi_url": f"https://www.youtube.com/watch?v={vid_id}",
            "action": "review_for_replicators"
        }
    except Exception as e:
        return {"error": str(e)}
''',
            "sql_query": "SELECT * FROM chunks WHERE kpi_tags LIKE '%youtube_intelligence%' ORDER BY roi_score DESC;"
        },
        "action_replicator": {
            "title": "Action Replicator Generator",
            "python_code": '''
def generate_action_replicator(description: str, kpi_type: str) -> str:
    """Auto-generate a Python action replicator from a description."""
    slug = re.sub(r"[^a-z0-9]+", "_", description.lower()[:40]).strip("_")
    template = f"""
def replicate_{slug}(input_data: str) -> dict:
    \\"\\"\\"
    Action Replicator: {description}
    KPI Type: {kpi_type}
    Auto-generated by OoRava RAG Engine
    \\"\\"\\"
    # TODO: implement core logic here
    return {{"input": input_data, "status": "pending_implementation", "kpi": "{kpi_type}"}}
"""
    return template
''',
            "sql_query": "SELECT * FROM replicators ORDER BY roi_score DESC, usage_count DESC;"
        },
        "solana_nft": {
            "title": "Solana NFT Data Extractor",
            "python_code": '''
def extract_solana_nft_data(mint_address: str) -> dict:
    """Query Solana NFT metadata via Helius/RPC."""
    import urllib.request, json
    rpc_url = "https://api.mainnet-beta.solana.com"
    payload = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "getAccountInfo",
        "params": [mint_address, {"encoding": "base64"}]
    }).encode()
    req = urllib.request.Request(rpc_url, data=payload,
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}
''',
            "sql_query": "SELECT * FROM chunks WHERE kpi_tags LIKE '%solana_nft%' ORDER BY roi_score DESC;"
        },
        "leaderboard_rubric": {
            "title": "Rubric Leaderboard SQL Engine",
            "python_code": '''
def run_leaderboard_query(db_path: str, period: str = "weekly") -> list:
    """Run the Grover-weighted leaderboard query."""
    import sqlite3
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT handle, tier_name, equity_shares,
               ROUND(equity_shares/10000.0*100, 2) AS ownership_pct,
               points, avg_rubric_score, sol_earned,
               ROUND(SQRT(points) * avg_rubric_score * (1 + equity_shares/1000.0), 2) AS grover_score
        FROM leaderboard l JOIN members m ON l.member_id = m.id
        WHERE period = ? ORDER BY grover_score DESC
    """, (period,))
    return c.fetchall()
''',
            "sql_query": """
SELECT kpi_type, COUNT(*) as chunk_count, AVG(roi_score) as avg_roi
FROM chunks GROUP BY kpi_type ORDER BY avg_roi DESC;
"""
        },
    }

    template = templates.get(kpi_type, templates.get("action_replicator"))
    rep_id = hashlib.md5(f"{kpi_type}:{chunk_content[:100]}".encode()).hexdigest()[:8]
    return {
        "id": rep_id,
        "kpi_type": kpi_type,
        "title": template["title"],
        "python_code": template["python_code"],
        "sql_query": template["sql_query"],
        "roi_score": roi_score,
        "created_at": datetime.datetime.now().isoformat(),
        "last_used": None,
    }

# ── INGEST ────────────────────────────────────────────────────────────────────
def ingest(source: str, source_type: str = "auto") -> dict:
    """Ingest any text/file into the RAG. Auto-detects type."""
    # Resolve source
    if os.path.exists(source):
        path = pathlib.Path(source)
        raw_text = path.read_text(errors='ignore')
        source_name = path.name
        if source_type == "auto":
            ext = path.suffix.lower()
            source_type = {"md": "markdown", ".txt": "text", ".html": "html",
                          ".json": "json"}.get(ext, "text")
    else:
        raw_text = source
        source_name = f"inline_{hashlib.md5(source[:50].encode()).hexdigest()[:6]}"

    # Clean HTML if needed
    if source_type == "html":
        raw_text = re.sub(r'<[^>]+>', ' ', raw_text)
        raw_text = re.sub(r'&[a-z]+;', ' ', raw_text)

    raw_text = re.sub(r'\s+', ' ', raw_text).strip()

    # Chunk (prefer section-based for markdown)
    if source_type == "markdown":
        chunks = chunk_by_section(raw_text)
    else:
        chunks = chunk_text(raw_text)

    conn = init_db()
    c = conn.cursor()
    chunks_created = 0
    replicators_created = 0
    all_kpis = []

    for i, chunk in enumerate(chunks):
        if len(chunk.strip()) < 30:
            continue

        chunk_id = hashlib.md5(f"{source_name}:{i}:{chunk[:50]}".encode()).hexdigest()[:12]

        # Check duplicate
        if c.execute("SELECT 1 FROM chunks WHERE id=?", (chunk_id,)).fetchone():
            continue

        kpi_tags = extract_kpi_tags(chunk)
        roi_score = compute_roi_score(chunk, kpi_tags)
        tfidf = compute_tfidf(chunk)
        all_kpis.extend(kpi_tags)

        c.execute("""
            INSERT INTO chunks (id, source, source_type, content, kpi_tags,
                               roi_score, word_count, tfidf_terms, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            chunk_id, source_name, source_type, chunk,
            json.dumps(kpi_tags), roi_score, len(chunk.split()),
            json.dumps(tfidf), datetime.datetime.now().isoformat()
        ))
        chunks_created += 1

        # Auto-generate replicators for high-ROI chunks
        if roi_score >= 8.5 and kpi_tags:
            for kpi in kpi_tags[:2]:  # top 2 KPI types only
                rep = auto_generate_replicator(kpi, chunk, roi_score)
                if rep and not c.execute("SELECT 1 FROM replicators WHERE id=?", (rep["id"],)).fetchone():
                    c.execute("""
                        INSERT INTO replicators (id, kpi_type, title, python_code,
                                               sql_query, roi_score, created_at, last_used)
                        VALUES (?,?,?,?,?,?,?,?)
                    """, (rep["id"], rep["kpi_type"], rep["title"], rep["python_code"],
                          rep["sql_query"], rep["roi_score"], rep["created_at"], rep["last_used"]))
                    replicators_created += 1

    # Update leaderboard
    kpi_counter = Counter(all_kpis)
    for kpi, count in kpi_counter.items():
        c.execute("""
            INSERT INTO leaderboard (kpi_type, chunk_count, total_words, avg_roi,
                                    replicator_count, last_updated)
            VALUES (?,?,?,?,?,?)
            ON CONFLICT(kpi_type) DO UPDATE SET
                chunk_count = chunk_count + excluded.chunk_count,
                total_words = total_words + excluded.total_words,
                last_updated = excluded.last_updated
        """, (kpi, count, len(raw_text.split())//len(chunks) if chunks else 0,
              KPI_ROI_WEIGHT.get(kpi, 5.0), replicators_created,
              datetime.datetime.now().isoformat()))

    # Log ingestion
    c.execute("""
        INSERT INTO ingestion_log (source, chunks_created, kpis_found,
                                  replicators_created, ingested_at)
        VALUES (?,?,?,?,?)
    """, (source_name, chunks_created, json.dumps(list(set(all_kpis))),
          replicators_created, datetime.datetime.now().isoformat()))

    conn.commit()
    conn.close()

    return {
        "source": source_name,
        "chunks_created": chunks_created,
        "kpis_found": list(set(all_kpis)),
        "replicators_created": replicators_created,
        "status": "✅ ingested"
    }

# ── QUERY ─────────────────────────────────────────────────────────────────────
def query(question: str, top_k: int = TOP_K, kpi_filter: str = None) -> list:
    """Semantic search via TF-IDF cosine similarity."""
    conn = init_db()
    c = conn.cursor()

    q_vec = compute_tfidf(question)

    if kpi_filter:
        rows = c.execute(
            "SELECT id, source, content, kpi_tags, roi_score, tfidf_terms FROM chunks WHERE kpi_tags LIKE ?",
            (f'%{kpi_filter}%',)
        ).fetchall()
    else:
        rows = c.execute(
            "SELECT id, source, content, kpi_tags, roi_score, tfidf_terms FROM chunks"
        ).fetchall()

    conn.close()

    if not rows:
        return []

    results = []
    for row in rows:
        chunk_id, source, content, kpi_tags_str, roi_score, tfidf_str = row
        try:
            chunk_vec = json.loads(tfidf_str)
        except:
            continue
        sim = cosine_similarity(q_vec, chunk_vec)
        # Grover boost: sim * sqrt(roi_score)
        grover_score = sim * math.sqrt(roi_score)
        results.append({
            "id": chunk_id,
            "source": source,
            "content": content[:300] + ("..." if len(content) > 300 else ""),
            "kpi_tags": json.loads(kpi_tags_str),
            "roi_score": roi_score,
            "similarity": round(sim, 4),
            "grover_score": round(grover_score, 4),
        })

    results.sort(key=lambda x: -x["grover_score"])
    return results[:top_k]

# ── LEADERBOARD ────────────────────────────────────────────────────────────────
def get_leaderboard() -> list:
    conn = init_db()
    c = conn.cursor()
    rows = c.execute("""
        SELECT l.kpi_type, l.chunk_count, l.avg_roi, l.replicator_count,
               COUNT(r.id) as actual_reps
        FROM leaderboard l
        LEFT JOIN replicators r ON r.kpi_type = l.kpi_type
        GROUP BY l.kpi_type
        ORDER BY l.avg_roi DESC
    """).fetchall()
    conn.close()
    return rows

def get_status() -> dict:
    conn = init_db()
    c = conn.cursor()
    total_chunks = c.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    total_reps = c.execute("SELECT COUNT(*) FROM replicators").fetchone()[0]
    avg_roi = c.execute("SELECT AVG(roi_score) FROM chunks").fetchone()[0] or 0
    sources = c.execute("SELECT COUNT(DISTINCT source) FROM chunks").fetchone()[0]
    recent = c.execute("SELECT source, ingested_at FROM ingestion_log ORDER BY id DESC LIMIT 5").fetchall()
    conn.close()
    return {
        "total_chunks": total_chunks,
        "total_replicators": total_reps,
        "avg_roi": round(avg_roi, 2),
        "unique_sources": sources,
        "recent_ingestions": recent,
    }

# ── EXPORT REPLICATORS ────────────────────────────────────────────────────────
def export_replicators() -> str:
    conn = init_db()
    c = conn.cursor()
    reps = c.execute("SELECT * FROM replicators ORDER BY roi_score DESC").fetchall()
    conn.close()
    output = ["# ACTION REPLICATORS — Auto-generated by OoRava RAG Engine\n"]
    for rep in reps:
        rid, kpi_type, title, python_code, sql_query, roi_score, usage, created_at, last_used = rep
        output.append(f"\n## [{rid}] {title} | KPI: {kpi_type} | ROI: {roi_score}")
        output.append(f"```python{python_code}```")
        output.append(f"\nSQL:\n```sql\n{sql_query}\n```\n")
    result = '\n'.join(output)
    out_path = REPLICATORS_DIR / "exported_replicators.md"
    out_path.write_text(result)
    return str(out_path)

# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "ingest" and len(sys.argv) > 2:
        source = " ".join(sys.argv[2:])
        result = ingest(source)
        print(json.dumps(result, indent=2))

    elif cmd == "query" and len(sys.argv) > 2:
        q = " ".join(sys.argv[2:])
        results = query(q)
        for i, r in enumerate(results, 1):
            print(f"\n[{i}] Score: {r['grover_score']} | ROI: {r['roi_score']} | {r['source']}")
            print(f"    KPIs: {', '.join(r['kpi_tags'][:3])}")
            print(f"    {r['content'][:200]}")

    elif cmd == "leaderboard":
        rows = get_leaderboard()
        print(f"\n{'KPI Type':<25} {'Chunks':>6} {'ROI':>6} {'Replicators':>12}")
        print("─" * 55)
        for row in rows:
            kpi, chunks, roi, _, reps = row
            print(f"{kpi:<25} {chunks:>6} {roi:>6.1f} {reps:>12}")

    elif cmd == "status":
        s = get_status()
        print(f"\n⚡ OoRava RAG Engine Status")
        print(f"   Chunks:       {s['total_chunks']}")
        print(f"   Replicators:  {s['total_replicators']}")
        print(f"   Avg ROI:      {s['avg_roi']}")
        print(f"   Sources:      {s['unique_sources']}")

    elif cmd == "export_replicators":
        path = export_replicators()
        print(f"✅ Exported to: {path}")

    elif cmd == "ingest_all":
        # Bulk ingest all processed vault files + genepools skills
        dirs = [
            WORKSPACE / "vault/processed",
            WORKSPACE / "vault/oorava-quest-billion",
            WORKSPACE / "genepools/skills",
            WORKSPACE / "souls/oorava",
        ]
        total = {"chunks": 0, "reps": 0, "sources": 0}
        for d in dirs:
            for f in pathlib.Path(d).rglob("*.md"):
                result = ingest(str(f), "markdown")
                total["chunks"] += result["chunks_created"]
                total["reps"] += result["replicators_created"]
                total["sources"] += 1
                if result["chunks_created"] > 0:
                    print(f"✅ {f.name}: {result['chunks_created']} chunks, KPIs: {result['kpis_found'][:3]}")
        print(f"\n🏆 Total: {total['sources']} sources, {total['chunks']} chunks, {total['reps']} replicators")

    else:
        print(__doc__)
