from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

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

# Initialize ChromaDB client
chroma_client = chromadb.Client(Settings(anonymized_telemetry=False))

# Create a collection
collection = chroma_client.create_collection(name="faq_collection")

# Add FAQ entries to ChromaDB
for i, question in enumerate(faq):
    collection.add(
        documents=[question],
        embeddings=[faq_embeddings[i]],
        ids=[str(i)]
    )

# User query example
user_query = "How do I change my password?"
query_embedding = model.encode([user_query])[0]

# Perform similarity search
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=1
)

# Retrieve matched question and answer
matched_id = int(results['ids'][0][0])
matched_question = faq[matched_id]
matched_answer = answers[matched_question]

# Output
print(f"User Query: {user_query}\n")
print("Matched FAQ: ", matched_question)
print("Chatbot Answer: ", matched_answer)
