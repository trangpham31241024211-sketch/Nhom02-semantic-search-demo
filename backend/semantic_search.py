
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

from backend.embedding_model import generate_embedding

# Đọc dữ liệu sản phẩm
DATA_DIR = Path(__file__).parent / "data"

df = pd.read_csv(DATA_DIR / "products_ready.csv")

# Đọc vector Embedding đã tạo
product_embeddings = np.load(
    DATA_DIR / "product_embeddings.npy"
)


def semantic_search(query, limit=5):
    """
    Tìm kiếm sản phẩm dựa trên độ tương đồng ngữ nghĩa.
    """

    query = query.strip()

    if not query:
        return []

    # Chuyển truy vấn thành vector Embedding
    query_embedding = generate_embedding(query)

    # Tính độ tương đồng Cosine
    similarities = cosine_similarity(
        query_embedding.reshape(1, -1),
        product_embeddings
    )[0]

    # Lấy vị trí sản phẩm theo thứ tự điểm tương đồng giảm dần
    ranked_indices = np.argsort(similarities)[::-1][:limit]

    results = []

    for index in ranked_indices:
        product = df.iloc[index].to_dict()

        product["score"] = float(similarities[index])
        product["score_type"] = "cosine_similarity"

        results.append(product)

    return results
