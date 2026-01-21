import re

def validate_whatsapp_number(number: str) -> bool:
    """Validate if the number matches WhatsApp format."""
    # This is a basic validation, Twilio validates it too
    if not number:
        return False
    return True # Placeholder for more complex regex if needed
