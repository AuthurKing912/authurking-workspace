#!/usr/bin/env python3
"""
ALCHEMY TUMBLR ENGINE — Self-replicating KPI Leaderboard MindMap
Drop in a snippet → it multiplies into rubric questions, lead magnets, trend posts.
Grover-amplified: highest-signal paths surface first.

Usage:
  python3 alchemy_tumblr.py seed "<your snippet>"    # Plant a seed
  python3 alchemy_tumblr.py grow                     # Grow all seeds
  python3 alchemy_tumblr.py leaderboard              # Show rankings
  python3 alchemy_tumblr.py mindmap                  # Visual map
  python3 alchemy_tumblr.py export                   # Export for publishing
"""
import json, hashlib, re, sys
from pathlib import Path
from datetime import datetime, timezone

BASE = Path("/workspace/genepools/alchemy-tumblr")
BASE.mkdir(parents=True, exist_ok=True)
SEEDS_FILE = BASE / "seeds.json"
LEADERBOARD_FILE = BASE / "leaderboard.json"

# ─── REPLICATOR TEMPLATES ───────────────────────────────────────
REPLICATORS = {
    "rubric_question": "On a scale of 1-10, how well does [{topic}] maximize ROI in [{domain}]?",
    "lead_magnet":     "🔥 FREE: The [{topic}] framework that top [{domain}] experts use. [LINK]",
    "kpi_metric":      "KPI: Track [{topic}] velocity weekly. Benchmark: top 10% score >{threshold}.",
    "trend_post":      "🚀 [{topic}] is the #{keyword} of {year}. Here's why it compounds: [{reason}]",
    "action_replicator":"DO THIS: [{action}] → measure [{metric}] → if score>{threshold}: replicate. Else: mutate.",
    "sql_rubric":      "SELECT * FROM leaderboard WHERE topic='{topic}' ORDER BY roi_score DESC LIMIT 10;",
    "grover_query":    "AMPLIFY: Which [{topic}] path has highest amplitude in [{domain}] space? Run 3 iterations.",
    "nft_gate":        "🔒 [{topic}] Mastery NFT — holders get: [{benefit1}] + [{benefit2}] + leaderboard rank.",
    "viral_hook":      "Nobody talks about [{topic}] in [{domain}] but it's the highest ROI move. Thread 🧵:",
}

DOMAINS = ["AI/ML", "crypto", "Python", "groupchats", "leaderboards", "consciousness", "quantum", "data"]
KEYWORDS = ["Web3", "AI", "opensource", "sovereignty", "fractal", "compounding", "ROI", "hermetic"]

def load_seeds():
    return json.loads(SEEDS_FILE.read_text()) if SEEDS_FILE.exists() else []

def save_seeds(seeds):
    SEEDS_FILE.write_text(json.dumps(seeds, indent=2))

def load_board():
    return json.loads(LEADERBOARD_FILE.read_text()) if LEADERBOARD_FILE.exists() else []

def save_board(board):
    LEADERBOARD_FILE.write_text(json.dumps(board, indent=2))

def extract_concepts(snippet):
    """Extract keywords/topics from a snippet"""
    words = re.findall(r'\b[A-Z][a-z]+|[a-z]{4,}\b', snippet)
    return list(set(words))[:5]

def grover_score(item):
    """Simulate Grover amplitude: score = sqrt(signal) * domain_multiplier"""
    signal = len(item.get("replications", [])) + item.get("upvotes", 0) + 1
    return round(signal ** 0.5 * 10, 2)

def seed(snippet):
    seeds = load_seeds()
    sid = hashlib.md5(snippet.encode()).hexdigest()[:6]
    concepts = extract_concepts(snippet)
    entry = {
        "id": sid,
        "snippet": snippet,
        "concepts": concepts,
        "planted": datetime.now(timezone.utc).isoformat(),
        "replications": [],
        "upvotes": 0,
        "grover_score": 0
    }
    seeds.append(entry)
    save_seeds(seeds)
    print(f"🌱 Seeded [{sid}]: {snippet[:60]}...")
    print(f"   Concepts: {concepts}")

def grow():
    seeds = load_seeds()
    board = load_board()
    now = datetime.now(timezone.utc)
    
    for s in seeds:
        if s.get("grown"): continue
        topic = s["concepts"][0] if s["concepts"] else "topic"
        domain = DOMAINS[len(s["id"]) % len(DOMAINS)]
        keyword = KEYWORDS[len(s["id"]) % len(KEYWORDS)]
        
        replications = []
        for rtype, template in REPLICATORS.items():
            try:
                rep = template.format(
                    topic=topic, domain=domain, keyword=keyword,
                    year=now.year, threshold="7.5",
                    action=f"implement {topic}", metric=f"{topic}_score",
                    reason=f"compounds at 12x per cycle",
                    benefit1=f"{topic} mastery guide",
                    benefit2="leaderboard access"
                )
                replications.append({"type": rtype, "content": rep})
            except: pass
        
        s["replications"] = replications
        s["grover_score"] = grover_score(s)
        s["grown"] = now.isoformat()
        
        board.append({
            "id": s["id"], "topic": topic, "domain": domain,
            "score": s["grover_score"], "replications": len(replications),
            "snippet": s["snippet"][:80]
        })
    
    save_seeds(seeds)
    board.sort(key=lambda x: x["score"], reverse=True)
    save_board(board)
    print(f"🌿 Grew {len(seeds)} seeds into {sum(len(s.get('replications',[])) for s in seeds)} replications")

def leaderboard():
    board = load_board()
    if not board:
        print("Empty — plant seeds first: python3 alchemy_tumblr.py seed 'your idea'")
        return
    print("🏆 ALCHEMY LEADERBOARD (Grover-ranked)")
    print(f"{'Rank':<5} {'Score':<8} {'Topic':<15} {'Domain':<12} {'Reps':<6} Snippet")
    print("─" * 80)
    for i, item in enumerate(board[:20], 1):
        print(f"{i:<5} {item['score']:<8} {item['topic'][:14]:<15} {item['domain'][:11]:<12} {item['replications']:<6} {item['snippet'][:35]}")

def mindmap():
    seeds = load_seeds()
    print("🗺️ ALCHEMY MINDMAP")
    print("=" * 60)
    for s in seeds[:10]:
        print(f"\n◆ [{s['id']}] {s['snippet'][:50]}")
        print(f"  Concepts: {' · '.join(s['concepts'])}")
        for r in s.get("replications", [])[:3]:
            print(f"  └─ {r['type']}: {r['content'][:60]}")
        print(f"  Grover Score: {s.get('grover_score', 0)}")

def export_posts():
    seeds = load_seeds()
    output = []
    for s in seeds:
        for r in s.get("replications", []):
            if r["type"] in ["viral_hook", "lead_magnet", "trend_post"]:
                output.append({"type": r["type"], "content": r["content"], "source_id": s["id"]})
    out_file = BASE / "export_posts.json"
    out_file.write_text(json.dumps(output, indent=2))
    print(f"📤 Exported {len(output)} posts → {out_file}")
    for p in output[:5]:
        print(f"\n[{p['type']}] {p['content']}")

CMD_MAP = {"seed": seed, "grow": grow, "leaderboard": leaderboard, "mindmap": mindmap, "export": export_posts}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "mindmap"
    if cmd == "seed" and len(sys.argv) > 2:
        seed(" ".join(sys.argv[2:]))
    elif cmd in CMD_MAP:
        CMD_MAP[cmd]()
    else:
        print("Commands: seed <text> | grow | leaderboard | mindmap | export")
