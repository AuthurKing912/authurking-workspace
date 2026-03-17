#!/usr/bin/env python3
"""
youtube_extractor.py — YouTube Intelligence Replicator
Extract high-ROI KPI data from any YouTube video or playlist.
Standalone, zero external deps (urllib only).

Usage:
  python3 youtube_extractor.py video <url>
  python3 youtube_extractor.py playlist <url>
  python3 youtube_extractor.py ingest_to_rag <url>

Auto-detects and extracts:
  - Title, description, chapter timestamps
  - Implied action replicators from content themes
  - KPI classification against OoRava ontology
  - Inserts into RAG engine (rag.py) automatically
"""

import sys, re, json, urllib.request, pathlib, hashlib, datetime

WORKSPACE = pathlib.Path("/workspace")
RAG_SCRIPT = WORKSPACE / "rag/rag.py"

def get_video_data(url: str) -> dict:
    """Fetch YouTube video metadata via public page scrape."""
    vid_match = re.search(r'(?:v=|youtu\.be/|/embed/)([a-zA-Z0-9_-]{11})', url)
    if not vid_match:
        return {"error": f"No video ID in URL: {url}"}
    vid_id = vid_match.group(1)

    req_url = f"https://www.youtube.com/watch?v={vid_id}"
    req = urllib.request.Request(req_url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; OoRava/1.0; +https://github.com/AuthurKing912)"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return {"error": str(e), "video_id": vid_id}

    # Extract metadata
    title_m = re.search(r'"title":"([^"]{1,200})"', html)
    desc_m = re.search(r'"shortDescription":"((?:[^"\\]|\\.)*)\"', html)
    duration_m = re.search(r'"lengthSeconds":"(\d+)"', html)
    channel_m = re.search(r'"ownerChannelName":"([^"]{1,100})"', html)
    views_m = re.search(r'"viewCount":"(\d+)"', html)
    likes_m = re.search(r'"label":"(\d[\d,]+) likes"', html)

    # Extract chapters from description
    raw_desc = desc_m.group(1).replace('\\n', '\n').replace('\\"', '"') if desc_m else ""
    chapters = re.findall(r'(\d{1,2}:\d{2}(?::\d{2})?)\s*[-–—]?\s*(.+)', raw_desc[:2000])

    # Clean title
    title = title_m.group(1).replace('\\u0026', '&') if title_m else "Unknown"

    duration_secs = int(duration_m.group(1)) if duration_m else 0
    duration_fmt = f"{duration_secs//3600}h{(duration_secs%3600)//60}m" if duration_secs > 3600 else f"{duration_secs//60}m{duration_secs%60}s"

    # KPI classify based on title + description
    kpi_signals = {
        "action_replicator": ["automat", "workflow", "system", "replicate", "pipeline", "n8n"],
        "solana_nft": ["solana", "nft", "blockchain", "crypto", "web3", "mint"],
        "ai_agent": ["agent", "ai", "llm", "gpt", "model", "prompt", "swarm"],
        "revenue_model": ["billion", "revenue", "income", "sell", "sales", "high ticket"],
        "youtube_intelligence": ["youtube", "channel", "playlist", "creator", "content"],
        "voice_agent": ["voice", "tts", "speech", "call", "eleven"],
        "real_estate": ["real estate", "property", "microacquisition"],
        "skill_md": ["skill", "system prompt", "persona", "identity"],
    }

    content = f"{title} {raw_desc}".lower()
    detected_kpis = [kpi for kpi, sigs in kpi_signals.items()
                     if sum(1 for s in sigs if s in content) >= 1]

    return {
        "video_id": vid_id,
        "url": req_url,
        "title": title,
        "channel": channel_m.group(1) if channel_m else "Unknown",
        "duration": duration_fmt,
        "views": views_m.group(1) if views_m else "N/A",
        "description_preview": raw_desc[:400],
        "chapters": chapters[:20],
        "detected_kpis": detected_kpis,
        "rag_content": f"YouTube: {title}\nChannel: {channel_m.group(1) if channel_m else 'Unknown'}\nDuration: {duration_fmt}\n\nDescription:\n{raw_desc[:1500]}\n\nChapters:\n" + "\n".join(f"{c[0]} {c[1]}" for c in chapters[:20]),
    }

def get_playlist_data(url: str) -> list:
    """Extract video list from a YouTube playlist."""
    list_m = re.search(r'list=([a-zA-Z0-9_-]+)', url)
    if not list_m:
        return [{"error": "No playlist ID found"}]
    pl_id = list_m.group(1)

    req_url = f"https://www.youtube.com/playlist?list={pl_id}"
    req = urllib.request.Request(req_url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; OoRava/1.0)"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return [{"error": str(e)}]

    # Extract video IDs and titles from playlist page
    vid_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
    vid_titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]{1,200})"', html)

    # Deduplicate while preserving order
    seen = set()
    videos = []
    for i, vid_id in enumerate(vid_ids):
        if vid_id not in seen:
            seen.add(vid_id)
            title = vid_titles[i] if i < len(vid_titles) else f"Video {i+1}"
            videos.append({
                "video_id": vid_id,
                "title": title,
                "url": f"https://www.youtube.com/watch?v={vid_id}",
                "playlist_position": len(videos) + 1,
            })

    pl_title_m = re.search(r'"title":"([^"]{1,200})","description"', html)
    return {
        "playlist_id": pl_id,
        "playlist_title": pl_title_m.group(1) if pl_title_m else "Unknown Playlist",
        "video_count": len(videos),
        "videos": videos[:50],  # cap at 50
    }

def ingest_to_rag(url: str) -> dict:
    """Extract YouTube data and ingest into RAG engine."""
    import subprocess

    if "playlist" in url or "list=" in url:
        playlist_data = get_playlist_data(url)
        results = []
        for vid in playlist_data.get("videos", [])[:10]:  # first 10 for now
            vid_data = get_video_data(vid["url"])
            if "error" not in vid_data and vid_data.get("rag_content"):
                r = subprocess.run(
                    ["python3", str(RAG_SCRIPT), "ingest", vid_data["rag_content"]],
                    capture_output=True, text=True
                )
                results.append({"video": vid_data["title"], "result": r.stdout.strip()[:100]})
        return {"playlist": playlist_data.get("playlist_title"), "ingested": results}
    else:
        vid_data = get_video_data(url)
        if "error" in vid_data:
            return vid_data
        r = subprocess.run(
            ["python3", str(RAG_SCRIPT), "ingest", vid_data["rag_content"]],
            capture_output=True, text=True
        )
        return {"video": vid_data["title"], "kpis": vid_data["detected_kpis"],
                "rag_result": r.stdout.strip()}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    url = sys.argv[2] if len(sys.argv) > 2 else ""

    if cmd == "video" and url:
        data = get_video_data(url)
        print(json.dumps(data, indent=2))
    elif cmd == "playlist" and url:
        data = get_playlist_data(url)
        print(f"Playlist: {data.get('playlist_title')} ({data.get('video_count')} videos)")
        for v in data.get("videos", [])[:10]:
            print(f"  [{v['playlist_position']}] {v['title']}")
    elif cmd == "ingest_to_rag" and url:
        result = ingest_to_rag(url)
        print(json.dumps(result, indent=2))
    else:
        print(__doc__)
