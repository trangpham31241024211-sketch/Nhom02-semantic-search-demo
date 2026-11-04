
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

print("Dang tai mo hinh...")

model = SentenceTransformer(MODEL_NAME)

texts = [
    "Giay di bo dem mem",
    "Giay the thao ho tro di bo em chan",
    "May pha ca phe tai nha",
]

embeddings = model.encode(texts)

print("Kich thuoc embedding:")
print(embeddings.shape)

print("Da tai mo hinh va tao embedding thanh cong!")
