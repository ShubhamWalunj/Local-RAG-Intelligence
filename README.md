📄 Local AI Document Intelligence Engine
Tagline: A high-performance RAG (Retrieval-Augmented Generation) system for secure, private conversation with local PDF documents.

This project enables users to transform static PDF files into an interactive knowledge base. By leveraging Llama 3.1 and ChromaDB, it provides an end-to-end pipeline for document ingestion, vectorization, and natural language querying with full source attribution.

✨ Features
Local Vector Storage: Uses ChromaDB for high-speed, persistent storage of document embeddings.

Context-Aware Q&A: Powered by Llama-3.1-8B-Instant for precise, human-like responses.

Source Attribution: Displays specific text chunks and page numbers used to generate each answer.

Secure Credential Management: Implements .env protocols to protect API keys from version control exposure.

Streamlit Interface: A clean, intuitive web UI for document uploading and real-time chatting.

🛠️ Installation
Ensure you have Python 3.9+ installed. Follow these steps to set up your local environment:

Clone the Repository:

Bash
git clone https://github.com/ShubhamWalunj/Local-RAG-Intelligence.git
cd Local-RAG-Intelligence
Create a Virtual Environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

Bash
pip install -r requirements.txt
🚀 Usage
Launch the Application:

Bash
streamlit run app.py
Interact:

Enter your Groq API Key in the sidebar.

Upload a PDF document.

Click "Build Knowledge Base" to trigger the RAG pipeline.

Ask questions in the chat interface.

📂 Project Structure
Plaintext
RAG_search_engine_project/
├── app.py                # Main Streamlit application and RAG logic
├── .env                  # Private environment variables (API keys)
├── .gitignore            # Security guard for sensitive files
├── requirements.txt      # Project dependency list
├── chroma_db/            # Local vector database storage
├── sample_document.pdf   # Demo data for testing
└── 01_data_ingestion.ipynb # Development notebook for vectorization testing
⚙️ Configuration
The project requires a .env file in the root directory. Add your credentials as follows:

Plaintext
GROQ_API_KEY=your_gsk_api_key_here
🤝 Contributing
Contributions are welcome! To contribute:

Fork the Project.

Create your Feature Branch (git checkout -b feature/AmazingFeature).

Commit your Changes (git commit -m 'Add some AmazingFeature').

Push to the Branch (git push origin feature/AmazingFeature).

Open a Pull Request.

📄 License
Distributed under the MIT License. See LICENSE for more information.

💡 Acknowledgments
Groq Cloud for providing high-speed inference.

LangChain for the robust orchestration framework.

HuggingFace for providing the all-MiniLM-L6-v2 embedding model.