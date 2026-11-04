
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

# Đọc dữ liệu đã làm sạch
df = pd.read_csv(DATA_DIR / "products_cleaned.csv")

# Kết hợp tên và mô tả sản phẩm
df["search_text"] = (
    "Product: " + df["product_name"].fillna("") +
    ". Description: " + df["description"].fillna("")
)

# Lưu dữ liệu đã chuẩn bị
output_path = DATA_DIR / "products_ready.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("Da chuan bi du lieu cho mo hinh!")
print("So san pham:", len(df))
print("\nVi du noi dung dau vao:")
print(df.loc[0, "search_text"])
print("\nFile da luu:", output_path)
