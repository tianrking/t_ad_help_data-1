from itsdangerous import json
import pandas as pd

from opensearchpy import OpenSearch

from fastapi import Cookie, FastAPI
from typing import Optional
from fastapi import FastAPI
from fastapi import Request
from typing import List, Optional
from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Header
from pydantic import BaseModel
import requests # only for JZMH

# from sympy import content

from app import app
from search_qa import search_qa_format


@app.get("/")
def return_hello(request:Request):
    client_host = request.client.host
    client_port = request.client.port

    try:
        return client_host
    except:
        return  "I can't get ur information via %s" % client_host 


# 暂时仅仅处理文字 
class Payload_Struct(BaseModel):
    # text:Optional[str] = ""
    text:str

class Item_jzmh_data(BaseModel):
    messageId: Optional[str] = ""
    chatId: Optional[str] = "" # juzi system chatId
    avatar: Optional[str] = ""
    roomTopic: Optional[str] = ""
    roomId: Optional[str] = "" # room wxid nullable
    contactName: Optional[str] = "" # message conact name
    contactId: Optional[str] = ""
    payload: Optional[Payload_Struct] = ""
    # payload: Optional[Payload_Struct] = None
    type: Optional[str] = ""
    timestamp: Optional[int] = "" # message timestamp
    token: Optional[str] = "" # token
    botId: Optional[str] = "" # botId
    contactType: Optional[int] = ""
    coworker: Optional[bool] = "" # is coworker or not
    botId: Optional[str] = ""
    botWxid: Optional[str] = ""
    botWeixin: Optional[str] = ""

class Item_jzmh(BaseModel):
    data:Optional[Item_jzmh_data]= ""

@app.post("/v1/QA/search/jzmh/sentResult")
async def sent_result(request: Request):
    print(await request.json())


@app.post("/v1/QA/search/jzmh/message")
async def receive_message(item: Item_jzmh,request : Request):

    search_text = item.data.payload.text
    format_return_data = search_qa_format(search_text)
    url_jzmh_message_send = "https://ex-api.botorange.com/message/send"
    # jzmh_message = json.dumps(return_data)

    send_messageId = "6214b19ea66c67d78d0f133d"
    print(item.data.messageId)
    jzmh_data = {
        "chatId":  item.data.chatId, #"6214b19ea66c67d78d0f133d",
        "token": "6214b16a39011db76498866b",
        "messageType": 0, # MessageType, check below
        "payload": {
            "text": format_return_data, # str(return_data).replace('{',"").replace('}',"") ,
            "mention": [] # mention list, you can only set it when you send text message to room,
        },
        "externalRequestId": "",
    }

    res = requests.post(url=url_jzmh_message_send, json=jzmh_data, timeout=30)
    ############################
    ###########################
    # return  json.dumps(return_data) 
