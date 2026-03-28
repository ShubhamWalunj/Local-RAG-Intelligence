import streamlit as st
import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from dotenv import load_dotenv

# --- 1. Setup & Session State ---
load_dotenv()

st.set_page_config(page_title="Local Library Intelligence", layout="wide", page_icon="📚")

# Initialize Session State for History and Chain
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

st.title("📚 Local Library Intelligence Engine")
st.markdown("Query multiple documents simultaneously with full privacy and high-speed inference.")
st.markdown("---")

# --- 2. Sidebar: Configuration & History ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key Handling
    api_key = st.text_input("Enter Groq API Key", type="password", value=os.getenv("GROQ_API_KEY", ""))
    
    # Multi-File Uploader [Updated for Multi-Document Support]
    uploaded_files = st.file_uploader("Upload your PDFs", type="pdf", accept_multiple_files=True)
    
    col1, col2 = st.columns(2)
    with col1:
        process_button = st.button("Build Library", use_container_width=True)
    with col2:
        # Clear Cache Button [UI Enhancement]
        if st.button("Clear Cache", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.rag_chain = None
            if os.path.exists("temp_dir"):
                shutil.rmtree("temp_dir")
            st.rerun()

    st.markdown("---")
    st.header("📜 Query History")
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        st.caption(f"Q: {chat['question'][:40]}...")

# --- 3. Multi-Document Processing Logic ---
if process_button:
    if not api_key:
        st.error("Please enter a Groq API Key.")
    elif not uploaded_files:
        st.error("Please upload at least one PDF.")
    else:
        with st.spinner("Analyzing library... Chunking & Vectorizing multiple documents."):
            # Create a clean temp directory
            if os.path.exists("temp_dir"):
                shutil.rmtree("temp_dir")
            os.makedirs("temp_dir")
            
            all_pages = []
            for uploaded_file in uploaded_files:
                temp_path = os.path.join("temp_dir", uploaded_file.name)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Load each PDF individually
                loader = PyPDFLoader(temp_path)
                all_pages.extend(loader.load())
            
            # Chunking the entire library
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(all_pages)
            
            # Local Vector Storage (Temporary for this session)
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings)
            
            # Initialize LLM & Chain
            llm = ChatGroq(api_key=api_key, model_name="llama-3.1-8b-instant", temperature=0)
            system_prompt = (
                "You are an expert research assistant. Use the provided context from multiple documents "
                "to answer the question. If you don't know, say 'I don't know.'\n\nContext: {context}"
            )
            prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
            
            # Create the RAG Chain
            combine_docs_chain = create_stuff_documents_chain(llm, prompt)
            st.session_state.rag_chain = create_retrieval_chain(vector_db.as_retriever(), combine_docs_chain)
            
            st.success(f"Library Ready! Processed {len(uploaded_files)} documents into {len(chunks)} searchable chunks.")

# --- 4. Chat Interface with History ---
st.header("💬 Chat with your Library")

# Display Conversation History
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["question"])
    with st.chat_message("assistant"):
        st.write(chat["answer"])
        with st.expander("🔍 View Evidence (Sources)"):
            for doc in chat["sources"]:
                st.info(f"**Doc:** {doc.metadata.get('source', 'Unknown')} | **Page:** {doc.metadata.get('page', 'N/A')}\n\n{doc.page_content[:300]}...")

# New User Input
user_input = st.chat_input("Ask a question about your documents...")

if user_input:
    if st.session_state.rag_chain:
        with st.spinner("Consulting library..."):
            response = st.session_state.rag_chain.invoke({"input": user_input})
            
            # Update Session State History [UI Enhancement]
            st.session_state.chat_history.append({
                "question": user_input,
                "answer": response["answer"],
                "sources": response["context"]
            })
            st.rerun() # Refresh to show new message immediately
    else:
        st.error("The engine is not ready. Please upload documents and click 'Build Library'.")