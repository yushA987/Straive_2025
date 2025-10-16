import streamlit as st
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import faiss
import numpy as np

# Streamlit UI
st.header("Hugging Face PDF Chatbot")

with st.sidebar:
    st.title("Your Documents")
    file = st.file_uploader("Upload a PDF file", type="pdf", key="pdf_uploader")

# Process PDF
if file is not None:
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    # Chunk text
    def chunk_text(text, chunk_size=1000, overlap=150):
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    chunks = chunk_text(text)
    st.write(f"Extracted {len(chunks)} chunks from the PDF.")

    # Embed chunks
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    chunk_embeddings = embedder.encode(chunks)

    # Build FAISS index
    index = faiss.IndexFlatL2(chunk_embeddings.shape[1])
    index.add(np.array(chunk_embeddings))

    # Hugging Face Q&A pipeline
    qa_model = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

    # User question
    user_question = st.text_input("Ask a question about the document")

    if user_question:
        query_embedding = embedder.encode([user_question])
        D, I = index.search(np.array(query_embedding), k=1)
        context = chunks[I[0][0]]
        # print(context)
        st.write(context)
        result = qa_model(question=user_question, context=context)
        st.subheader("Answer")
        st.write(result['answer'])