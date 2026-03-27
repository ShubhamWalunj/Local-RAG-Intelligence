import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from dotenv import load_dotenv

# This looks for the .env file and loads the variables
load_dotenv()
secret_api_key = os.getenv("GROQ_API_KEY")

# --- 1. Page Configuration ---
st.set_page_config(page_title="Local Enterprise RAG", layout="wide")
st.title("📄 AI Document Intelligence Engine")
st.markdown("---")

# --- 2. Sidebar for Settings ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Groq API Key", type="password")
    uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
    process_button = st.button("Build Knowledge Base")

# --- 3. Backend Logic (The Engine) ---
if uploaded_file and api_key and process_button:
    with st.spinner("Processing document... This involves Chunking & Vectorization."):
        # Save uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Ingestion & Chunking
        loader = PyPDFLoader("temp.pdf")
        pages = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(pages)
        
        # Vector Storage (ChromaDB)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings)
        
        # Initialize LLM
        llm = ChatGroq(api_key=api_key, model_name="llama-3.1-8b-instant", temperature=0)
        
        # Build RAG Chain
        system_prompt = "Use the context to answer the question. Context: {context}"
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
        chain = create_retrieval_chain(vector_db.as_retriever(), create_stuff_documents_chain(llm, prompt))
        
        # Store in Session State (to keep the app 'awake')
        st.session_state.rag_chain = chain
        st.success("Database Ready! You can now ask questions.")

# --- 4. Chat Interface with Source Attribution ---
st.header("Chat with your Document")
user_input = st.text_input("Ask a question about the PDF:")

if user_input:
    if "rag_chain" in st.session_state:
        with st.spinner("Thinking..."):
            response = st.session_state.rag_chain.invoke({"input": user_input})
            
            # Display the AI Answer
            st.markdown(f"**AI Answer:** {response['answer']}")
            
            # Display the Sources (The Data Engineer part!)
            with st.expander("View Source Context (Evidence)"):
                for i, doc in enumerate(response["context"]):
                    st.write(f"**Chunk {i+1} from Page {doc.metadata.get('page', 'N/A')}:**")
                    st.info(doc.page_content[:300] + "...")
    else:
        st.error("Please upload a PDF and click 'Build Knowledge Base' first.")