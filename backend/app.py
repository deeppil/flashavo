from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json, re
from openai import OpenAI
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
CORS(app=app)

@app.post("/generate")
def generate():
    data = request.get_json(force=True, silent=True) or {}
    topic = (data.get("topics") or "").strip()
    if not topic:
        return jsonify({"error": "topics is required"}), 400

    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=(
        "You are a flashcard generator.\n"
        f"Topic: {topic}\n\n"
        "Return exactly 3 flashcards as a JSON array with objects like, the flashcard must be on the topic:\n"
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


if __name__ == "__main__":
    app.run(port=5000)