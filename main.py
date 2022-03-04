
import os
from fastapi import Request
from fastapi.responses import HTMLResponse

from app import app
from search_qa import search_qa_format
from items import Item_jzmh
from jzmh import send_message, default_token
import api_config
from open_search import current_dir


@app.get("/")
def get_index():
    return HTMLResponse(
        content=open(os.path.join(current_dir, 'html', 'index.html')).read(),
        status_code=200)


@app.post("/v1/QA/search/jzmh/message")
@app.post("/v1/QA/search/jzmh/message/{jzmj_token}")
async def receive_message(item: Item_jzmh, request: Request, jzmj_token: str= None):
    """对接句子互动的api

    curl -XPOST localhost:1333/v1/QA/search/jzmh/message -H 'Content-Type: application/json' \
        -d '{
            "data": { "payload": { "text": "hello" }, "chatId": "fake" }
        }'

    curl -XPOST localhost:1333/v1/QA/search/jzmh/message/iamtoken -H 'Content-Type: application/json' \
        -d '{
            "data": { "payload": { "text": "hello" }, "chatId": "fake" }
        }'
    """
    if jzmj_token is None:
        jzmj_token = default_token
    search_text = item.data.payload.text
    format_return_data = search_qa_format(search_text, token=jzmj_token)
    return send_message(chatid=item.data.chatId, text=format_return_data, token=jzmj_token)
