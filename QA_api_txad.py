from itsdangerous import json
import pandas as pd

from opensearchpy import OpenSearch

from fastapi import Cookie, FastAPI
from typing import Optional
from fastapi import FastAPI
from fastapi import Request
from typing import List, Optional
from fastapi import FastAPI,File
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Header
from pydantic import BaseModel
import requests # only for JZMH


from sentence_transformers import SentenceTransformer, util
from sympy import content
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

host = 'localhost'
port = 9200
auth = ('admin', 'admin')

client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    # client_cert = client_cert_path,
    # client_key = client_key_path,
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    # ca_certs = ca_certs_path
)

id=1

df = pd.read_csv("/home/tianrking/t_ad_help_data/data/ad_weixin_qq_com_guide_titile_clean.csv")
print(df.head())
index_name = 'qa_index_768'
# 'Access-Control-Allow-Origin'
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def return_hello(request:Request):
    client_host = request.client.host
    client_port = request.client.port

    try:
        return client_host
    except:
        return  "I can't get ur information via %s" % client_host 

@app.get("/v1/QA/{_Q}")
def GET_QA_V1(_Q):
    embedding = model.encode(_Q, convert_to_tensor=True)
    print(embedding)
    return {"txt": _Q,"embedding":embedding.tolist()}


class Item_sts(BaseModel):
    text: Optional[str] = ""

   
@app.post("/v1/QA/add")
def create_item(item: Item_sts):
    
    embedding = model.encode(item.text, convert_to_tensor=True)
    _Q_vec = embedding.tolist()
    get_df = df[df['KEY']==item.text]
    for url in get_df['URL']:
        id  = url.split('/guide/')[1]
        print(id)
        # print(Q_text)
        embedding = model.encode(item.text, convert_to_tensor=True)
        _Q_vec = embedding.tolist()
        document = {
            'Q_text':item.text,
            'Q_vec':embedding.tolist(),
            'Ans':url,
        }
        response = client.index(
            index = index_name,
            body = document,
            id = id,
            refresh = True
        )
    # print(len(embedding.tolist()))
    print('\nAdding document:')
    # print(df[df['KEY']=='朋友圈信息流'].head(1))
    
    return { 'answer':df[df['KEY']==item.text]}

# curl -X POST -k "127.0.0.1:1333/api/sts/" -H 'Content-Type: application/json' -d' { "text": "ok" } '

@app.post("/v1/QA/search")
def create_item(item: Item_sts):
    
    embedding = model.encode(item.text, convert_to_tensor=True)
    _Q_vec = embedding.tolist()
    
    
    query = {
        'size': 5,
        'query': {
            "knn": {
            "Q_vec": {
                "vector": _Q_vec ,
                "k": 2
                }
            }
        }
    }

    response = client.search(
        body = query,
        index = index_name
    )
    print('\nSearch results: %s' %str(item.text))

    return_data = {}
    
    time=0
    for i in response['hits']['hits']:
        print(i['_source']['Q_text'],i['_source']['Ans'],i['_score'],i['_id'])
        # return {'ANS':i['_source']['Ans']}
        # return_data.update('Q_text':i['_source']['Q_text'])
        # return { 'answer':response}
        return_data[time] = {'Q':i['_source']['Q_text'],'Score':i['_score'],'Ans':i['_source']['Ans']}  # {'Q_text':i['_source']['Q_text'],'Ans':i['_source']['Ans'],'Score':i['_score']}
        time = time + 1
    # print(return_data)
    # print(type(return_data))  dict2json
    return  json.dumps(return_data) 

## 测试 json 的结构 以便确认构造是否正确
@app.post("/v1/QA/search/jzmh/messagee")
async def veiw_server_json(request : Request):
    data_json =  await request.json()
    print(data_json)
    
    data_body =  await request.body()
    print(data_body)
    


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

@app.post("/v1/QA/search/jzmh/message")
async def create_item(item: Item_jzmh,request : Request):
    
    # print(item)
    # return
    # try:
    # data =  await request.json()
    # print(data)
    search_text = item.data.payload.text
    # except:
    #     search_text = item.payload.content
    embedding = model.encode(search_text, convert_to_tensor=True)
    _Q_vec = embedding.tolist()
    
    query = {
        'size': 5,
        'query': {
            "knn": {
            "Q_vec": {
                "vector": _Q_vec ,
                "k": 2
                }
            }
        }
    }

    response = client.search(
        body = query,
        index = index_name
    )
    print('\nSearch results: %s' %str(search_text))

    return_data_sturct = {}
    return_data = {}
    
    time=1 
    for i in response['hits']['hits']:
        print(i['_source']['Q_text'],i['_source']['Ans'],i['_score'],i['_id'])
        # return {'ANS':i['_source']['Ans']}
        # return_data.update('Q_text':i['_source']['Q_text'])
        # return { 'answer':response}
        return_data_sturct[time] = {'Q':i['_source']['Q_text'],'Score':i['_score'],'Ans':i['_source']['Ans']}  # {'Q_text':i['_source']['Q_text'],'Ans':i['_source']['Ans'],'Score':i['_score']}
        return_data[time] = i['_source']['Q_text']+"\n"+ i['_source']['Ans']+ " "
        time = time + 1
    # print(return_data)
    format_return_data = ""
    for i in return_data:
        format_return_data = format_return_data  + "%s. "%i + return_data[i] + "\n"
    # print(type(return_data))  dict2json
    
    ###########################
    ###########################  MESSAGE SEND BLOCK 
    
    url_jzmh_message_send = "https://ex-api.botorange.com/message/send"
    jzmh_message = json.dumps(return_data)
    
    send_messageId = "6214b19ea66c67d78d0f133d"
    print(item.data.messageId)
    jzmh_data = {
        "chatId":  item.data.chatId, #"6214b19ea66c67d78d0f133d",
        "token": "6214b16a39011db76498866b",
        "messageType": 0 , # MessageType, check below
        "payload": {
            "text": format_return_data ,# str(return_data).replace('{',"").replace('}',"") ,
            "mention": [] # mention list, you can only set it when you send text message to room,
        },
        "externalRequestId": "",
    }
    
    # newjson=json.dumps(jzmh_message,ensure_ascii=False) 
    
    jzmh_headers = {'Content-Type': 'application/json'}
    
    res = requests.post(url=url_jzmh_message_send, headers=jzmh_headers, data=json.dumps(jzmh_data))

    ############################
    ###########################
    
    # return  json.dumps(return_data) 

