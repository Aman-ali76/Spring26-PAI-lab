# loader.py
# Loads data files once and caches them in memory.

import csv
import json
from config import CSV_DIR, JSON_DIR

_chunks = None
_laws   = None


def load_chunks():
    global _chunks
    if _chunks is not None:
        return _chunks

    csv.field_size_limit(10 * 1024 * 1024)  # allow large text fields

    chunks = []
    with open(CSV_DIR / "sections_all.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            chunks.append({
                "text": (
                    f"Law: {row.get('law_title', '')}\n"
                    f"Section: {row.get('section_number', '')}\n"
                    f"Title: {row.get('title', '')}\n"
                    f"Content: {row.get('content', '')}\n"
                    f"Penalty: {row.get('punishment_text', 'N/A')}"
                ),
                "law_id":          row.get("law_id", ""),
                "law_title":       row.get("law_title", ""),
                "section_number":  row.get("section_number", ""),
                "title":           row.get("title", ""),
                "content":         row.get("content", ""),
                "punishment_text": row.get("punishment_text", ""),
            })

    _chunks = chunks
    return _chunks


def load_laws():
    global _laws
    if _laws is not None:
        return _laws

    with open(JSON_DIR / "laws_index.json", encoding="utf-8") as f:
        data = json.load(f)

    _laws = {item["id"]: item for item in data}
    return _laws


def load_contacts():
    """Loads all government agency contacts from CSV and returns as a list of dicts."""
    contacts = []
    with open(CSV_DIR / "agencies_contacts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            contacts.append(row)
    return contacts
