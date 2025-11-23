import streamlit as st
import os
from backend.document_parser import DocumentParser
from backend.rag_engine import RAGEngine
from backend.generator import ContentGenerator
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(
    page_title="NOTEMATE GenAI",
    page_icon="🚀",
    layout="wide"
)

# Fix: initialize collection_name
if "collection_name" not in st.session_state:
    st.session_state.collection_name = None

# Initialize RAG engine
if 'rag_engine' not in st.session_state:
    st.session_state.rag_engine = RAGEngine()

# Initialize LLM generator
if 'generator' not in st.session_state:
    api_key = None

    # Try Streamlit Secrets first (Cloud)
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

    # Fallback: try .env (local development)
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        st.session_state.generator = ContentGenerator(api_key)
    else:
        st.error("⚠️ GROQ_API_KEY not found.")
        st.info(
            'In Streamlit Cloud, set it under "Settings → Secrets" as:\n'
            'GROQ_API_KEY = "your_key_here"'
        )
        st.stop()

# Debug: show what secrets are available
st.write("Secrets keys:", list(st.secrets.keys()))

# HEADER
st.title("🚀 NOTEMATE - GenAI Study Pack Generator")
st.caption("Transform your notes into AI-powered learning materials using RAG + GenAI!")

# SIDEBAR
with st.sidebar:
    st.header("📁 Upload Your Notes")

    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'txt'])

    if uploaded_file:
        if st.button("🔄 Process Document", type="primary", use_container_width=True):

            with st.spinner("Processing your document..."):
                os.makedirs("./uploads", exist_ok=True)

                file_path = f"./uploads/{uploaded_file.name}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                parser = DocumentParser()

                if uploaded_file.name.endswith(".pdf"):
                    text = parser.parse_pdf(file_path)
                elif uploaded_file.name.endswith(".docx"):
                    text = parser.parse_docx(file_path)
                else:
                    text = parser.parse_txt(file_path)

                chunks = parser.chunk_text(text)
                collection_name = uploaded_file.name.replace(".", "_").replace(" ", "_")
                st.session_state.collection_name = collection_name

                st.session_state.rag_engine.create_collection(collection_name)
                st.session_s_
