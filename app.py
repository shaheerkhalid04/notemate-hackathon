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

# Initialize
if 'rag_engine' not in st.session_state:
    st.session_state.rag_engine = RAGEngine()
if 'generator' not in st.session_state:
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        st.session_state.generator = ContentGenerator(api_key)
    else:
        st.error("⚠️ Please add your GROQ_API_KEY to .env file")
        st.info("Get your free API key from https://console.groq.com/keys")
        st.stop()
if 'collection_name' not in st.session_state:
    st.session_state.collection_name = None

# Header
st.title("🚀 NOTEMATE - GenAI Study Pack Generator")
st.caption("Transform your notes into AI-powered learning materials using RAG + GenAI!")

# Sidebar
with st.sidebar:
    st.header("📁 Upload Your Notes")
    
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=['pdf', 'docx', 'txt'],
        help="Upload PDF, Word, or text files"
    )
    
    if uploaded_file:
        if st.button("🔄 Process Document", type="primary", use_container_width=True):
            with st.spinner("Processing your document..."):
                # Create uploads folder
                os.makedirs("./uploads", exist_ok=True)
                
                # Save file
                file_path = f"./uploads/{uploaded_file.name}"
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                
                # Parse document
                parser = DocumentParser()
                
                if uploaded_file.name.endswith('.pdf'):
                    text = parser.parse_pdf(file_path)
                elif uploaded_file.name.endswith('.docx'):
                    text = parser.parse_docx(file_path)
                else:
                    text = parser.parse_txt(file_path)
                
                # Process text
                chunks = parser.chunk_text(text)
                collection_name = uploaded_file.name.replace('.', '_').replace(' ', '_')
                st.session_state.collection_name = collection_name
                
                # Store in vector DB
                st.session_state.rag_engine.create_collection(collection_name)
                st.session_state.rag_engine.add_documents(collection_name, chunks)
                
                st.success(f"✅ Successfully processed {len(chunks)} chunks!")
                st.balloons()
    
    if st.session_state.collection_name:
        st.divider()
        st.info(f"📄 Active Document: {st.session_state.collection_name}")

