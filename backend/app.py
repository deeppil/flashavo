from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json, re
from openai import OpenAI
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
CORS(app=app)

@app.get("/")
def home():
    return app.send_static_file("index.html")

@app.post("/generate")
def generate():
    data = request.get_json(force=True, silent=True) or {}
    topic = (data.get("topics") or "").strip()
    number = str(data.get("number", "")).strip()
    try:
        number = int(number)
    except ValueError:
        number = 3
    if not topic:
        return jsonify({"error": "topics is required"}), 400

    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=(
        "You are a flashcard generator.\n"
        f"Topic: {topic}\n\n"
        f"Return exactly {number} flashcards as a JSON array with objects like, the flashcard must be on the topic:\n"
        '[{"front":"question","back":"answer","tag":"topic"}]\n\n'
        "Do not include anything except the JSON."
        )
        )
    
    raw = getattr(resp, "output_text", None)
    if not raw:
        raw = resp.output[0].content[0].text

    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
    m = re.search(r"\[.*\]", text, flags=re.S)
    json_str = m.group(0) if m else text

    cards = json.loads(json_str) 
    
    return jsonify({
        "cards": cards
    })

@app.post("/follow")
def follow():
    data = request.get_json(force=True, silent=True) or {}
    query = (data.get("query") or "").strip()
    question = (data.get("question") or "").strip()
    topic = (data.get("topic") or "").strip()
    answer = (data.get("answer") or "").strip()
    if not query:
        return jsonify({"error": "query is required"}), 400

    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=(
        "You are a flashcard generator.\n"
        f"You were previously given the topic: {topic} and you generated a flashcard. The question was: {question} and answer was: {answer} \n"
        f"The user has a query: {query}"
        f"Return answer to the submitted query.\n"
        "Do not include anything except the answer. Keep it short but well explained."
        )
    )

    raw = getattr(resp, "output_text", None)
    if not raw:
        raw = resp.output[0].content[0].text

    text = (raw or "").strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
    answer_obj = None
    try:
        answer_obj = json.loads(text)
        if not isinstance(answer_obj, dict) or "answer" not in answer_obj:
            raise ValueError("Bad JSON shape")
    except Exception:

        answer_obj = {"answer": text}

    return jsonify(answer_obj)


if __name__ == "__main__":
    app.run(port=5000)