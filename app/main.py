from fastapi import FastAPI
from app.config import settings
from app.whatsapp.webhook import router as whatsapp_router
from app.db.session import engine
from app.db.models import Base

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.include_router(whatsapp_router, prefix="/whatsapp", tags=["whatsapp"])

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.APP_NAME}!"}
