
from backend.embedding_model import generate_embedding

# Văn bản dùng để kiểm tra
test_text = "A beautiful decorative lamp for the bedroom"

# Tạo vector Embedding
embedding = generate_embedding(test_text)

# Kiểm tra kết quả
print("Đã tạo Embedding thành công!")
print("Kích thước vector:", embedding.shape)
print("Một số giá trị đầu tiên:", embedding[:5])
