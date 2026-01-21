from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Whatsapp RAG Chatbot"
    APP_VERSION: str = "0.0.1"
    APP_BASE_URL: str = "http://localhost:8000"
    
    # WhatsApp (Twilio)
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_WHATSAPP_NUMBER: str = ""
    
    # LLM
    # Options: "openai", "groq"
    LLM_PROVIDER: str = "groq"
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    
    # Database
    DB_URL: str = "sqlite:///./app.db"
    
    class Config:
        env_file = ".env"

settings = Settings()
