from fastapi import APIRouter, Form, Request, Depends
from app.logger import logger
from app.whatsapp.twilio_client import whatsapp_client
from app.memory.chat_memory import add_user_message, get_user_history
from app.rag.retriever import retrieve_context
from app.llm.client import llm_client
from app.llm.prompt import generate_rag_prompt
from app.db.session import get_db
from app.db.queries import search_faqs, get_all_faqs
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/webhook")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Handle incoming WhatsApp messages from Twilio.
    """
    try:
        user_id = From.replace("whatsapp:", "")
        message_body = Body.strip()
        
        logger.info(f"Received message from {user_id}: {message_body}")
        
        # 1. Update Memory
        add_user_message(user_id, message_body, "user")
        
        # 2. Check Database Intent
        response_text = ""
        
        logger.info("Processing intent...")

        if "faq" in message_body.lower():
            faqs = get_all_faqs(db)
            if faqs:
                response_text = "Here are some FAQs:\n" + "\n".join([f"- {f.question}: {f.answer}" for f in faqs])
            else:
                response_text = "No FAQs found in database."
                
        elif "contact" in message_body.lower():
            # Retrieve contacts... 
            # (Assuming we implement get_all_contacts in queries if needed, simplified here)
            response_text = "Contact admin@example.com for more info."
            
        else:
            # 3. RAG Pipeline
            # Retrieve context
            context_chunks = retrieve_context(message_body)
            
            if not context_chunks:
                # Fallback if no docs
                response_text = "I couldn't find any documents to answer your question."
                # Or ask LLM without context
            
            else:
                # Generate Answer
                history = get_user_history(user_id)
                prompt = generate_rag_prompt(message_body, context_chunks, history)
                response_text = llm_client.generate_answer(prompt)
                
                # Append citations
                sources = set([c['metadata']['source'] for c in context_chunks])
                if sources:
                    response_text += "\n\nSources:\n" + "\n".join([f"- {s}" for s in sources])

        # 4. Update Memory with Assistant Reply
        add_user_message(user_id, response_text, "assistant")
        
        # 5. Send Reply
        logger.info(f"Generated reply: {response_text}")
        whatsapp_client.send_message(user_id, response_text)
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        # Optional: Send error message back to user if critical
        return {"status": "error", "message": str(e)}
        
    return {"status": "success"}
