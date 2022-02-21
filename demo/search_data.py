from opensearchpy import OpenSearch

host = 'localhost'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.
# ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

# Optional client certificates if you don't want to use HTTP basic authentication.
# client_cert_path = '/full/path/to/client.pem'
# client_key_path = '/full/path/to/client-key.pem'

# Create the client with SSL/TLS enabled, but hostname verification disabled.
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

# Create an index with non-default settings.
index_name = 'qa_index_384'

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
embedding = model.encode("朋友圈信息流", convert_to_tensor=True)
Q_vec = embedding.tolist()

query = {
  'size': 5,
  'query': {
    "knn": {
      "Q_vec": {
        "vector": Q_vec ,
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
print(response)
