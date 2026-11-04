from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

print("Đang tải mô hình Embedding...")

model = SentenceTransformer(
    MODEL_NAME,
    local_files_only=True
)

print("Mô hình Embedding đã sẵn sàng!")

def get_model():
    return model

def generate_embedding(text):
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding