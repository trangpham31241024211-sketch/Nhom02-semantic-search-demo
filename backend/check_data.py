
import pandas as pd
from pathlib import Path

# Đường dẫn đến dataset gốc
DATA_DIR = Path(__file__).parent / "data"
file_path = DATA_DIR / "amazon_product_data_cleaned"

# Đọc dữ liệu
df = pd.read_csv(file_path)

# Chọn các cột cần thiết
products = df[
    [
        "Uniq Id",
        "Product Name",
        "Category",
        "Selling Price",
        "About Product"
    ]
].copy()

# Đổi tên cột theo cấu trúc dự án
products.columns = [
    "product_id",
    "product_name",
    "category",
    "price",
    "description"
]

# Xử lý dữ liệu thiếu
products = products.dropna(
    subset=["product_id", "product_name", "description", "price"]
)

products["category"] = products["category"].fillna("Chưa phân loại")

# Xóa khoảng trắng thừa
for col in ["product_id", "product_name", "category", "description"]:
    products[col] = products[col].astype(str).str.strip()

# Chuyển giá về dạng số
products["price"] = (
    products["price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

products["price"] = pd.to_numeric(products["price"], errors="coerce")

# Loại bỏ các dòng có giá không hợp lệ
products = products.dropna(subset=["price"])

# Xóa sản phẩm trùng mã
products = products.drop_duplicates(subset=["product_id"])

# Chọn tối đa 200 sản phẩm
products = products.sample(
    n=min(200, len(products)),
    random_state=42
)

# Xuất thành file mới, không ghi đè dataset gốc
output_path = DATA_DIR / "products_cleaned.csv"
products.to_csv(output_path, index=False, encoding="utf-8-sig")

print("Đã xử lý dữ liệu thành công!")
print("Số sản phẩm:", len(products))
print("Các cột:", products.columns.tolist())
print("File kết quả:", output_path)
print("\n5 sản phẩm đầu tiên:")
print(products.head().to_string(index=False))
