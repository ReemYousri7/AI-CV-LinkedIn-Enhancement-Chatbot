# AI CV & LinkedIn Enhancement Chatbot

An AI-powered career assistant that analyzes and improves CVs and LinkedIn profiles using Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), and semantic document retrieval.

The chatbot provides personalized recommendations for CV improvement, LinkedIn profile optimization, ATS compatibility, keyword optimization, professional summaries, and career branding.

---

## 🚀 Features

- CV analysis and improvement
- PDF and DOCX CV upload
- LinkedIn profile optimization
- Retrieval-Augmented Generation (RAG)
- Semantic document retrieval
- Context-aware AI responses
- ATS-friendly CV recommendations
- Keyword optimization
- Professional summary improvement
- Personalized career recommendations
- Conversation history support
- CV keyword and content analysis
- Knowledge-base-powered responses
- Fallback LLM model for improved reliability

---

## 🧠 How It Works

The system combines a knowledge base, semantic retrieval, and an LLM to generate personalized career recommendations.

### Workflow

1. The user asks a question about their CV or LinkedIn profile.
2. The system checks the career knowledge base for an exact matching question.
3. If no exact match is found, relevant documents are retrieved using semantic similarity.
4. The retrieved context is combined with the user's question and conversation history.
5. If a CV is uploaded, its extracted content is added to the context.
6. The LLM generates a personalized response.
7. The chatbot returns actionable recommendations to the user.

---

## 🏗️ System Architecture

```text
User
 │
 ▼
Streamlit Web Interface
 │
 ├── CV Upload (PDF / DOCX)
 │
 ▼
CV Processing
 │
 ├── Text Extraction
 ├── Keyword Analysis
 └── Recommendations
 │
 ▼
Chatbot
 │
 ├── Exact Question Matching
 │
 └── Semantic Retrieval
       │
       ▼
   ChromaDB Vector Store
       │
       ▼
   Retrieved Context
       │
       ▼
     Groq LLM
       │
       ▼
Personalized Career Recommendations
