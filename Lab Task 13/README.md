# LegalBot PK — Pakistan Law AI Assistant

<div align="center">
  <h1>⚖️ LegalBot PK</h1>
  <p><em>Ask any question about Pakistan law — get cited, accurate answers in seconds.</em></p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python" />
    <img src="https://img.shields.io/badge/Flask-3.0-black?style=flat-square&logo=flask" />
    <img src="https://img.shields.io/badge/Gemini-2.0%20Flash-orange?style=flat-square&logo=google" />
    <img src="https://img.shields.io/badge/FAISS-Vector%20Search-green?style=flat-square" />
    <img src="https://img.shields.io/badge/Laws%20Indexed-28%2C249-forestgreen?style=flat-square" />
  </p>
</div>

---

## What is this?

LegalBot PK is a **RAG (Retrieval-Augmented Generation)** chatbot built on Pakistan's complete federal law database.

Instead of making things up, it:
1. Searches 28,249 law sections using vector similarity (FAISS)
2. Retrieves the most relevant provisions
3. Passes them as context to Gemini
4. Returns an answer that cites actual laws and sections

It also includes real government agency contacts (FIA, PTA, SECP, etc.) so it can answer "where do I complain?" questions with actual helpline numbers.

---

## How the App Works — Full Flow

```
User types a question
        │
        ▼
   app.py /api/chat
        │
        ├─► retriever.search(query)
        │         │
        │         ├─ MiniLM encodes the query → 384-dim vector
        │         └─ FAISS finds top-5 closest law sections
        │
        ├─► generator.build_context(results)
        │         └─ Formats the retrieved sections into readable text
        │
        ├─► loader.load_contacts()
        │         └─ Loads all agency helplines, emails, portals
        │
        └─► generator.generate_answer(query, context, history, contacts)
                  └─ Gemini Flash reads context + contacts → writes answer
                        │
                        ▼
              JSON response: { answer, sources, elapsed_s }
                        │
                        ▼
              Frontend displays answer + clickable source chips
```

---

## Project Structure

```
Lab Task 13/
│
├── app.py              ← Flask server + all API routes
├── config.py           ← All settings (paths, API key, model names)
├── loader.py           ← Reads data files (chunks, laws, contacts)
├── retriever.py        ← FAISS vector search + MiniLM embedding
├── generator.py        ← Builds prompt + calls Gemini API
│
├── templates/
│   └── index.html      ← Frontend chatbot UI (3-column layout)
│
├── pakistan_law_dataset/
│   ├── csv/
│   │   ├── sections_all.csv        ← 28,249 law sections (main data)
│   │   └── agencies_contacts.csv   ← Government agency contact info
│   └── json/
│       └── laws_index.json         ← Law metadata (title, year, URL)
│
├── embeddings.npy          ← Pre-built MiniLM vectors (28,249 × 384)
├── faiss_law_index.index   ← FAISS index built from embeddings.npy
│
├── requirements.txt
├── .env                    ← Your GEMINI_API_KEY goes here
└── PAI_Project_Embeddings.ipynb   ← How embeddings were created
```

---

## Module Reference

### `config.py` — Settings

Holds all constants in one place. Change things here only.

| Variable | Value | Purpose |
|---|---|---|
| `INDEX_PATH` | `faiss_law_index.index` | Path to the FAISS index file |
| `JSON_DIR` | `pakistan_law_dataset/json/` | Folder with laws_index.json |
| `CSV_DIR` | `pakistan_law_dataset/csv/` | Folder with sections CSV |
| `GEMINI_API_KEY` | from `.env` | Gemini API key |
| `GEN_MODEL` | `gemini-3-flash-preview` | Which Gemini model to use |
| `TOP_K` | `5` | How many law sections to retrieve per query |
| `CHAT_HISTORY` | `8` | How many past turns to remember per session |

---

### `loader.py` — Data Loading

Reads files from disk. Caches results in RAM so files are only read once.

#### `load_chunks()`
- **Reads:** `sections_all.csv`
- **Returns:** List of 28,249 dicts, one per law section
- **Each dict has:** `law_id`, `law_title`, `section_number`, `title`, `content`, `punishment_text`
- **Why:** This is the main legal text database. Every section is a "chunk" that was embedded into the FAISS index.

#### `load_laws()`
- **Reads:** `laws_index.json`
- **Returns:** Dict of `{ law_id → law_metadata }`
- **Each entry has:** `name`, `year`, `status`, `source_url`
- **Why:** Used to look up the source URL and status of a law when building the sources list for the frontend.

#### `load_contacts()`
- **Reads:** `agencies_contacts.csv`
- **Returns:** List of agency dicts
- **Each dict has:** `name`, `abbr`, `helpline_tollfree`, `helpline_direct`, `email_complaint`, `complaint_portal`, `jurisdiction`
- **Why:** Passed to Gemini so it can answer "where do I report?" questions with real phone numbers and emails.

---

### `retriever.py` — Vector Search

Converts a query to a vector and finds the closest law sections in the FAISS index.

#### `_get_index()`
- Loads `faiss_law_index.index` from disk (once, cached in `_index`)
- **Why:** The FAISS index holds 28,249 pre-computed 384-dim vectors. Loading it into RAM makes search instant.

#### `_get_model()`
- Loads `all-MiniLM-L6-v2` from sentence-transformers (once, cached in `_model`)
- **Why:** This is the same model that was used in `PAI_Project_Embeddings.ipynb` to build `embeddings.npy`. Query and corpus must use the same model or the vectors are incompatible.

