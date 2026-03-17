#!/usr/bin/env python3
"""
VAULT SYNC — MD file exchange system
Drop MDs into /workspace/vault/incoming/ → this indexes, links, and stores them.
Self-contained. Zero internet needed. Feels like 21st.dev but local.

Usage:
  python3 vault_sync.py ingest          # Process all incoming MDs
  python3 vault_sync.py status          # Show vault state
  python3 vault_sync.py export <tag>    # Export MDs matching tag
  python3 vault_sync.py mindmap         # Print current mindmap
"""
import os, json, re, hashlib, shutil
from pathlib import Path
from datetime import datetime, timezone

VAULT = Path("/workspace/vault")
INCOMING = VAULT / "incoming"
PROCESSED = VAULT / "processed"
OBSIDIAN = VAULT / "obsidian"
INDEX_FILE = VAULT / "index.json"

def load_index():
    return json.loads(INDEX_FILE.read_text()) if INDEX_FILE.exists() else {"docs": {}, "tags": {}, "links": {}}

def save_index(idx):
    INDEX_FILE.write_text(json.dumps(idx, indent=2))

def extract_frontmatter(content):
    """Extract tags, title, links from MD content"""
    tags = re.findall(r'#(\w+)', content)
    tags += re.findall(r'^tags?:\s*\[([^\]]+)\]', content, re.MULTILINE)
    title_m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_m.group(1) if title_m else "Untitled"
    links = re.findall(r'\[\[([^\]]+)\]\]', content)  # obsidian-style links
    return {"title": title, "tags": list(set(tags)), "links": links}

def ingest():
    idx = load_index()
    ingested = []
    for f in INCOMING.glob("*.md"):
        content = f.read_text()
        meta = extract_frontmatter(content)
        doc_id = hashlib.md5(content.encode()).hexdigest()[:8]
        now = datetime.now(timezone.utc).isoformat()
        
        # Store in processed
        dest = PROCESSED / f.name
        shutil.copy2(f, dest)
        
        # Copy to obsidian vault
        obs_dest = OBSIDIAN / f.name
        shutil.copy2(f, obs_dest)
        
        # Index it
        idx["docs"][doc_id] = {
            "file": f.name, "title": meta["title"],
            "tags": meta["tags"], "links": meta["links"],
            "ingested": now, "size": len(content)
        }
        for tag in meta["tags"]:
            idx["tags"].setdefault(tag, []).append(doc_id)
        
        f.unlink()  # Remove from incoming
        ingested.append(f.name)
    
    save_index(idx)
    print(f"✅ Ingested {len(ingested)} files: {ingested}")
    return ingested

def status():
    idx = load_index()
    docs = idx["docs"]
    tags = idx["tags"]
    print(f"📚 VAULT STATUS")
    print(f"  Total docs: {len(docs)}")
    print(f"  Tags: {list(tags.keys())[:20]}")
    print(f"  Incoming queue: {len(list(INCOMING.glob('*.md')))}")
    for did, d in list(docs.items())[-5:]:
        print(f"  └─ {d['title']} [{', '.join(d['tags'][:3])}]")

def mindmap():
    idx = load_index()
    print("🗺️ MINDMAP")
    for tag, doc_ids in idx["tags"].items():
        titles = [idx["docs"][d]["title"][:30] for d in doc_ids if d in idx["docs"]]
        print(f"  #{tag} → {' | '.join(titles)}")

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "ingest": ingest()
    elif cmd == "mindmap": mindmap()
    else: status()