# Main content
if st.session_state.collection_name:
    tabs = st.tabs([
        "🎯 Quiz Generator",
        "📚 Lesson Creator", 
        "📖 Story Mode",
        "🗺️ Mind Map",
        "📅 Study Planner",
        "🎓 Multi-Level Explain",
        "📋 Summary & Cards"
    ])
    
    # Tab 1: Quiz Generator
    with tabs[0]:
        st.header("AI-Powered Quiz Generator")
        st.caption("Generate different types of practice questions from your notes")
        
        col1, col2 = st.columns(2)
        with col1:
            num_q = st.number_input("Number of questions", min_value=1, max_value=10, value=5)
        with col2:
            q_type = st.selectbox("Question type", ["mcq", "scenario", "short"])
        
        if st.button("🎯 Generate Quiz", type="primary"):
            with st.spinner("Creating quiz..."):
                context = st.session_state.rag_engine.query(
                    st.session_state.collection_name,
                    "main concepts and important topics",
                    n_results=5
                )
                
                quiz = st.session_state.generator.generate_quiz(context, num_q, q_type)
                st.markdown("### Your Generated Quiz:")
                st.markdown(quiz.get("content", "No quiz generated"))

    
    # Tab 2: Lesson Generator
    with tabs[1]:
        st.header("Auto-Lesson Generator")
        st.caption("Create complete lessons with objectives and exercises")
        
        topic = st.text_input("Enter topic for lesson", placeholder="e.g., Machine Learning, Photosynthesis, World War 2")
        
        if st.button("📚 Generate Lesson", type="primary") and topic:
            with st.spinner(f"Creating lesson about '{topic}'..."):
                context = st.session_state.rag_engine.query(
                    st.session_state.collection_name,
                    topic,
                    n_results=5
                )
                
                lesson = st.session_state.generator.generate_lesson(topic, context)
                st.markdown("### Generated Lesson:")
                st.markdown(lesson)
    
    # Tab 3: Story Mode
    with tabs[2]:
        st.header("Story-Based Learning")
        st.caption("Turn complex concepts into memorable stories")
        
        concept = st.text_input("Enter concept to storify", placeholder="e.g., Database Indexing, Cell Division, Supply and Demand")
        
        if st.button("📖 Generate Story", type="primary") and concept:
            with st.spinner("Creating story..."):
                context = st.session_state.rag_engine.query(
                    st.session_state.collection_name,
                    concept,
                    n_results=3
                )
                
                story = st.session_state.generator.generate_story_mode(concept, context)
                st.markdown("### Your Learning Story:")
                st.write(story)
    
    # Tab 4: Mind Map
    with tabs[3]:
        st.header("Mind Map Generator")
        st.caption("Visualize concept hierarchy from your notes")
        
        if st.button("🗺️ Generate Mind Map", type="primary"):
            with st.spinner("Creating mind map..."):
                context = st.session_state.rag_engine.query(
                    st.session_state.collection_name,
                    "all topics subtopics concepts hierarchy structure",
                    n_results=10
                )
                
                mindmap = st.session_state.generator.generate_mindmap(context)
                st.markdown("### Concept Mind Map:")
                st.code(mindmap, language="text")
    
    # Tab 5: Study Planner
    with tabs[4]:
        st.header("Personalized Study Plan")
        st.caption("Get a day-by-day study schedule")
        
        col1, col2 = st.columns(2)
        
        with col1:
            chapters = st.text_area("Enter chapters/topics (one per line)", 
                                   placeholder="Chapter 1: Introduction\nChapter 2: Basics\nChapter 3: Advanced",
                                   height=100)
            days = st.slider("Days until exam", min_value=1, max_value=30, value=7)
        
        with col2:
            difficulty = st.select_slider(
                "Your current level",
                ["Beginner", "Intermediate", "Advanced"],
                value="Intermediate"
            )
            st.write("")
            st.write("")
            plan_btn = st.button("📅 Generate Study Plan", type="primary", use_container_width=True)
        
        if plan_btn and chapters:
            with st.spinner("Creating personalized study plan..."):
                chapter_list = [c.strip() for c in chapters.split('\n') if c.strip()]
                plan = st.session_state.generator.generate_study_plan(chapter_list, days, difficulty)
                st.markdown("### Your Study Plan:")
                st.text(plan)
    
    # Tab 6: Multi-Level Explainer
    with tabs[5]:
        st.header("3-Level Concept Explainer")
        st.caption("Understand concepts at different complexity levels")
        
        explain_concept = st.text_input("Enter concept to explain", 
                                       placeholder="e.g., Recursion, Quantum Physics, Democracy")
        
        if st.button("🎓 Generate Explanations", type="primary") and explain_concept:
            with st.spinner("Generating explanations at 3 levels..."):
                context = st.session_state.rag_engine.query(
                    st.session_state.collection_name,
                    explain_concept,
                    n_results=3
                )
                
                levels = st.session_state.generator.explain_at_levels(explain_concept, context)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("### 🧒 Beginner Level")
                    st.info(levels.get('beginner', 'Generating...'))
                
                with col2:
                    st.markdown("### 🎓 Intermediate Level")
                    st.warning(levels.get('intermediate', 'Generating...'))
                
                with col3:
                    st.markdown("### 🎯 Advanced Level")
                    st.error(levels.get('advanced', 'Generating...'))
    
    # Tab 7: Summary & Flashcards
    with tabs[6]:
        st.header("Summary & Flashcards")
        st.caption("Quick revision tools")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 Generate Summary")
            if st.button("Create Summary", type="primary", use_container_width=True):
                with st.spinner("Generating comprehensive summary..."):
                    context = st.session_state.rag_engine.query(
                        st.session_state.collection_name,
                        "comprehensive overview all main topics key points",
                        n_results=10
                    )
                    
                    summary = st.session_state.generator.generate_summary(context)
                    st.markdown("### Summary:")
                    st.write(summary)
        
        with col2:
            st.subheader("🎴 Generate Flashcards")
            num_cards = st.slider("Number of flashcards", min_value=5, max_value=20, value=10)
            
            if st.button("Create Flashcards", type="primary", use_container_width=True):
                with st.spinner("Generating flashcards..."):
                    context = st.session_state.rag_engine.query(
                        st.session_state.collection_name,
                        "key terms definitions important concepts",
                        n_results=5
                    )
                    
                    cards = st.session_state.generator.generate_flashcards(context, num_cards)
                    st.markdown("### Flashcards:")
                    st.text(cards)
else:
    # Welcome screen
    st.info("👈 Please upload a document to start generating AI-powered study materials")
    
    st.divider()
    
    # Feature showcase
    st.subheader("✨ What NOTEMATE Can Do")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📚 Content Generation**
        - Auto-generate complete lessons
        - Create story-based learning
        - Build concept mind maps
        """)
    
    with col2:
        st.markdown("""
        **🎯 Practice Materials**
        - Multi-format quiz generation
        - Flashcard creation
        - Practice exercises
        """)
    
    with col3:
        st.markdown("""
        **🎓 Personalized Learning**
        - 3-level explanations
        - Custom study plans
        - Smart summaries
        """)
    
    st.divider()
    
    st.subheader("🚀 Powered by RAG + GenAI")
    st.caption("Using Retrieval-Augmented Generation for context-aware content creation")