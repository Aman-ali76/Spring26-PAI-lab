
import time
from flask import Flask, request, jsonify, render_template

import config
import loader
import retriever
import generator

app = Flask(__name__)


sessions = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    body       = request.get_json() or {}
    query      = body.get("query", "").strip()
    session_id = body.get("session_id", "default")

    if not query:
        return jsonify({"error": "Please provide a question."}), 400

    start = time.perf_counter()

    results  = retriever.search(query)
    context  = generator.build_context(results)
    history  = sessions.get(session_id, [])
    contacts = loader.load_contacts()

    answer = generator.generate_answer(query, context, history, contacts)

    history.append({"user": query, "assistant": answer})
    sessions[session_id] = history[-config.CHAT_HISTORY:]

    elapsed = round(time.perf_counter() - start, 2)

    laws      = loader.load_laws()
    sources   = []
    seen      = set()

    for r in results:
        key = (r["law_id"], r["section_number"])
        if key in seen:
            continue
        seen.add(key)
        meta = laws.get(r["law_id"], {})
        sources.append({
            "law_title":      r["law_title"],
            "section_number": r["section_number"],
            "similarity":     r["similarity"],
            "source_url":     meta.get("source_url", ""),
        })

    return jsonify({
        "answer":    answer,
        "sources":   sources[:5],
        "elapsed_s": elapsed,
    })


@app.route("/api/health")
def health():
    laws = loader.load_laws()
    return jsonify({"status": "ok", "laws_indexed": len(laws)})


@app.route("/api/clear", methods=["POST"])
def clear_session():
    body       = request.get_json() or {}
    session_id = body.get("session_id", "default")
    sessions.pop(session_id, None)
    return jsonify({"cleared": True})


if __name__ == "__main__":
    app.run(debug=True)
