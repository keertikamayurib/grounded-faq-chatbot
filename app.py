import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Read FAQ file
with open("faq.md", "r", encoding="utf-8") as file:
    faq_text = file.read()

faq_items = []

# Extract FAQ sections
sections = re.split(r"\n(?=## )", faq_text)

for section in sections:
    lines = section.strip().splitlines()

    if not lines:
        continue

    question = ""
    answer = []

    for line in lines:
        if line.startswith("## "):
            question = line[3:].strip()
        elif question:
            answer.append(line.strip())

    if question and answer:
        faq_items.append({
            "question": question,
            "answer": " ".join(answer)
        })


def find_answer(user_question):

    user_words = set(
        re.findall(r"\b[a-zA-Z]+\b", user_question.lower())
    )

    stop_words = {
        "what", "is", "the", "a", "an", "are",
        "how", "can", "do", "does", "about",
        "college", "student"
    }

    user_words = user_words - stop_words

    best_match = None
    best_score = 0

    for item in faq_items:

        faq_words = set(
            re.findall(r"\b[a-zA-Z]+\b", item["question"].lower())
        )

        faq_words = faq_words - stop_words

        common_words = user_words.intersection(faq_words)

        score = len(common_words)

        if score > best_score:
            best_score = score
            best_match = item

    if best_match and best_score >= 1:
        return best_match["answer"]

    return "Sorry, I could not find an answer to that question in the College FAQ."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    question = data.get("question", "")

    answer = find_answer(question)

    return jsonify({
        "answer": answer
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
