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
