import streamlit as st
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import requests
import json

# Streamlit UI
st.header("Gemini PDF Chatbot")

with st.sidebar:
    st.title("Your Documents")
    file = st.file_uploader("Upload a PDF file", type="pdf", key="pdf_uploader")


# Function to extract text from PDF
def extract_pdf_text(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text


# Chunk text for embedding
def chunk_text(text, chunk_size=1000, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


# Function to get response from Gemini API
def generate_answer_with_gemini(question, context, api_key):
    url = "https://api.gemini.com/v1/qa"  # Replace this with the correct Gemini endpoint
    headers = {
        "Authorization": f"Bearer {AIzaSyD_f7zVwrll1t_FWmTq5FESiYsSjFZoQ5E}",
        "Content-Type": "application/json"
    }
    data = {
        "question": question,
        "context": context
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()  # Return the response containing the generated answer
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None


# Main app flow
if file is not None:
    # Extract and chunk PDF text
    text = extract_pdf_text(file)
    chunks = chunk_text(text)
    st.write(f"Extracted {len(chunks)} chunks from the PDF.")

    # Embed text chunks
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    chunk_embeddings = embedder.encode(chunks)

    # Build FAISS index for fast search
    index = faiss.IndexFlatL2(chunk_embeddings.shape[1])
    index.add(np.array(chunk_embeddings))

    # User question input
    user_question = st.text_input("Ask a question about the document")

    if user_question:
        # Search for the most relevant chunk
        query_embedding = embedder.encode([user_question])
        D, I = index.search(np.array(query_embedding), k=1)
        context = chunks[I[0][0]]

        # Display the context from the document
        st.write("Context from the document:")
        st.write(context)

        # Get the API key from the user (prompting for input)
        api_key = st.text_input("Enter your Gemini API key", type="password")

        if api_key:
            # Call the Gemini API to generate the answer
            response = generate_answer_with_gemini(user_question, context, api_key)

            if response:
                # Display the generated answer
                answer = response.get("answer", "Sorry, I couldn't generate an answer.")
                st.subheader("Answer:")
                st.write(answer)
