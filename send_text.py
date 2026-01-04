import requests
from dotenv import load_dotenv
import os

load_dotenv()

EVOLUTION_INSTANCE_NAME = os.getenv('EVOLUTION_INSTANCE_NAME')
AUTHENTICATION_API_KEY = os.getenv('AUTHENTICATION_API_KEY')
EVOLUTION_API_URL = os.getenv('EVOLUTION_API_URL')

def send_message(number, text):
   
    url = f'{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE_NAME}'
    headers = {
        'apikey': AUTHENTICATION_API_KEY,
        'Content-Type': 'application/json'
    }
    payload = { 
        'number': number,
        'text': text,
    }
    requests.post(
        url=url,
        json=payload,
        headers=headers,
    )