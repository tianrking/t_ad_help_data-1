import pandas as pd

import pandas as pd
import json 
from opensearchpy import OpenSearch

from fastapi import Cookie, FastAPI
from typing import Optional
from fastapi import FastAPI
from fastapi import Request
import requests
from typing import List, Optional
import sys
import uvicorn
from fastapi import FastAPI,UploadFile,File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Header
import os
import requests
from pydantic import BaseModel


from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

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

# 创建索引
# index_name = 'python-test-index'
# index_body = {
#   'settings': {
#     'index': {
#       'number_of_shards': 4
#     }
#   }
# }

# response = client.indices.create(index_name, body=index_body)
# print('\nCreating index:')
# print(response)



df = pd.read_csv('/home/tianrking/t_ad_help_data/ad_weixin_qq_com_guide_titile_clean.csv')
print(df.head())
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

template_Q = ['我']
template_Q_vec = ''
for i in template_Q:
    embedding = model.encode(i, convert_to_tensor=True)
    template_Q_vec.append(embedding.tolist())
    
@app.post("/v1/QA")
async def create_item(item: Item_sts):
    embedding = model.encode(item.text, convert_to_tensor=True)
    _Q_vec = embedding.tolist()
    for _template_Q in template_Q_vec:
        _template_Q_vec = 
    print(item.text)
    # print(item.method)
    return embedding.tolist()

# curl -X POST -k "127.0.0.1:1333/api/sts/" -H 'Content-Type: application/json' -d' { "text": "ok" } '