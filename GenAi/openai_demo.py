# import streamlit as st
# from PyPDF2 import PdfReader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.chains.question_answering import load_qa_chain
# from langchain_community.chat_models import ChatOpenAI
# import google.generativeai as genai
#
#
# genai.configure(api_key="AIzaSyD_f7zVwrll1t_FWmTq5FESiYsSjFZoQ5E")
#
# # OPENAI_API_KEY = "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" #Pass your key here
#
#
# #Upload PDF files
# st.header("My first Chatbot")
#
#
# with  st.sidebar:
#     st.title("Your Documents")
#     file = st.file_uploader(" Upload a PDf file and start asking questions", type="pdf", key="pdf_uploader")
#
#
# #Extract the text
# if file is not None:
#     pdf_reader = PdfReader(file)
#     text = ""
#     for page in pdf_reader.pages:
#         text += page.extract_text()
#         #st.write(text)
#
#
# #Break it into chunks
#     text_splitter = RecursiveCharacterTextSplitter(
#         separators="\n",
#         chunk_size=1000,
#         chunk_overlap=150,
#         length_function=len
#     )
#     chunks = text_splitter.split_text(text)
#     st.write(chunks)
#     #
#     #
#     #
#     #
#     # # generating embedding
#     embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
#
#
#     # creating vector store - FAISS
#     vector_store = FAISS.from_texts(chunks, embeddings)
#     #
#     #
#     # get user question
#     user_question = st.text_input("Type Your question here")
#
#
#     # do similarity search
#     if user_question:
#         match = vector_store.similarity_search(user_question)
#         #st.write(match)
#
#
#         #define the LLM
#         llm = ChatOpenAI(
#             openai_api_key = OPENAI_API_KEY,
#             temperature = 0,
#             max_tokens = 1000,
#             model_name = "gpt-3.5-turbo"
#         )
#
#
#         #output results
#         #chain -> take the question, get relevant document, pass it to the LLM, generate the output
#         chain = load_qa_chain(llm, chain_type="stuff")
#         response = chain.run(input_documents = match, question = user_question)
#         st.write(response)

import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

st.header("Gemini PDF Chatbot")

with st.sidebar:
    st.title("Your Documents")
    file = st.file_uploader("Upload a PDF file", type="pdf", key="pdf_uploader")

if file is not None:
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    user_question = st.text_input("Type your question here")

    if user_question:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Answer this question based on the following text:\n\n{text}\n\nQuestion: {user_question}")
        st.write(response.text)
