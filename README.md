# 📄 Local AI Document Intelligence Engine

**A high-performance RAG system for secure, private conversation with local PDF documents using Llama 3.1 and ChromaDB.**

---

## 🚀 Overview
This project enables users to transform static PDF files into an interactive knowledge base. By leveraging a **Retrieval-Augmented Generation (RAG)** architecture, it provides an end-to-end pipeline for document ingestion, vectorization, and natural language querying with full source attribution. 

Built with a focus on **Data Privacy**, all document processing and vector storage happen locally, ensuring sensitive information never leaves your environment.

## ✨ Features
* **Local Vector Storage:** Uses **ChromaDB** for high-speed, persistent storage of document embeddings.
* **Context-Aware Q&A:** Powered by **Llama-3.1-8B-Instant** via Groq for lightning-fast, precise responses.
* **Source Attribution:** Displays the specific text "chunks" and page numbers used as evidence for every answer.
* **Secure Credential Management:** Implements `.env` protocols to protect API keys from version control exposure.
* **Streamlit Interface:** A clean, intuitive web UI for document uploading and real-time chatting.

## 🛠️ Tech Stack
* **LLM:** Llama 3.1 (Groq Cloud)
* **Orchestration:** LangChain
* **Vector Database:** ChromaDB
* **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
* **Frontend:** Streamlit

## 📦 Installation & Setup
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/ShubhamWalunj/Local-RAG-Intelligence.git](https://github.com/ShubhamWalunj/Local-RAG-Intelligence.git)
    cd Local-RAG-Intelligence
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Environment:**
    Create a `.env` file in the root directory and add your Groq API Key:
    ```text
    GROQ_API_KEY=your_api_key_here
    ```

## 🚀 Usage
1.  **Launch the App:**
    ```bash
    streamlit run app.py
    ```
2.  **Interact:**
    * Enter your API Key in the sidebar (if not in .env).
    * Upload a PDF.
    * Click **"Build Knowledge Base"**.
    * Start chatting with your document!

## 📂 Project Structure
* `app.py`: Main application logic and RAG pipeline.
* `.env`: Private environment variables (Safely ignored by Git).
* `.gitignore`: Prevents sensitive files from being uploaded.
* `chroma_db/`: Directory where the local vector database is persisted.
* `requirements.txt`: List of Python dependencies.

## 📄 License
Distributed under the **MIT License**.

## 💡 Acknowledgments
* **Groq Cloud** for high-speed LLM inference.
* **LangChain** for the robust orchestration framework.
