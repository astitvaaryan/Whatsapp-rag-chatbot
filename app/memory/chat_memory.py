from collections import deque

# Simple in-memory storage: {user_phone: deque(maxlen=5)}
# In production, use Redis or Database
chat_histories = {} 
MAX_HISTORY = 5

def get_user_history(user_id: str) -> list:
    return list(chat_histories.get(user_id, []))

def add_user_message(user_id: str, message: str, role: str):
    if user_id not in chat_histories:
        chat_histories[user_id] = deque(maxlen=MAX_HISTORY)
    
    # role: 'user' or 'assistant'
    chat_histories[user_id].append({"role": role, "content": message})
