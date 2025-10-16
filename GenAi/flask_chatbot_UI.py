from flask import Flask, request, jsonify, render_template_string
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
    "What is a credit score and how is it calculated?",
    "How can I improve my credit score?",
    "What is the difference between a checking and savings account?",
    "How do I open a brokerage account?",
    "What are the different types of investment options?",
    "What is compound interest?",
    "How do I apply for a mortgage loan?",
    "What documents are needed for a personal loan application?",
    "What are the tax benefits of investing in retirement accounts?",
    "How does a 401(k) plan work?",
    "What is an IRA and how does it differ from a 401(k)?",
    "How do I create a monthly budget?",
    "What is the difference between a stock and a bond?",
    "What are mutual funds and ETFs?",
    "How much emergency fund should I have?",
    "How do I refinance my mortgage?",
    "What is debt consolidation?",
    "How do credit cards work?",
    "What is APR and how does it affect my loan?",
    "What are the risks of investing in the stock market?",
    "How do dividends work?",
    "What is inflation and how does it affect my savings?",
    "What is the difference between fixed and variable interest rates?",
    "How can I protect myself from identity theft?",
    "What is financial planning and why is it important?",
    "How do taxes on capital gains work?",
    "What is a credit limit?",
    "How do I dispute a fraudulent charge on my credit card?",
    "What is a secured loan?",
    "How does credit card reward programs work?",
    "How can I save for my child’s education?",
    "What is the difference between term and whole life insurance?",
    "How do I choose the right health insurance plan?",
    "What are the benefits of a high-yield savings account?",
    "How do payday loans work and what are the risks?",
    "What is a home equity loan?",
    "How does mortgage pre-approval work?",
    "What is the difference between gross and net income?",
    "What are tax deductions and tax credits?",
    "How do I avoid late fees on my bills?",
    "What is a budget deficit?",
    "How do I track my expenses efficiently?",
    "What is the significance of a financial advisor?",
    "How can I start investing with a small amount of money?",
    "What is diversification in investment?",
    "What are the penalties for early withdrawal from retirement accounts?",
    "How do I calculate my debt-to-income ratio?",
    "What is an emergency fund and why do I need one?",
    "How do overdraft fees work?",
    "How do I set financial goals?"
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
# RAG retrieval and generation function
# -----------------------------
def rag_answer(user_query, gemini_api_key, top_k=3):
    # Embed query
    query_embedding = model.encode([user_query], convert_to_numpy=True)

    # Search FAISS index for similar FAQs
    distances, indices = index.search(query_embedding, top_k)
    relevant_faqs = [faqs[i] for i in indices[0]]

    # Construct context string for Gemini prompt
    context = "\n".join(relevant_faqs)

    prompt = f"""
You are a helpful financial advisor.
Below are some relevant FAQs from the knowledge base:

{context}

User's question: {user_query}

Based on the information above, provide a clear and helpful answer to the user.
"""

    # Call Gemini API
    return generate_response_with_gemini(prompt, gemini_api_key)

# -----------------------------
# Flask endpoint to serve UI
# -----------------------------
@app.route("/")
def home():
    # Simple HTML with embedded JS to send query and display conversation stack
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Banking FAQ Chatbot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f5f7fa;
                display: flex;
                justify-content: center;
                padding: 50px;
            }
            .card {
                background: white;
                width: 600px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                border-radius: 8px;
                padding: 20px;
                display: flex;
                flex-direction: column;
                max-height: 80vh;
                overflow-y: auto;
            }
            .conversation {
                flex-grow: 1;
                overflow-y: auto;
                margin-bottom: 20px;
            }
            .message {
                margin-bottom: 15px;
            }
            .user {
                font-weight: bold;
                color: #2c3e50;
            }
            .bot {
                background: #e1f5fe;
                padding: 10px;
                border-radius: 6px;
                white-space: pre-wrap;
            }
            .input-area {
                display: flex;
                gap: 10px;
            }
            input[type="text"] {
                flex-grow: 1;
                padding: 10px;
                font-size: 16px;
                border-radius: 6px;
                border: 1px solid #ccc;
            }
            button {
                background: #3498db;
                border: none;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                cursor: pointer;
                transition: background 0.3s ease;
            }
            button:hover {
                background: #2980b9;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div id="conversation" class="conversation"></div>
            <div class="input-area">
                <input type="text" id="userInput" placeholder="Type your question here..." />
                <button onclick="sendQuery()">Send</button>
            </div>
        </div>
        <script>
            const conversationDiv = document.getElementById('conversation');
            const userInput = document.getElementById('userInput');

            function addMessage(user, text) {
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message');
                if (user === 'user') {
                    messageDiv.innerHTML = `<div class="user">You:</div><div>${text}</div>`;
                } else {
                    messageDiv.innerHTML = `<div class="bot">Bot:</div><div>${text}</div>`;
                }
                // Add new messages at the top
                conversationDiv.insertBefore(messageDiv, conversationDiv.firstChild);
            }

            async function sendQuery() {
                const query = userInput.value.trim();
                if (!query) return;

                addMessage('user', query);
                userInput.value = '';
                userInput.disabled = true;

                try {
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({query})
                    });

                    const data = await response.json();

                    if (response.ok) {
                        addMessage('bot', data.answer);
                    } else {
                        addMessage('bot', 'Error: ' + data.error);
                    }
                } catch (err) {
                    addMessage('bot', 'Network error');
                } finally {
                    userInput.disabled = false;
                    userInput.focus();
                }
            }

            // Allow pressing Enter to send message
            userInput.addEventListener('keydown', function(event) {
                if (event.key === 'Enter') {
                    sendQuery();
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

# -----------------------------
# Flask API endpoint for /ask
# -----------------------------
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    user_query = data["query"]

    # Your Gemini API key (better to store in environment variable for production)
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
# Run Flask app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)



