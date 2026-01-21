def generate_rag_prompt(query: str, context_chunks: list, history: list) -> str:
    context_text = "\n\n".join([c['metadata']['text'] for c in context_chunks])
    
    chat_history_text = ""
    for msg in history:
        chat_history_text += f"{msg['role'].capitalize()}: {msg['content']}\n"
        
    prompt = f"""You are a helpful assistant for a WhatsApp chatbot.
    
Context from documents:
{context_text}

Chat History:
{chat_history_text}

User Question: {query}

Answer the user question based on the context above. If the answer is not in the context, say you don't know. 
Date citation to the source document if possible.
"""
    return prompt
