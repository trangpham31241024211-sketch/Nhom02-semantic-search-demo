
import pandas as pd
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

# 1. Xác định đường dẫn
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# 2. Đọc dữ liệu sản phẩm
df = pd.read_csv(DATA_DIR / "products_ready.csv")

# 3. Khai báo mô hình
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

print("Dang tai mo hinh...")
model = SentenceTransformer(MODEL_NAME)

# 4. Lấy nội dung văn bản của sản phẩm
texts = df["search_text"].fillna("").tolist()

# 5. Sinh embedding
print("Dang tao embedding...")
embeddings = model.encode(
    texts,
    show_progress_bar=True,
    convert_to_numpy=True
)

# 6. Lưu embedding
output_path = DATA_DIR / "product_embeddings.npy"
np.save(output_path, embeddings)

# 7. Kiểm tra kết quả
print("\nDa tao embedding thanh cong!")
print("So san pham:", len(df))
print("Kich thuoc embedding:", embeddings.shape)
print("File da luu:", output_path)
