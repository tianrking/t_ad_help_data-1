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
index_name = 'qa_index_18522'
# index_body = {
#     'settings':
#     {
#         'index': {
#             "knn": True,
#             "knn.algo_param.ef_search": 100
#         }
#     },
#     "mappings": {
#         "properties": {
#             "QA": {
#                 "type": "knn_vector",
#                 "dimension": 2,
#                 "method": {
#                     "name": "hnsw",
#                     "space_type": "l2",
#                     "engine": "nmslib",
#                     "parameters": {
#                         "ef_construction": 128,
#                         "m": 24
#                     }
#                 }
#             }
#         }
#     }
# }
# response = client.indices.create(index_name, body=index_body)
# print('\nCreating index:')
# print(response)
# exit()
# # Add a document to the index.

document = {
  'que':'abc',
  'QA':[1,2],
  'ans':'ABC',
}
# document = {
#   'text': 'abc',
#   'QA': [1, 2],
# }
id = '2'

response = client.index(
    index = index_name,
    body = document,
    id = id,
    refresh = True
)

# print('\nAdding document:')
print(response)

# # Search for the document.
q = 'miller'
query = {
  'size': 5,
  'query':  {
    "knn": {
      "QA": {
        "vector": [2,3],
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

# # Delete the document.
# response = client.delete(
#     index = index_name,
#     id = id
# )

# print('\nDeleting document:')
# print(response)

# Delete the index.
# response = client.indices.delete(
#     index = index_name
# )

# print('\nDeleting index:')
# print(response)