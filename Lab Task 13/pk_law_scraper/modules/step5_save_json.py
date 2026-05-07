"""
Step 5 — Save JSON Files
Outputs: all_laws_master.json, laws_index.json,
         agencies_contacts.json, offense_to_section.json
"""

import json
import os


def save_json(laws, sections, all_raw, agencies, offense_map, output_dir):
    print("\n[STEP 5] Saving JSON files...")
    out = f"{output_dir}/json"
    os.makedirs(out, exist_ok=True)

    # all_laws_master.json — full raw text of every law
    path = f"{out}/all_laws_master.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(all_raw, f, indent=2, ensure_ascii=False)
    size = os.path.getsize(path) / (1024 * 1024)
    print(f"  ✅ all_laws_master.json  ({len(all_raw)} laws, {size:.1f} MB)")

    # laws_index.json — lightweight metadata only
    path = f"{out}/laws_index.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(laws, f, indent=2, ensure_ascii=False)
    print(f"  ✅ laws_index.json  ({len(laws)} records)")

    # agencies_contacts.json
    path = f"{out}/agencies_contacts.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(agencies, f, indent=2, ensure_ascii=False)
    print(f"  ✅ agencies_contacts.json  ({len(agencies)} agencies)")

    # offense_to_section.json
    path = f"{out}/offense_to_section.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(offense_map, f, indent=2, ensure_ascii=False)
    print(f"  ✅ offense_to_section.json  ({len(offense_map)} offenses)")
