📘 NOTEMATE – GenAI Study Pack Generator

Transform your notes into AI-powered learning materials using RAG + GenAI.

🚀 Overview

NOTEMATE is an AI-powered study assistant built with Streamlit, FAISS, Sentence Transformers, and Groq gpt-oss-120b.
It allows users to upload notes (PDF, DOCX, TXT) and instantly generate:

Quizzes (MCQ / Scenario / Short)

Complete lessons

Stories for concept understanding

Mind maps

Study planners

Multi-level explanations

Summaries & Flashcards

Powered by Retrieval-Augmented Generation (RAG) to keep outputs aligned with uploaded notes.

🧠 Features
📄 Document Processing

Upload PDF, DOCX, or TXT

Extract text using PyPDF2 / python-docx

Split into semantic chunks

Generate embeddings with MiniLM-L6-v2

🔍 Retrieval Engine (RAG)

Store embeddings in FAISS L2 index

Fast, semantic search

Retrieve most relevant chunks as LLM context

🤖 AI Generation

Using Groq LLM for:

Quizzes (MCQ, scenario, short)

Lessons (objectives, concepts, examples, exercises)

Stories (narrative explanations)

Mind maps

Study plans (day-by-day)

3-level explainers (beginner → advanced)

Summaries & flashcards

🏗️ Project Structure
notemate/
│
├── app.py                     # Main Streamlit app UI
│
├── backend/
│   ├── document_parser.py     # PDF/DOCX/TXT parsing + chunking
│   ├── rag_engine.py          # FAISS vector DB + embeddings
│   └── generator.py           # Groq LLM-based content generation
│
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Optional: Docker deployment
└── README.md                  # Project documentation

🔧 Installation (Local Development)
1. Clone the repo
git clone https://github.com/yourusername/notemate.git
cd notemate

2. Create virtual environment
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows

3. Install dependencies
pip install -r requirements.txt

4. Create .env

Create a file named .env:

GROQ_API_KEY=your_key_here

5. Run the app
streamlit run app.py

☁️ Deployment (Streamlit Cloud)
1. Upload the repo to GitHub
2. Open:

https://share.streamlit.io

→ Create new app → Select GitHub repo

3. Add Secrets:

Go to:
App → Settings → Secrets

Paste:

GROQ_API_KEY = "your_groq_api_key_here"

4. Deploy

Streamlit Cloud will automatically:

Install requirements

Run app.py

Host your app publicly

🔑 Environment Variables
Variable	Description
GROQ_API_KEY	Required to access Groq LLM API
GROQ_MODEL	Optional. Defaults to openai/gpt-oss-120b (Groq retired llama-3.3-70b-versatile on 16 Aug 2026)
🛠️ Technologies Used

Streamlit – UI

FAISS CPU – vector database

Sentence Transformers – MiniLM embeddings

Groq gpt-oss-120b, LLM inference

PyPDF2 / python-docx – document parsing

NumPy – math utilities

🤝 Contributing

Contributions are welcome!
Create an issue or submit a pull request.

📜 License

MIT License — free for personal & commercial use.

⭐ Support

If you like NOTEMATE, please ⭐ star the repository on GitHub!
