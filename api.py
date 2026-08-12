# File: api.py
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def query_groq(prompt: str, model: str = None) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in .env file.")

    try:
        client = Groq(api_key=api_key)

        #  Use latest working Groq model
        model = model or "llama-3.3-70b-versatile"

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        raise Exception(f"Error querying Groq: {e}")

