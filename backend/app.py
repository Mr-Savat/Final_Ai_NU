# import os
# from flask import Flask, request, jsonify, send_from_directory
# from faq_loader import load_faq, find_answer
# from gpt2_model import ask_gpt2
# from confidence import calculate_confidence
# from groq import Groq
# from dotenv import load_dotenv  # Load environment variables

# # ----------------------------
# # Load .env file
# load_dotenv()

# # Initialize Flask
# app = Flask(__name__)
# faqs = load_faq("data/faqs.csv")

# # Load Groq API key from .env
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# groq_client = Groq(api_key=GROQ_API_KEY)

# # ----------------------------
# # Chat endpoint
# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.json
#     question = data.get("question", "").strip()

#     # Step 1: Check FAQ
#     faq_answer = find_answer(question, faqs)
#     if faq_answer:
#         return jsonify({"answer": faq_answer, "source": "FAQ"})

#     # Step 2: Ask GPT-2
#     gpt2_answer = ask_gpt2(question)
#     confidence = calculate_confidence(question, gpt2_answer)

#     if confidence >= 0.7:
#         return jsonify({
#             "answer": gpt2_answer,
#             "source": f"GPT-2 (confidence: {confidence:.2f})"
#         })

#     # Step 3: Groq fallback if GPT-2 confidence is low
#     groq_response = groq_client.chat.completions.create(
#         model="compound-beta-mini",  # Free tier model
#         messages=[
#             {"role": "system", "content": "You are a helpful chatbot."},
#             {"role": "user", "content": question}
#         ]
#     )
#     groq_answer = groq_response.choices[0].message.content

#     return jsonify({
#         "answer": groq_answer,
#         "source": f"Groq API (GPT-2 confidence: {confidence:.2f})"
#     })

# # ----------------------------
# # Serve frontend
# @app.route("/")
# def index():
#     return send_from_directory("../frontend", "index.html")

# @app.route("/<path:path>")
# def static_files(path):
#     return send_from_directory("../frontend", path)

# # ----------------------------
# # Run Flask app
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)

import os
from flask import Flask, request, jsonify, send_from_directory
from faq_loader import load_faq, find_answer
from gpt2_model import ask_gpt2
from confidence import calculate_confidence
from groq import Groq
from dotenv import load_dotenv  # Load environment variables

# ----------------------------
# Load .env file
load_dotenv()

# Initialize Flask
app = Flask(__name__)
faqs = load_faq("data/faqs.csv")

# Load Groq API key from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

# ----------------------------
# Chat endpoint


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    question = data.get("question", "").strip()

    # Step 1: Check FAQ
    faq_answer = find_answer(question, faqs)
    if faq_answer:
        return jsonify({"answer": faq_answer, "source": "FAQ"})

    # Step 2: Skip GPT-2, go straight to Groq fallback
    groq_response = groq_client.chat.completions.create(
        model="compound-beta-mini",
        messages=[
            {"role": "system", "content": "You are a helpful chatbot."},
            {"role": "user", "content": question}
        ]
    )
    groq_answer = groq_response.choices[0].message.content

    return jsonify({
        "answer": groq_answer,
        "source": "Groq API (no GPT-2)"
    })


# ----------------------------
# Serve frontend
@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("../frontend", path)


# ----------------------------
# Run Flask app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
