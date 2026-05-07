"""
Step 9 — Write README.md Documentation
"""

import os
from datetime import datetime


def write_readme(laws, sections, agencies, offense_map, output_dir):
    print("\n[STEP 9] Writing README.md...")
    out = f"{output_dir}/docs"
    os.makedirs(out, exist_ok=True)

    ts = datetime.now().strftime("%Y-%m-%d")

    content = f"""# 🇵🇰 Pakistan Law Chatbot — Dataset Documentation

> Generated: {ts} | Laws: {len(laws)} | Sections: {len(sections)} | Agencies: {len(agencies)}

---

## What Is This?

A structured dataset of all 1,030 federal Pakistani statutes plus agency contacts
and offense-to-section mappings — built for powering an AI law chatbot.

---

## Data Source

| Source | URL | What it provides |
|---|---|---|
| Pakistani Law MCP (GitHub) | https://github.com/Ansvar-Systems/Pakistani-law-mcp | 1,030 federal statutes as JSON |
| Pakistan Code (official) | https://pakistancode.gov.pk | Original consolidated federal laws |
| FIA | https://fia.gov.pk | Cybercrime unit contacts |
| PTA | https://pta.gov.pk | Telecom complaint portal |
| SECP | https://secp.gov.pk | Securities complaints |
| NAB | https://nab.gov.pk | Anti-corruption bureau |
| Wafaqi Mohtasib | https://mohtasib.gov.pk | Federal ombudsman (1055) |
| Digital Rights Foundation | https://digitalrightsfoundation.pk | Cyber harassment helpline |

---

## File Structure

```
output/
├── json/
│   ├── all_laws_master.json       ← Full text of all {len(laws)} laws
│   ├── laws_index.json            ← Metadata only (fast to load)
│   ├── agencies_contacts.json     ← {len(agencies)} agencies with contacts
│   └── offense_to_section.json    ← {len(offense_map)} offense → section maps
│
├── csv/
│   ├── laws_catalogue.csv         ← {len(laws)} rows — law metadata
│   ├── sections_all.csv           ← {len(sections)} rows — all provisions (use for RAG)
│   ├── agencies_contacts.csv      ← Agency contacts flat
│   └── offense_to_section.csv     ← Offense mappings flat
│
├── xml/
│   ├── pakistan_laws.xml          ← Laws in XML
│   └── agencies.xml               ← Agencies in XML
│
├── sqlite/
│   └── pakistan_law.db            ← Full database (4 tables, indexed)
│
└── docs/
    └── README.md                  ← This file
```

---

## SQLite Tables

| Table | Rows | Purpose |
|---|---|---|
| `laws` | {len(laws)} | Law metadata |
| `sections` | {len(sections)} | All provisions with full text |
| `agencies` | {len(agencies)} | Agency contacts |
| `offense_map` | {len(offense_map)} | Offense → section mapping |

---

## Quick Usage Examples

### Python — Section lookup
```python
import sqlite3
conn = sqlite3.connect("output/sqlite/pakistan_law.db")
c = conn.cursor()

# Find sections about harassment
c.execute(
    "SELECT law_title, section_number, title, content "
    "FROM sections WHERE content LIKE ?",
    ('%harassment%',)
)
for row in c.fetchall():
    print(row)
```

### Python — Get agency contact
```python
c.execute(
    "SELECT name, helpline_tollfree, complaint_portal, email_complaint "
    "FROM agencies WHERE id = ?",
    ('FIA',)
)
print(c.fetchone())
```

### Python — Find offense → section
```python
c.execute(
    "SELECT * FROM offense_map WHERE offense = ?",
    ('cyberstalking',)
)
print(c.fetchone())
```

---

## Agency Quick Reference

| Agency | Helpline | Portal |
|---|---|---|
| FIA Cybercrime | **1991** | complaint.fia.gov.pk |
| NCCIA / NR3C | 1991 | complaint.fia.gov.pk |
| PTA | **0800-55055** | complaint.pta.gov.pk |
| SECP | **0800-88008** | xs.secp.gov.pk |
| NAB | **1800-888-999** | nab.gov.pk/complaint |
| Wafaqi Mohtasib | **1055** | mohtasib.gov.pk/complaint |
| FBR | 051-111-772-772 | iris.fbr.gov.pk |
| SBP | 111-727-273 | sbp.org.pk/cpd/complaint |
| Women Helpline | **1043** | — |
| Police | **15** | complaint.punjabpolice.gov.pk |
| DRF (Online Harassment) | **0800-39393** | digitalrightsfoundation.pk/report |
| Rescue 1122 | **1122** | — |
| PEMRA | 0800-73672 | pemra.gov.pk/complaints |

---

## What Is Missing (Limitations)

| Missing | Reason | How to add |
|---|---|---|
| Punjab provincial laws | punjablaws.gov.pk blocks automated scraping | Download PDFs manually from browser |
| Sindh provincial laws | sindhlaws.gov.pk blocks automated scraping | Same |
| KPK provincial laws | pakp.gov.pk blocks automated scraping | Same |
| Balochistan laws | blaws.gob.pk unavailable | Same |
| Court judgments | Requires paid subscription | pakistanlawsite.com / paklegaldatabase.com |
| PECA Amendment 2025 full text | Not in seed repo yet | Download from na.gov.pk manually |

To add PDFs: place them in a `/pdfs` folder and run `python3 pdf_extractor.py` (coming soon).

---

## How to Re-run

```bash
pip install requests beautifulsoup4 lxml
python3 main.py
```

*Dataset built by pakistan_law_scraper | Source: github.com/Ansvar-Systems/Pakistani-law-mcp*
"""

    path = f"{out}/README.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ README.md written → {path}")
