"""
Step 8 — Save SQLite Database
Creates pakistan_law.db with 4 indexed tables:
  laws, sections, agencies, offense_map
"""

import os
import json
import sqlite3


def save_sqlite(laws, sections, agencies, offense_map, output_dir):
    print("\n[STEP 8] Saving SQLite database...")
    out = f"{output_dir}/sqlite"
    os.makedirs(out, exist_ok=True)

    db_path = f"{out}/pakistan_law.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # ── Schema ────────────────────────────────────────────────────
    c.executescript("""
        DROP TABLE IF EXISTS laws;
        DROP TABLE IF EXISTS sections;
        DROP TABLE IF EXISTS agencies;
        DROP TABLE IF EXISTS offense_map;

        CREATE TABLE laws (
            id              TEXT PRIMARY KEY,
            title           TEXT,
            short_name      TEXT,
            year            TEXT,
            status          TEXT,
            issued_date     TEXT,
            in_force_date   TEXT,
            source_url      TEXT,
            description     TEXT,
            num_provisions  INTEGER,
            source_file     TEXT
        );

        CREATE TABLE sections (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            law_id          TEXT,
            law_title       TEXT,
            section_number  TEXT,
            provision_ref   TEXT,
            title           TEXT,
            content         TEXT,
            punishment_text TEXT,
            FOREIGN KEY(law_id) REFERENCES laws(id)
        );

        CREATE TABLE agencies (
            id                  TEXT PRIMARY KEY,
            name                TEXT,
            abbr                TEXT,
            category            TEXT,
            website             TEXT,
            complaint_portal    TEXT,
            helpline_tollfree   TEXT,
            helpline_direct     TEXT,
            email_complaint     TEXT,
            email_general       TEXT,
            whatsapp            TEXT,
            address_hq          TEXT,
            operating_hours     TEXT,
            jurisdiction        TEXT,
            source              TEXT
        );

        CREATE TABLE offense_map (
            offense     TEXT PRIMARY KEY,
            description TEXT,
            laws_json   TEXT,
            report_to   TEXT,
            portal      TEXT
        );

        CREATE INDEX idx_sections_law    ON sections(law_id);
        CREATE INDEX idx_sections_num    ON sections(section_number);
        CREATE INDEX idx_laws_year       ON laws(year);
        CREATE INDEX idx_laws_status     ON laws(status);
        CREATE INDEX idx_agencies_cat    ON agencies(category);
    """)

    # ── Insert ────────────────────────────────────────────────────
    c.executemany(
        "INSERT OR REPLACE INTO laws VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        [tuple(l.values()) for l in laws]
    )

    c.executemany(
        """INSERT INTO sections
           (law_id, law_title, section_number, provision_ref, title, content, punishment_text)
           VALUES (?,?,?,?,?,?,?)""",
        [(s["law_id"], s["law_title"], s["section_number"],
          s["provision_ref"], s["title"], s["content"], s["punishment_text"])
         for s in sections]
    )

    flat_agencies = [{k: v for k, v in a.items() if k != "regional_offices"} for a in agencies]
    c.executemany(
        "INSERT OR REPLACE INTO agencies VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [tuple(a.values()) for a in flat_agencies]
    )

    c.executemany(
        "INSERT OR REPLACE INTO offense_map VALUES (?,?,?,?,?)",
        [(k,
          v["description"],
          json.dumps(v["laws"]),
          " | ".join(v["report_to"]),
          v["portal"])
         for k, v in offense_map.items()]
    )

    conn.commit()
    conn.close()

    size_mb = os.path.getsize(db_path) / (1024 * 1024)
    print(f"  ✅ pakistan_law.db  ({size_mb:.1f} MB, 4 tables)")
