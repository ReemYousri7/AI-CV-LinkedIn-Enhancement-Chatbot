from src.retrieval import retrieve_relevant_docs
from src.preprocess import load_qa_pairs
from src.llm import generate_response

# Load data only once
qa_pairs = load_qa_pairs("data/linkedin_career_chatbot_dataset.csv")

def chat_with_bot(user_input, conversation_history=None, cv_context=None):
    # Search for direct answer in data
    for pair in qa_pairs:
        if pair['question'].lower().strip() == user_input.lower().strip():
            return pair['answer']

    # If not found, use retrieval
    relevant_docs = retrieve_relevant_docs(user_input)

    if not relevant_docs:
        return "Sorry, I couldn't find enough information to answer your question."

    # If there is CV context, add it
    if cv_context:
        relevant_docs.append(f"Uploaded CV content: {cv_context}")

    # Use LLM to generate response from context
    response = generate_response(user_input, relevant_docs, conversation_history)
    return response
