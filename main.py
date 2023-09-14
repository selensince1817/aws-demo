import httpx
from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv
from mangum import Mangum

from llm.LLM import Agent


client = httpx.AsyncClient()

app = FastAPI()
load_dotenv()
TOKEN = os.getenv("TG_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

agent = Agent()
handler = Mangum(app)


@app.get("/")
def index():
    return "<h1>pi</h1>"


@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    chat_id = data['message']['chat']['id']
    text = data['message']['text']

    if text in ['/reset']:
        agent.llm_chain.memory.clear()
        resp = 'Reset complete!.'
    else:
        # resp = agent.aget_reply(text)
        resp = text
    print(resp)

    payload = {"text": resp, "chat_id": chat_id}
    await client.post(f"{BASE_URL}/sendMessage", json=payload)
    # print('sent ' + resp)
    return
