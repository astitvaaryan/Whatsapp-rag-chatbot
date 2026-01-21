import sys
import os
from pyngrok import ngrok, conf

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings

def start_ngrok():
    print("Starting ngrok...")
    
    # Optional: Set auth token if you have one
    # ngrok.set_auth_token("YOUR_AUTH_TOKEN")
    
    # Open a HTTP tunnel on the default port 8000
    public_url = ngrok.connect(8000).public_url
    print(f"Ngrok Tunnel Started: {public_url}")
    print(f"Update Twilio Webhook to: {public_url}/whatsapp/webhook")
    
    # Keep the script running
    try:
        # Just keep process alive
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down ngrok...")
        ngrok.kill()

if __name__ == "__main__":
    start_ngrok()
