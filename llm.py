# llm.py
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL  = "llama-3.1-8b-instant"


def ask_llm(question: str, context: str = "", history: list = []) -> str:
    """
    Send question to Groq LLM with context and history.
    """
    from context_builder import build_structured_prompt

    # Build structured prompt using context
    structured_prompt = build_structured_prompt(question, context)

    # System message
    system_message = {
        "role"   : "system",
        "content": (
            "You are a helpful, honest AI assistant. "
            "Always answer based on the provided context. "
            "Never make up information you are not sure about."
        )
    }

    # Start messages with system
    messages = [system_message]

    # Add conversation history
    if history:
        messages.extend(history)

    # Add current structured prompt
    messages.append({
        "role"   : "user",
        "content": structured_prompt
    })

    # Call Groq
    response = client.chat.completions.create(
        model      = MODEL,
        messages   = messages,
        temperature= 0.3,   # lower = more focused, less creative
        max_tokens = 1024,
    )

    return response.choices[0].message.content


def get_token_usage(question: str, answer: str) -> dict:
    """Estimate token usage."""
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")

    input_tokens  = len(enc.encode(question))
    output_tokens = len(enc.encode(answer))

    return {
        "input_tokens" : input_tokens,
        "output_tokens": output_tokens,
        "total_tokens" : input_tokens + output_tokens
    }