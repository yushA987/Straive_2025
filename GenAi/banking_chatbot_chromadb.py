# Required: pip install faiss-cpu sentence-transformers requests

import os
import faiss
import numpy as np
import requests
from sentence_transformers import SentenceTransformer

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
# Step 1: Encode with SentenceTransformer
# -----------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')
faq_embeddings = model.encode(faqs, convert_to_numpy=True)

# -----------------------------
# Step 2: Build FAISS index
# -----------------------------
dimension = faq_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(faq_embeddings)

# -----------------------------
# Step 3: RAG retrieval and generation
# -----------------------------
def rag_answer(user_query, gemini_api_key, top_k=3):
    # Embed query
    query_embedding = model.encode([user_query], convert_to_numpy=True)

    # Search FAISS
    distances, indices = index.search(query_embedding, top_k)
    relevant_faqs = [faqs[i] for i in indices[0]]

    # Construct context
    context = "\n".join(relevant_faqs)

    # Prompt to Gemini
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
# Run Example
# -----------------------------
if __name__ == "__main__":
    user_query = "I forgot my online banking password. What should I do?"

    gemini_api_key =  "AIzaSyD_f7zVwrll1t_FWmTq5FESiYsSjFZoQ5E"

    answer = rag_answer(user_query, gemini_api_key)
    print("User Query:", user_query)
    print("AI Answer:", answer)
