
from google import genai
from config import GEMINI_API_KEY, GEN_MODEL, CHAT_HISTORY

client = None


def _get_client():
    global client
    if client is None:
        client = genai.Client(api_key=GEMINI_API_KEY)
    return client


def build_context(results):
    """Turns retrieved law chunks into a readable text block."""
    lines = []
    seen  = set()

    for r in results:
        key = (r["law_id"], r["section_number"])
        if key in seen:
            continue
        seen.add(key)

        block = (
            f"---\n"
            f"Law: {r['law_title']}\n"
            f"Section {r['section_number']}: {r['title']}\n"
            f"Text: {r['content'][:800]}\n"
        )
        if r.get("punishment_text"):
            block += f"Penalty: {r['punishment_text']}\n"

        lines.append(block)

    return "\n".join(lines)


def build_contacts_text(contacts):
    """Turns the contacts list into a readable block for the prompt."""
    lines = []
    for c in contacts:
        line = f"- {c['name']} ({c['abbr']})"
        if c.get("helpline_tollfree"):
            line += f" | Helpline: {c['helpline_tollfree']}"
        if c.get("helpline_direct"):
            line += f" | Direct: {c['helpline_direct']}"
        if c.get("email_complaint"):
            line += f" | Email: {c['email_complaint']}"
        if c.get("complaint_portal"):
            line += f" | Portal: {c['complaint_portal']}"
        if c.get("jurisdiction"):
            line += f"\n  Handles: {c['jurisdiction']}"
        lines.append(line)
    return "\n".join(lines)


def generate_answer(query, context, history, contacts):
    # past conv
    history_text = ""
    for turn in history[-CHAT_HISTORY:]:
        history_text += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n\n"

    contacts_text = build_contacts_text(contacts)

    prompt = f"""You are LegalBot PK — an AI assistant for Pakistan law research.

RULES:
1. Answer based on the legal context AND the contacts list below.
2. Always cite the Law name and Section number for legal claims.
3. If the user asks WHERE to complain or report, always give the relevant agency name, helpline, and email from the contacts list.
4. Never make up sections, penalties, phone numbers, or dates.

LEGAL CONTEXT:
{context}

GOVERNMENT AGENCY CONTACTS:
{contacts_text}

CONVERSATION HISTORY:
{history_text}
User's Question: {query}

Answer:"""

    response = _get_client().models.generate_content(
        model=GEN_MODEL,
        contents=prompt
    )
    return response.text.strip()
