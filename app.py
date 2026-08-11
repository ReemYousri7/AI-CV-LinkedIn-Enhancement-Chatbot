
import streamlit as st
from src.chatbot import chat_with_bot
from src.cv_processor import process_cv_file
import tempfile
import os

# Custom CSS for professional styling
st.markdown("""
<style>
    .main {
        direction: ltr;
        text-align: left;
        background-color: #f8f9fa;
    }
    .stChatMessage {
        direction: ltr;
        text-align: left;
    }
    .stChatInput {
        direction: ltr;
        text-align: left;
    }
    .title {
        font-size: 3em;
        color: #2c3e50;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.3em;
        color: #34495e;
        text-align: center;
        margin-bottom: 30px;
        font-style: italic;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        color: #95a5a6;
        font-size: 0.9em;
        border-top: 1px solid #ecf0f1;
        padding-top: 20px;
    }
    .sidebar-content {
        background-color: #ecf0f1;
        padding: 20px;
        border-radius: 10px;
    }
    .upload-section {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .chat-section {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="LinkedIn & CV Assistant", page_icon="💼", layout="wide")

# Sidebar with CV upload and tips
with st.sidebar:
    # CV Upload section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.subheader("📎 Upload CV for Analysis (Optional)")
    uploaded_file = st.file_uploader("Upload your CV (PDF or DOCX) for personalized recommendations:", type=["pdf", "docx"])
    cv_analysis = None
    if uploaded_file is not None:
        with st.spinner("Analyzing CV..."):
            # Save to temp file for processing
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            cv_analysis = process_cv_file(tmp_file_path)
            os.unlink(tmp_file_path)  # Clean up
        if "error" in cv_analysis:
            st.error(cv_analysis["error"])
        else:
            st.success("CV analyzed successfully!")
            with st.expander("📊 CV Analysis"):
                st.write(f"**Word count:** {cv_analysis['length']}")
                st.write(f"**Existing keywords:** {', '.join(cv_analysis['keywords'])}")
                if cv_analysis['recommendations']:
                    st.write("**Improvement recommendations:**")
                    for rec in cv_analysis['recommendations']:
                        st.write(f"- {rec}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.header("💡 Professional Tips")
    st.markdown("""
    **LinkedIn Optimization:**
    - Incorporate industry-specific keywords
    - Maintain a professional profile photo
    - Regularly share insightful content

    **CV Enhancement:**
    - Keep it concise and targeted
    - Use clean, readable fonts
    - Highlight achievements over duties
    """)
    if st.button("🗑️ Clear Conversation"):
        st.session_state["messages"] = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Main content
st.markdown('<h1 class="title">💼 LinkedIn & CV Career Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-powered tool to optimize your LinkedIn profile and create ATS-friendly CVs.</p>', unsafe_allow_html=True)

# Chat section
st.markdown('<div class="chat-section">', unsafe_allow_html=True)
st.subheader("💬 AI Career Assistant Chat")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    role = msg.get("role", "user")
    content = msg.get("content", "")
    with st.chat_message(role):
        st.markdown(content)

if prompt := st.chat_input("Ask about LinkedIn optimization or CV improvement:"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Analyzing and responding..."):
            cv_context = cv_analysis.get("extracted_text") if cv_analysis else None
            response = chat_with_bot(prompt, st.session_state["messages"], cv_context)
            st.markdown(response)

    st.session_state["messages"].append({"role": "assistant", "content": response})
st.markdown('</div>', unsafe_allow_html=True)
