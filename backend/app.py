import os
from flask import Flask, request, jsonify, send_from_directory
from faq_loader import load_faq, find_answer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Load FAQs
try:
    faqs = load_faq("data/faqs.csv")
except Exception as e:
    print(f"FAQ loading error: {e}")
    faqs = []

# Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# List of available Groq models (fallback options)
AVAILABLE_MODELS = [
    "llama-3.1-8b-instant",  # New model name
    "llama-3.3-70b-versatile",  # Alternative
    "mixtral-8x7b-32768",  # Another option
    "gemma2-9b-it"  # Backup model
]


def get_available_model():
    """Try to find an available model"""
    # Default to the first one which should be available
    return AVAILABLE_MODELS[0]


@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"answer": "Please enter a question.", "source": "System"})

        # FAQ first
        faq_answer = find_answer(question, faqs)
        if faq_answer:
            return jsonify({"answer": faq_answer, "source": "FAQ"})

        # Groq fallback
        if not groq_client:
            return jsonify({
                "answer": "Chat service is currently unavailable.",
                "source": "System"
            })

        # Use available model
        model_name = get_available_model()
        print(f"Using model: {model_name}")

        groq_response = groq_client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful assistant for Norton University in Cambodia. 
                    Provide accurate and friendly information about the university.
                    Answer in a helpful and professional manner."""
                },
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=1024
        )

        return jsonify({
            "answer": groq_response.choices[0].message.content,
            "source": "Norton AI Assistant"
        })

    except Exception as e:
        print(f"Chat error: {e}")
        # Provide a more helpful error message
        return jsonify({
            "answer": "I apologize, but I'm experiencing technical difficulties. Please try asking about Norton University's programs, admissions, or contact information.",
            "source": "System"
        })


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
