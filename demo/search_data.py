from sentence_transformers import SentenceTransformer, util
from opensearchpy import OpenSearch
import json

host = 'localhost'
port = 9200
auth = ('admin', 'admin')  # For testing only. Don't store credentials in code.
# ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

# Optional client certificates if you don't want to use HTTP basic authentication.
# client_cert_path = '/full/path/to/client.pem'
# client_key_path = '/full/path/to/client-key.pem'

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_compress=True,  # enables gzip compression for request bodies
    http_auth=auth,
    # client_cert = client_cert_path,
    # client_key = client_key_path,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
    # ca_certs = ca_certs_path
)

# Create an index with non-default settings.
index_name = 'qa_index_768'

_Q = "数据"
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
embedding = model.encode(_Q, convert_to_tensor=True)
Q_vec = embedding.tolist()

query = {
    'size': 8,
    'query': {
        "knn": {
            "Q_vec": {
                "vector": Q_vec,
                "k": 2
            }
        }
    }
}

response = client.search(
    body=query,
    index=index_name
)

return_data_sturct = {}
return_data = {}

time = 1

return_message_str = ""

_score_=0.3

for i in response['hits']['hits']:
    # print(i['_source']['Q_text'], i['_source']['Ans'], i['_score'], i['_id'])
    if i['_score']>_score_:
        return_message_str = return_message_str + i['_source']['Q_text'] + "\n" + \
            i['_source']['Ans'] + "\n"
        
    # return {'ANS':i['_source']['Ans']}
    # return_data.update('Q_text':i['_source']['Q_text'])
    # return { 'answer':response}
    # {'Q_text':i['_source']['Q_text'],'Ans':i['_source']['Ans'],'Score':i['_score']}
    
    
    
    # return_data_sturct[time] = {
    #     'Q': i['_source']['Q_text'], 'Score': i['_score'], 'Ans': i['_source']['Ans']}
    # return_data[time] = i['_source']['Q_text'] + \
    #     ' ' + i['_source']['Ans'] + ' '
    # time = time + 1

print('\nSearch results for %s with %s:' % (_Q,str(_score_)))
if len(return_message_str):
    print(return_message_str)
else:
    print("请咨询人工客服")
# print(return_data)

# print(response)
