from groq import Groq

# Create Groq client with your key
client = Groq(api_key="Your API Key")

def generate_response(query: str, context: list, conversation_history: list = None) -> str:
    """
    Generate a response using Groq based on the question and context.
    Supports the llama-3.3-70b-versatile model with fallback in case of error.
    """

    # Prepare the texts
    context_text = "\n".join(context)
    history_text = "\n".join([
        f"User: {msg['content']}" if msg['role'] == 'user' else f"Assistant: {msg['content']}"
        for msg in (conversation_history or [])[-4:]
    ])

    prompt = f"""
You are an intelligent assistant for improving LinkedIn profiles and writing CVs. Use the following context to answer the question:

Context:
{context_text}

Conversation History:
{history_text}

Question: {query}

The answer should be in English, helpful, and direct.
"""

    try:
        # First attempt using the primary model
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"⚠️ Primary model error: {e}")
        print("🔄 Switching to fallback model (llama-3.1-8b-instant)...")

        # Second attempt using the fallback model
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e2:
            print(f"❌ Fallback model error: {e2}")
            return "Sorry, an error occurred in generating the answer. Please try again later."

# 🧪 Quick test:
if __name__ == "__main__":
    result = generate_response(
        "How do I write a professional summary on LinkedIn?",
        ["LinkedIn profile tips", "CV writing guide"]
    )
    print("\n🤖 Response:")
    print(result)
