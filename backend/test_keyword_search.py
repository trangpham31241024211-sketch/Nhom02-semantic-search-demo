from backend.keyword_search import keyword_search

query = "VTech karaoke toy for children"

results = keyword_search(query, limit=5)

print("Từ khóa tìm kiếm:", query)
print("Số sản phẩm tìm thấy:", len(results))

for product in results:
    print("----------------------------")
    print("Mã sản phẩm:", product["product_id"])
    print("Tên sản phẩm:", product["product_name"])
    print("Danh mục:", product["category"])
    print("Giá:", product["price"])
