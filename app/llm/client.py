import openai
import os
from groq import Groq
from app.config import settings

class LLMClient:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER.lower()
        self.client = None
        
        if self.provider == "openai" and settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        elif self.provider == "groq" and settings.GROQ_API_KEY:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
        
    def generate_answer(self, prompt: str) -> str:
        try:
            if self.provider == "openai":
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                return response.choices[0].message.content
                
            elif self.provider == "groq":
                if not self.client:
                    return "Groq API Key missing."
                
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="llama-3.3-70b-versatile", # Updated model
                )
                return chat_completion.choices[0].message.content
                
            else:
                return "No valid LLM provider configured (openai or groq)."
                
        except Exception as e:
            return f"Error contacting LLM ({self.provider}): {str(e)}"

llm_client = LLMClient()
