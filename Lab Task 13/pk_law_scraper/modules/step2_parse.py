"""
Step 2 — Parse all 1030 seed JSON files from the cloned repo
Extracts: law metadata + all provisions/sections + punishment text
"""

import os
import re
import json
import sys

SEED_DIR = "./Pakistani-law-mcp/data/seed"


def parse_seed_files():
    print("\n[STEP 2] Parsing seed JSON files...")

    if not os.path.exists(SEED_DIR):
        print(f"  ❌ Seed directory not found: {SEED_DIR}")
        print("  Did Step 1 (clone) succeed?")
        sys.exit(1)

    files = sorted([f for f in os.listdir(SEED_DIR) if f.endswith(".json")])
    print(f"  Found {len(files)} JSON files")

    laws         = []   # law-level metadata
    sections     = []   # all provisions/sections flat
    all_raw      = []   # full raw JSON for master file

    for i, fname in enumerate(files, 1):
        fpath = os.path.join(SEED_DIR, fname)
        try:
            with open(fpath, encoding="utf-8") as f:
                d = json.load(f)
        except Exception as e:
            print(f"  ⚠️  Skipping {fname}: {e}")
            continue

        all_raw.append(d)

        # ── law metadata ─────────────────────────────────────────
        law = {
            "id":             d.get("id", ""),
            "title":          d.get("title", ""),
            "short_name":     d.get("short_name", ""),
            "year":           (d.get("issued_date", "") or "")[:4],
            "status":         d.get("status", ""),
            "issued_date":    d.get("issued_date", ""),
            "in_force_date":  d.get("in_force_date", ""),
            "source_url":     d.get("url", ""),
            "description":    (d.get("description", "") or "").replace("\n", " "),
            "num_provisions": len(d.get("provisions", [])),
            "source_file":    fname,
        }
        laws.append(law)

        # ── provisions/sections ───────────────────────────────────
        for p in d.get("provisions", []):
            content = p.get("content", "") or ""

            # extract punishment clause using regex
            pun = re.search(
                r'(shall be punish|punishable|imprisonment|fine of|shall pay)[^\n]{0,300}',
                content, re.IGNORECASE
            )

            sections.append({
                "law_id":          law["id"],
                "law_title":       law["title"],
                "section_number":  p.get("section", ""),
                "provision_ref":   p.get("provision_ref", ""),
                "title":           p.get("title", ""),
                "content":         content.replace("\n", " ").strip(),
                "punishment_text": pun.group(0).strip() if pun else "",
            })

        if i % 200 == 0:
            print(f"  Parsed {i}/{len(files)}...")

    print(f"  ✅ Laws: {len(laws)}  |  Sections: {len(sections)}")
    return laws, sections, all_raw
