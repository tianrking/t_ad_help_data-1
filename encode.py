from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

def encode(x):
    return model.encode(x, convert_to_tensor=True).tolist()
