from flask import Flask, request, jsonify
import os
import faiss
import numpy as np
import requests
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# -----------------------------
# Gemini API call function
# -----------------------------
def generate_response_with_gemini(prompt, api_key):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    resp_json = response.json()
    if 'candidates' in resp_json and len(resp_json['candidates']) > 0:
        parts = resp_json['candidates'][0]['content'].get('parts', [])
        if parts and 'text' in parts[0]:
            return parts[0]['text']
        else:
            return "Sorry, response parts do not contain text."
    else:
        return "Sorry, I couldn't generate an answer. Please try again."

# -----------------------------
# FAQ dataset
# -----------------------------
faqs = [
    "How can I reset my online banking password?",
    "How do I check my account balance?",
    "What should I do if my debit card is lost?",
    "How do I activate international transactions on my credit card?",
    "How can I open a new savings account?",
    "What is the minimum balance required?",
    "How do I update my registered mobile number?",
    "How can I apply for a home loan?",
    "What is the process for closing my bank account?",
    "How do I check my loan EMI schedule?",
    "How can I download my account statement?",
    "What is the daily withdrawal limit from an ATM?",
    "How do I enable UPI payments?",
    "Can I increase my credit card limit?",
    "What is the process to block a stolen credit card?",
    "How can I register for mobile banking?",
    "How do I apply for a personal loan?",
    "What is the penalty for not maintaining minimum balance?",
    "How can I dispute a wrong transaction?",
    "What are the bank's working hours?"
]

# -----------------------------
# Initialize SentenceTransformer model and FAISS index once
# -----------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')
faq_embeddings = model.encode(faqs, convert_to_numpy=True)
dimension = faq_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(faq_embeddings)

# -----------------------------
# RAG retrieval and generation
# -----------------------------
def rag_answer(user_query, gemini_api_key, top_k=3):
    # Embed query
    query_embedding = model.encode([user_query], convert_to_numpy=True)

    # Search FAISS
    distances, indices = index.search(query_embedding, top_k)
    relevant_faqs = [faqs[i] for i in indices[0]]

    # Construct context for Gemini
    context = "\n".join(relevant_faqs)

    prompt = f"""
You are a helpful banking assistant.
Below are some relevant FAQs from the knowledge base:

{context}

User's question: {user_query}

Based on the information above, provide a clear and helpful answer to the user.
"""

    # Call Gemini API
    return generate_response_with_gemini(prompt, gemini_api_key)

# -----------------------------
# Flask endpoint
# -----------------------------
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    user_query = data["query"]

    # Get Gemini API key from env variable for safety
    gemini_api_key = "AIzaSyD_f7zVwrll1t_FWmTq5FESiYsSjFZoQ5E"
    if not gemini_api_key:
        return jsonify({"error": "GEMINI_API_KEY environment variable not set"}), 500

    try:
        answer = rag_answer(user_query, gemini_api_key)
        return jsonify({
            "query": user_query,
            "answer": answer
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# Run the Flask app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
