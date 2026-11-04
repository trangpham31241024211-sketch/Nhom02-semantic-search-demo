
import pandas as pd
from pathlib import Path

# Đường dẫn đến dữ liệu sản phẩm
DATA_DIR = Path(__file__).parent / "data"

# Đọc dữ liệu sản phẩm
df = pd.read_csv(DATA_DIR / "products_cleaned.csv")


def keyword_search(query, limit=5):
    """
    Tìm kiếm sản phẩm dựa trên từ khóa
    trong tên và mô tả sản phẩm.
    """

    query = query.strip().lower()

    # Kiểm tra truy vấn rỗng
    if not query:
        return []

    # Tìm từ khóa trong tên hoặc mô tả
    mask = (
        df["product_name"].str.lower().str.contains(
            query, na=False, regex=False
        )
        |
        df["description"].str.lower().str.contains(
            query, na=False, regex=False
        )
    )

    # Lấy các sản phẩm phù hợp
    results = df[mask].head(limit)

    return results.to_dict(orient="records")
