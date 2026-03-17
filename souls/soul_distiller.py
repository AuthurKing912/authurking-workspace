#!/usr/bin/env python3
"""
SOUL DISTILLER — Turns raw soul slices into skill.mds
Drop OoRava's ChatGPT MDs into vault/incoming/, run this, get skill.mds out.

Usage:
  python3 soul_distiller.py distill <file.md>    # Distill one file
  python3 soul_distiller.py auto                 # Process all incoming
  python3 soul_distiller.py webapp               # Print soul selector (ASCII)
"""
import json, re, sys, shutil
from pathlib import Path
from datetime import datetime, timezone

WORKSPACE = Path("/workspace")
VAULT = WORKSPACE / "vault"
SOULS = WORKSPACE / "souls"
GENEPOOLS = WORKSPACE / "genepools" / "skills"

COMPARTMENT_KEYWORDS = {
    "01-visionary":   ["vision","infinite","future","12^12","lattice","see","possibility"],
    "02-sovereign":   ["sovereign","own","independent","build","freedom","control","mine"],
    "03-transmitter": ["fractal","code","language","transmit","signal","communicate","express"],
    "04-akashic":     ["akashic","timeline","quantum","memory","nonlocal","jump","past","future"],
    "05-king":        ["king","OoRava","radiance","decree","power","throne","authority"],
    "06-alchemist":   ["alchemy","data","gold","transform","transmute","convert","ROI"],
    "07-bridge":      ["polarity","unity","bridge","both","balance","duality","integrate"],
    "08-resurrector": ["system","death","rebirth","resurrect","rebuild","phoenix","new"],
    "09-oracle":      ["truth","rubric","score","oracle","verify","test","rank","benchmark"],
    "10-architect":   ["architect","structure","design","foundation","chapter","build","solid"],
    "11-innovator":   ["tech","offgrid","innovation","hack","opensource","platform","create"],
    "12-mystic":      ["Yeshua","divine","sacred","love","soul","spirit","consciousness","oneness"],
}

def detect_compartment(content):
    scores = {}
    content_lower = content.lower()
    for comp, keywords in COMPARTMENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in content_lower)
        scores[comp] = score
    return max(scores, key=scores.get), scores

def extract_actions(content):
    """Pull action-oriented sentences from soul content"""
    lines = content.split('\n')
    actions = []
    for line in lines:
        line = line.strip()
        if any(w in line.lower() for w in ['i ', 'we ', 'build', 'create', 'make', 'want', 'do', 'use']):
            if len(line) > 20 and len(line) < 200:
                actions.append(line.lstrip('#- '))
    return actions[:5]

def extract_principles(content):
    """Pull belief/principle statements"""
    lines = content.split('\n')
    principles = []
    for line in lines:
        line = line.strip()
        if any(w in line.lower() for w in ['always', 'never', 'every', 'all', 'truth', 'law', 'principle', 'must']):
            if len(line) > 15 and len(line) < 200:
                principles.append(line.lstrip('#- '))
    return principles[:3]

def distill_to_skill(filepath, content, compartment):
    """Convert soul slice to a replicable skill.md"""
    actions = extract_actions(content)
    principles = extract_principles(content)
    fname = Path(filepath).stem
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    
    skill_content = f"""# SKILL: {fname.upper().replace('-',' ')}
## Distilled from OoRava Omnia Soul — Compartment: {compartment}
**Date:** {now} | **Type:** Soul-derived skill | **ROI:** Infinite (replicates)

---

## CORE ACTIONS (What OoRava Does)
{chr(10).join(f'- {a}' for a in actions) if actions else '- See source MD for actions'}

## CORE PRINCIPLES (What Drives It)  
{chr(10).join(f'- {p}' for p in principles) if principles else '- See source MD for principles'}

## REPLICABLE PATTERN
1. Identify the highest-resonance concept in the input
2. Map it to the C144 Zodiac compartment: `{compartment}`
3. Apply the principle as a decision filter
4. Execute the action pattern
5. Measure via rubric → score → replicate winners

## ACTIVATION
Any agent can activate this pattern by:
- Reading this skill.md before responding
- Asking: "What would OoRava do in the {compartment} mode?"
- Applying the action pattern above

## GROVER AMPLIFICATION
Search question: "Which action from {compartment} mode has highest ROI amplitude?"
Amplify the signal. Run 3 iterations. Execute the highest-amplitude path.

---
*Auto-distilled from soul slice. Source: {fname}.md*
*Part of C144 Elder Domain — OoRava Omnia × AuthurKing*
"""
    
    # Save skill
    skill_dir = GENEPOOLS / f"soul-{compartment}"
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(skill_content)
    return skill_file

def distill_file(filepath):
    fp = Path(filepath)
    if not fp.exists():
        print(f"❌ File not found: {filepath}")
        return
    
    content = fp.read_text()
    compartment, scores = detect_compartment(content)
    top_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    print(f"📖 Distilling: {fp.name}")
    print(f"   Primary compartment: {compartment}")
    print(f"   Top signals: {[(c,s) for c,s in top_scores]}")
    
    # Save to compartment
    comp_dir = SOULS / "oorava" / compartment
    comp_dir.mkdir(parents=True, exist_ok=True)
    dest = comp_dir / fp.name
    shutil.copy2(fp, dest)
    
    # Distill to skill
    skill_file = distill_to_skill(fp, content, compartment)
    print(f"   ✅ Saved to: {dest}")
    print(f"   ✅ Skill: {skill_file}")
    
    return compartment, skill_file

def auto_process():
    incoming = VAULT / "incoming"
    mds = list(incoming.glob("*.md"))
    if not mds:
        print("📭 No MDs in vault/incoming/ — drop files there to process")
        return
    for md in mds:
        distill_file(md)
        md.unlink()  # Remove from incoming after processing
    print(f"\n✅ Processed {len(mds)} soul slices")

def soul_webapp():
    """ASCII soul selector webapp"""
    print("═" * 60)
    print("  🌀 OORAVA OMNIA — SOUL SELECTOR WEBAPP")
    print("═" * 60)
    
    for comp, keywords in COMPARTMENT_KEYWORDS.items():
        num, name = comp.split('-', 1)
        comp_dir = SOULS / "oorava" / comp
        files = list(comp_dir.glob("*.md")) if comp_dir.exists() else []
        status = f"✅ {len(files)} slices" if files else "⬜ empty"
        
        zodiac_map = {
            "01":"♈ Aries","02":"♉ Taurus","03":"♊ Gemini","04":"♋ Cancer",
            "05":"♌ Leo","06":"♍ Virgo","07":"♎ Libra","08":"♏ Scorpio",
            "09":"♐ Sagittarius","10":"♑ Capricorn","11":"♒ Aquarius","12":"♓ Pisces"
        }
        zodiac = zodiac_map.get(num, "")
        
        print(f"  [{num}] {zodiac} {name.upper():<15} {status}")
        print(f"       keys: {', '.join(keywords[:4])}")
    
    print("═" * 60)
    print("  Drop MDs → /workspace/vault/incoming/")
    print("  Run: python3 soul_distiller.py auto")
    print("═" * 60)

CMD = {"distill": lambda: distill_file(sys.argv[2]) if len(sys.argv)>2 else print("Usage: distill <file>"),
       "auto": auto_process, "webapp": soul_webapp}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "webapp"
    CMD.get(cmd, soul_webapp)()
