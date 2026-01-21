from twilio.rest import Client
from app.config import settings
from app.logger import logger

class WhatsAppClient:
    def __init__(self):
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        else:
            self.client = None
            logger.warning("Twilio credentials missing. WhatsApp messages won't be sent.")

    def send_message(self, to_number: str, body_text: str):
        if not self.client:
            logger.info(f"Simulating sending message to {to_number}: {body_text}")
            return

        try:
            # Twilio whatsapp numbers often need 'whatsapp:' prefix if not present
            if not to_number.startswith("whatsapp:"):
                to_number = f"whatsapp:{to_number}"
                
            from_number = settings.TWILIO_WHATSAPP_NUMBER
            if not from_number.startswith("whatsapp:"):
                from_number = f"whatsapp:{from_number}"

            message = self.client.messages.create(
                from_=from_number,
                body=body_text,
                to=to_number
            )
            logger.info(f"Message sent to {to_number}: {message.sid}")
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {str(e)}")

whatsapp_client = WhatsAppClient()