#### `_embed(query)`
- Converts a text string → 384-dim float32 numpy array
- **Why:** FAISS can only search by vector, not by text. We convert the query to the same vector space as the stored law sections.

#### `search(query, top_k=5)`
- Runs `_embed(query)` then calls `index.search(vec, k=top_k)`
- Converts L2 distance → similarity score: `similarity = 1 - distance/2`
- **Returns:** Top-5 chunks with similarity scores attached
- **Why:** This is the core retrieval step. Without good retrieval, Gemini has no relevant context to answer from.

> **Note:** `embeddings.npy` (corpus) and `_embed()` (query) must use the **same model and same dimensions (384)**. Mixing models gives wrong results.

---

### `generator.py` — Answer Generation

Takes the retrieved chunks and generates a cited answer using Gemini.

#### `_get_client()`
- Creates a `genai.Client` using `GEMINI_API_KEY` (once, cached in `client`)
- **Why:** Avoid creating a new HTTP client on every request.

#### `build_context(results)`
- Takes the list of retrieved chunks from `retriever.search()`
- Formats them into a readable text block:
  ```
  ---
  Law: Prevention of Electronic Crimes Act 2016
  Section 24: Cyber Stalking
  Text: A person commits the offence of cyber stalking who...
  Penalty: 3 years imprisonment or fine of 1 million rupees
  ```
- **Why:** Gemini is not a law database — it doesn't know Pakistani law. We must paste the relevant text into the prompt so it has something accurate to answer from.

#### `build_contacts_text(contacts)`
- Converts the contacts list into a formatted string for the prompt:
  ```
  - FIA (FIA) | Helpline: 1991 | Direct: 051-111-345-786 | Email: complaints@fia.gov.pk
    Handles: Federal — Cybercrime, Human Trafficking, Banking Fraud
  ```
- **Why:** Without this, Gemini would say "consult a lawyer" when asked where to report. With it, it gives real helpline numbers.

#### `generate_answer(query, context, history, contacts)`
- Builds a full prompt containing: system rules + legal context + agency contacts + conversation history + user's question
- Calls `gemini-3-flash-preview` with `generate_content()`
- **Returns:** The answer text as a plain string
- **Why:** Gemini's job is to read the pasted context and write a well-structured, cited answer. It does not "know" Pakistani law — it only reads what we give it.

---

### `app.py` — Flask Routes

The entry point. Receives HTTP requests, calls modules, returns JSON.

#### `GET /` → `home()`
- Serves `templates/index.html`
- **Why:** Renders the frontend chatbot UI.

#### `POST /api/chat` → `chat()`
Full chat flow, step by step:
1. Parse `query` and `session_id` from the request body
2. Call `retriever.search(query)` → top-5 law sections
3. Call `generator.build_context(results)` → readable law text
4. Get `sessions[session_id]` → past conversation turns
5. Call `loader.load_contacts()` → agency contact data
6. Call `generator.generate_answer(...)` → Gemini answer
7. Save this turn to `sessions[session_id]`
8. Build `sources` list (law title, section, similarity, URL)
9. Return `{ answer, sources, elapsed_s }`

#### `GET /api/health` → `health()`
- Returns `{ status: "ok", laws_indexed: 1030 }`
- **Why:** Frontend pings this on load to confirm the server is alive.

#### `POST /api/clear` → `clear_session()`
- Deletes `sessions[session_id]`
- **Why:** "New Chat" button resets conversation history.

#### `sessions = {}`
- In-memory dict: `{ session_id → [ {user, assistant}, ... ] }`
- **Why:** Gemini has no memory between calls. We store past turns here and paste them into every prompt so the bot remembers context.

---

## Installation

```bash
# 1. Clone or download the project
cd "Lab Task 13"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file with your Gemini API key
echo GEMINI_API_KEY=your_key_here > .env

# 4. Run the server
python app.py
```

Then open `http://localhost:5000` in your browser.

> **First run:** MiniLM model (~80MB) downloads automatically from Hugging Face. This only happens once.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | Yes | Get from [Google AI Studio](https://aistudio.google.com/apikey) |

---

## API Reference

| Endpoint | Method | Body | Returns |
|---|---|---|---|
| `/` | GET | — | HTML page (chatbot UI) |
| `/api/chat` | POST | `{ query, session_id }` | `{ answer, sources, elapsed_s }` |
| `/api/health` | GET | — | `{ status, laws_indexed }` |
| `/api/clear` | POST | `{ session_id }` | `{ cleared }` |

---

## How Embeddings Were Built

See `PAI_Project_Embeddings.ipynb`. The short version:

1. All 28,249 law sections were loaded from `sections_all.csv`
2. Each section was converted to text (law + section + content + penalty)
3. `all-MiniLM-L6-v2` encoded each text → 384-dim vector
4. All vectors saved to `embeddings.npy` (shape: 28,249 × 384)
5. FAISS index built from those vectors → `faiss_law_index.index`

At query time, the user's question goes through the same model → same 384-dim space → FAISS finds the closest matches.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + Flask |
| Vector Search | FAISS (Facebook AI Similarity Search) |
| Query Embedding | sentence-transformers `all-MiniLM-L6-v2` |
| Answer Generation | Google Gemini `gemini-3-flash-preview` |
| Frontend | HTML + Vanilla CSS + JavaScript |
| Data | 1,030+ Pakistan federal laws, 28,249 sections |

---

## License

For academic use only — BSAI-4C, Programming for AI (Lab), Lab Task 13.
