import os
from openai import OpenAI

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load FAQ knowledge base
with open("faq.md", "r", encoding="utf-8") as file:
    knowledge = file.read()

print("College Student Grounded FAQ Chatbot")
print("Type 'exit' to stop.\n")

while True:
    question = input("You: ")

    if question.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    prompt = f"""
You are a College Student FAQ chatbot.

Use ONLY the information provided in the knowledge base below.

If the answer is not available in the knowledge base, say:
"I don't have that information in the provided FAQ."

Do not invent or assume information.

KNOWLEDGE BASE:
{knowledge}

USER QUESTION:
{question}

Answer clearly and briefly.
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    print("Chatbot:", response.output_text)
    print()
