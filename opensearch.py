from opensearchpy import OpenSearch

host = 'localhost'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.
ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

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
    ca_certs = ca_certs_path
)

# Create an index with non-default settings.
index_name = 'abc_test_index'
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

# Add a document to the index.
# document = {
#   'Q_text': 'A BC',
#   'Q_vec': '123',
#   'Answer': 'abc'
# }
# id = '1'

# response = client.index(
#     index = index_name,
#     body = document,
#     id = id,
#     refresh = True
# )

# print('\nAdding document:')
# print(response)

# Search for the document.
q = 'BC'
query = {
  'size': 5,
  'query': {
    'multi_match': {
      'query': q,
      # 'fields': ['title^2', 'director']  # 'director'
      'fields': ['Q_text']
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

# # Delete the index.
# response = client.indices.delete(
#     index = index_name
# )

# print('\nDeleting index:')
# print(response)

# from sentence_transformers import SentenceTransformer, util
# model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# # Two lists of sentences
# sentences1 = ['The cat sits outside',
#              'A man is playing guitar',
#              'The new movie is awesome']

# sentences2 = ['The dog plays in the garden',
#               'A woman watches TV',
#               'The new movie is so great']

# #Compute embedding for both lists
# embeddings1 = model.encode(sentences1, convert_to_tensor=True)
# embeddings2 = model.encode(sentences2, convert_to_tensor=True)

# #Compute cosine-similarits
# cosine_scores = util.cos_sim(embeddings1, embeddings2)

# print(cosine_scores)