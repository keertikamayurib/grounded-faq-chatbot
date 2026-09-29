import re

# Read FAQ data
with open("faq.md", "r", encoding="utf-8") as file:
    faq_text = file.read()

# Convert FAQ markdown into question-answer pairs
faq_items = []

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
        re.findall(r"\b[a-zA-Z0-9]+\b", user_question.lower())
    )

    best_match = None
    best_score = 0

    for item in faq_items:
        faq_words = set(
            re.findall(r"\b[a-zA-Z0-9]+\b", item["question"].lower())
        )

        common_words = user_words.intersection(faq_words)
        score = len(common_words)

        if score > best_score:
            best_score = score
            best_match = item

    if best_match and best_score >= 1:
        return best_match["answer"]

    return "Sorry, I could not find an answer to that question in the FAQ."


print("College Student Grounded FAQ Chatbot")
print("Type 'exit' to stop.")

while True:
    user_question = input("\nYou: ")

    if user_question.lower() == "exit":
        print("Chatbot stopped.")
        break

    answer = find_answer(user_question)

    print("Bot:", answer)
