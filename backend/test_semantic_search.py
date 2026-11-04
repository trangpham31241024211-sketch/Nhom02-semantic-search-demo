
from backend.semantic_search import semantic_search

# Truy vấn kiểm thử
query = "VTech karaoke toy for children"

# Thực hiện tìm kiếm
results = semantic_search(query, limit=5)

print("Truy vấn:", query)
print("Số sản phẩm tìm thấy:", len(results))

for index, product in enumerate(results, start=1):
    print(f"\nTOP {index}")
    print("Tên sản phẩm:", product["product_name"])
    print("Điểm tương đồng:", round(product["score"], 4))
