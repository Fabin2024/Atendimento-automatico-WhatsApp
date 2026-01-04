from fastapi import FastAPI, Request
from send_text import send_message
from bot import agente, knowledge
import asyncio
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.chunking.semantic import SemanticChunking


app = FastAPI()



@app.on_event("startup")
async def load_rag_data():
    print("🔄 Carregando base de conhecimento...")
    await knowledge.add_content_async(path="Pdfs")  # ✅ versão assíncrona
    print("✅ Base carregada!")

@app.post("/webhook")
async def receber_dados(request: Request):
    data = await request.json()

    msg = data.get('data', data) 

    if isinstance(msg, dict):
        messages = [msg]
    else:
        messages = msg

    for m in messages:
        key = m.get('key', {})

        is_from_me = key.get('fromMe', False)

        if is_from_me:
            print("Mensagem enviada por mim, ignorando...")
            continue

        number = key.get('remoteJid')
        
        message_obj = m.get('message', {})
        text_received = message_obj.get('conversation', "")

        response = await agente.arun(text_received,session_id=number)
        

        if number and text_received:
            print(f"Respondendo para {number}: {text_received}")
            send_message(number=number, text= str(response.content))

    return {"status": "ok"}