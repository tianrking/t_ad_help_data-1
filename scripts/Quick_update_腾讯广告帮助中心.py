import pandas as pd
import requests
from opensearchpy import OpenSearch


from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

df = pd.read_csv("/home/tianrking/t_ad_help_data/data/tx_ah_help_center_with_url_warning.csv",header=None, names=['0','Q_text','A','Ans','update'])
df = df[[ "Q_text", "Ans"]]
QA_api_server = "http://127.0.0.1:1333/v1/QA/add"

# print(df.head(1))
# exit()

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


for i in range(df.shape[0]):
    
    Ans = df.loc[i, 'Ans']
    Q_text = df.loc[i, 'Q_text']
    Ans = df.loc[i,"Ans"]
    id  = "93"+str(i)  # 腾讯广告帮助中心 93
    print(Q_text,Ans)
    
    embedding = model.encode(Q_text, convert_to_tensor=True)
    Q_vec = embedding.tolist()
    document = {
        'Q_text': Q_text,
        'Q_vec': Q_vec,
        'Ans': Ans,
    }

    response = client.index(
        index=index_name,
        body=document,
        id=id,
        refresh=True
    )

    print('\nAdding id %s ' % str(id))
    print(response)
# print(df.shape)