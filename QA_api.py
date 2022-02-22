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

id=1

df = pd.read_csv('/home/tianrking/t_ad_help_data/ad_weixin_qq_com_guide_titile_clean.csv')
print(df.head())
index_name = 'qa_index_384'
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
    print('\nSearch results:')
    # print(response)
    
    # list1= []
    # for i in json_data:
    #     i.pop("explanation")
    #     i.pop("more")
    #     list1.append(i)
    # print(response)
    for i in response['hits']['hits']:
        print(i['_source']['Ans'],i['_score'],i['_id'])
    # for i in response:
    #     print(i)
    #     # print(i['hits']['hits'][0]['_source']['Ans'])
    #     # break
        
    # return { 'answer':response}
