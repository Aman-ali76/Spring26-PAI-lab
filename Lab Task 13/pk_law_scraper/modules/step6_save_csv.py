"""
Step 6 — Save CSV Files
Outputs: laws_catalogue.csv, sections_all.csv,
         agencies_contacts.csv, offense_to_section.csv
"""

import csv
import json
import os


def save_csv(laws, sections, agencies, offense_map, output_dir):
    print("\n[STEP 6] Saving CSV files...")
    out = f"{output_dir}/csv"
    os.makedirs(out, exist_ok=True)

    # laws_catalogue.csv
    path = f"{out}/laws_catalogue.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(laws[0].keys()))
        w.writeheader()
        w.writerows(laws)
    print(f"  ✅ laws_catalogue.csv  ({len(laws)} rows)")

    # sections_all.csv — every provision as a flat row (best for RAG/embedding)
    path = f"{out}/sections_all.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(sections[0].keys()))
        w.writeheader()
        w.writerows(sections)
    print(f"  ✅ sections_all.csv  ({len(sections)} rows)")

    # agencies_contacts.csv (drop nested regional_offices dict)
    path = f"{out}/agencies_contacts.csv"
    flat = [{k: v for k, v in a.items() if k != "regional_offices"} for a in agencies]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(flat[0].keys()))
        w.writeheader()
        w.writerows(flat)
    print(f"  ✅ agencies_contacts.csv  ({len(flat)} rows)")

    # offense_to_section.csv
    path = f"{out}/offense_to_section.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["offense", "description", "laws_json", "report_to", "portal"])
        for offense, data in offense_map.items():
            w.writerow([
                offense,
                data.get("description", ""),
                json.dumps(data.get("laws", [])),
                " | ".join(data.get("report_to", [])),
                data.get("portal", ""),
            ])
    print(f"  ✅ offense_to_section.csv  ({len(offense_map)} rows)")
