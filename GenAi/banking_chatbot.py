import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

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
    faq[0]:
        "To reset your password, go to the login page and click on 'Forgot Password'. Follow the instructions sent to your registered email.",
    faq[1]:
        "We charge a 3% fee on all international transactions processed through your debit or credit card.",
    faq[2]:
        "You can apply for a personal loan through our website or mobile app by filling out the application form and submitting the required documents.",
    faq[3]:
        "Our current savings account interest rate is 4% per annum, compounded monthly.",
    faq[4]:
        "You can reach customer support 24/7 at 1-800-123-4567 or email us at support@bankexample.com."
}

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode the FAQ questions
faq_embeddings = model.encode(faq)

print(faq_embeddings.shape)
# Build the FAISS index using Inner Product for cosine similarity
dimension = faq_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(faq_embeddings)

# User query example
user_query = "How do I change my password?"

# Encode and normalize user query
query_embedding = model.encode([user_query])
k = 1
distances, indices = index.search(np.array(query_embedding), k)

closest_idx = faq[indices[0][0]]

answer = answers[closest_idx]


print(f"User Query: {user_query}\n")
print("Matched FAQ: ", closest_idx)
print("Chatbot answer; ", answer)

