from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

app = Flask(__name__)

# ----------------------------
# Load data and initialize FAISS
# ----------------------------

# FAQ questions list
faq = [
    "How can I reset my online banking password?",
    "What are the charges for international transactions?",
    "How do I apply for a personal loan?",
    "What is the interest rate on savings accounts?",
    "How can I contact customer support?"
]

# Answers dictionary
answers = {
    faq[0]: "To reset your password, go to the login page and click on 'Forgot Password'. Follow the instructions sent to your registered email.",
    faq[1]: "We charge a 3% fee on all international transactions processed through your debit or credit card.",
    faq[2]: "You can apply for a personal loan through our website or mobile app by filling out the application form and submitting the required documents.",
    faq[3]: "Our current savings account interest rate is 4% per annum, compounded monthly.",
    faq[4]: "You can reach customer support 24/7 at 1-800-123-4567 or email us at support@bankexample.com."
}

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode FAQs
faq_embeddings = model.encode(faq)
dimension = faq_embeddings.shape[1]

# Create FAISS index
index = faiss.IndexFlatL2(dimension)
index.add(faq_embeddings)


# ----------------------------
# Endpoint: /ask
# ----------------------------
@app.route("/ask", methods=["POST"])
def ask_bot():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    user_query = data["query"]

    # Encode the user query
    query_embedding = model.encode([user_query])
    k = 1
    distances, indices = index.search(np.array(query_embedding), k)

    matched_question = faq[indices[0][0]]
    answer = answers[matched_question]

    return jsonify({
        "query": user_query,
        "matched_question": matched_question,
        "answer": answer
    })


# ----------------------------
# Run the Flask app
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
