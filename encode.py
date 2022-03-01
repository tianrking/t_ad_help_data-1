"""
encode sentence to vector with multi-language model (include Chinese)
"""

from sentence_transformers import SentenceTransformer

# model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
model = None

def encode(x):
    global model
    if model is None:
        model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    return model.encode(x, convert_to_tensor=True).tolist()


if __name__ == '__main__':
    # for test and download model in Dockerfile
    encode('test')
