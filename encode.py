"""
encode sentence to vector with multi-language model (include Chinese)
"""

import os
from sentence_transformers import SentenceTransformer


model = None

def load_model():
    global model
    if model is not None:
        return model
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    return model


def encode(x):
    model = load_model()
    return model.encode(x, convert_to_tensor=True).tolist()


if os.environ.get('LOAD_MODEL_STARTUP'):
    load_model()


if __name__ == '__main__':
    # for test and download model in Dockerfile
    encode('test')
