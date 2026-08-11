import pytest
from src.chatbot import chat_with_bot
from unittest.mock import patch

def test_chat_with_bot_exact_match():
    # Mock qa_pairs to have exact match
    with patch('src.chatbot.qa_pairs', [{"question": "test question", "answer": "test answer"}]):
        response = chat_with_bot("test question")
        assert response == "test answer"

def test_chat_with_bot_retrieval():
    # Mock retrieval and LLM
    with patch('src.chatbot.retrieve_relevant_docs', return_value=["Some context"]), \
         patch('src.chatbot.generate_response', return_value="Generated response"):
        response = chat_with_bot("unknown question")
        assert response == "Generated response"

def test_chat_with_bot_no_docs():
    with patch('src.chatbot.retrieve_relevant_docs', return_value=[]):
        response = chat_with_bot("unknown question")
        assert "couldn't find enough information" in response

def test_chat_with_bot_cv_context():
    with patch('src.chatbot.retrieve_relevant_docs', return_value=["Some context"]), \
         patch('src.chatbot.generate_response', return_value="Response with CV"):
        response = chat_with_bot("question", cv_context="CV text")
        assert response == "Response with CV"
