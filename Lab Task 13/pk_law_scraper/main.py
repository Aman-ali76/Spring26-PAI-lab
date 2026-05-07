#!/usr/bin/env python3
"""
============================================================
  PAKISTAN LAW DATASET BUILDER — MAIN ENTRY POINT
  Run: python3 main.py
============================================================
"""

from modules.step1_clone      import clone_repo
from modules.step2_parse      import parse_seed_files
from modules.step3_agencies   import get_agencies
from modules.step4_offenses   import get_offense_map
from modules.step5_save_json  import save_json
from modules.step6_save_csv   import save_csv
from modules.step7_save_xml   import save_xml
from modules.step8_save_db    import save_sqlite
from modules.step9_readme     import write_readme
from modules.step10_zip       import create_zip
from datetime import datetime

OUTPUT_DIR = "./output"

if __name__ == "__main__":
    print("=" * 60)
    print("  PAKISTAN LAW DATASET BUILDER")
    print("  Source: github.com/Ansvar-Systems/Pakistani-law-mcp")
    print("=" * 60)

    start = datetime.now()

    # Step 1 — Clone GitHub repo
    clone_repo()

    # Step 2 — Parse all 1030 seed JSON files
    laws, sections, all_raw = parse_seed_files()

    # Step 3 — Load agency contacts
    agencies = get_agencies()

    # Step 4 — Build offense → section map
    offense_map = get_offense_map()

    # Step 5-8 — Save all formats
    save_json   (laws, sections, all_raw, agencies, offense_map, OUTPUT_DIR)
    save_csv    (laws, sections, agencies, offense_map, OUTPUT_DIR)
    save_xml    (laws, agencies, OUTPUT_DIR)
    save_sqlite (laws, sections, agencies, offense_map, OUTPUT_DIR)

    # Step 9 — Write README
    write_readme(laws, sections, agencies, offense_map, OUTPUT_DIR)

    # Step 10 — Create ZIP
    zip_path = create_zip(OUTPUT_DIR)

    elapsed = (datetime.now() - start).seconds
    print("\n" + "=" * 60)
    print("  ✅ DONE!")
    print(f"  Laws:       {len(laws)}")
    print(f"  Sections:   {len(sections)}")
    print(f"  Agencies:   {len(agencies)}")
    print(f"  Offenses:   {len(offense_map)}")
    print(f"  Time:       {elapsed}s")
    print(f"  Output:     {zip_path}")
    print("=" * 60)
