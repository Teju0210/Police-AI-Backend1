import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
models = [
    'gemini-flash-lite-latest',
    'gemini-1.5-flash-latest',
    'gemini-2.5-flash-lite',
    'gemini-2.0-flash-lite',
    'gemini-3.5-flash-lite',
    'gemini-3.1-flash-lite',
    'gemini-2.5-flash',
    'gemini-2.5-pro'
]

for m in models:
    resp = requests.post(
        f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}',
        json={'contents':[{'parts':[{'text': 'hello'}]}]}
    ).json()
    if 'error' not in resp:
        print(f'SUCCESS: {m}')
    else:
        msg = resp.get('error', {}).get('message', '')
        print(f'FAILED {m}: {msg}')
