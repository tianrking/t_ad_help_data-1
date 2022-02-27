
"""
curl -k https://admin:admin@localhost:9200/qa_index_768?pretty
"""

import os
from opensearchpy import OpenSearch


index_name = os.environ.get('index', 'qa_index_768')
host = os.environ.get('host', 'localhost')
port = int(os.environ.get('port', 9200))
auth = (
    os.environ.get('user', 'admin'),
    os.environ.get('pass', 'admin')
)

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
