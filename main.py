
from fastapi import Request
import pandas as pd

from app import app
from search_qa import search_qa_format
from items import Item_jzmh
from jzmh import send_message


@app.get("/")
def return_hello(request: Request):
    client_host = request.client.host
    client_port = request.client.port

    try:
        return client_host
    except:
        return  "I can't get ur information via %s" % client_host 


@app.post("/v1/QA/search/jzmh/sentResult")
async def sent_result(request: Request):
    print(await request.json())


@app.post("/v1/QA/search/jzmh/message")
async def receive_message(item: Item_jzmh,request : Request):
    search_text = item.data.payload.text
    format_return_data = search_qa_format(search_text)
    send_message(chatid=item.data.chatId, text=format_return_data)

