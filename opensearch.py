from opensearchpy import OpenSearch

host = 'localhost'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.
# ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

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



index_name = 'python-test-index3-knn'
index_body = {
  "settings": {
    "index": {
      "knn": True,
      "knn.algo_param.ef_search": 100
    }
  },
  "mappings": {
    "properties": {
        "my_vector1": {
          "type": "knn_vector",
          "dimension": 2,
          "method": {
            "name": "hnsw",
            "space_type": "l2",
            "engine": "nmslib",
            "parameters": {
              "ef_construction": 128,
              "m": 24
            }
          }
        }
    }
  }
}

# response = client.indices.create(index_name, body=index_body)
# print('\nCreating index:')
# print(response)

# document = {
#   'text': 'abc',
#   'my_vector1': [1, 2],
# }
# id = '1'

# response = client.index(
#     index = index_name,
#     body = document,
#     id = id,
#     refresh = True
# )
# print(response)


query = {
  'size': 5,
  'query': {
    "knn": {
      "my_vector1": {
        "vector": [2, 3],
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