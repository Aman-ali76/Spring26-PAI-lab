# config.py

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR   = Path(__file__).parent
INDEX_PATH = BASE_DIR / "faiss_law_index.index"
JSON_DIR   = BASE_DIR / "pakistan_law_dataset" / "json"
CSV_DIR    = BASE_DIR / "pakistan_law_dataset" / "csv"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEN_MODEL      = "gemini-3-flash-preview"
TOP_K          = 5
CHAT_HISTORY   = 8
