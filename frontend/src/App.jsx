
import { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    if (!query.trim()) {
      setError("Vui lòng nhập nội dung tìm kiếm.");
      return;
    }

    setLoading(true);
    setError("");
    setProducts([]);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/search?query=${encodeURIComponent(query)}&limit=5`
      );

      if (!response.ok) {
        throw new Error("Không thể kết nối đến máy chủ.");
      }

      const data = await response.json();
      setProducts(data.results);
    } catch (err) {
      setError("Có lỗi khi tìm kiếm. Vui lòng kiểm tra Backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>Semantic Product Search</h1>
        <p>Tìm kiếm sản phẩm thông minh bằng ngữ nghĩa</p>
      </header>

      <main>
        <div className="search-box">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            placeholder="Nhập nhu cầu tìm kiếm sản phẩm..."
          />
          <button onClick={handleSearch} disabled={loading}>
            {loading ? "Đang tìm..." : "Tìm kiếm"}
          </button>
        </div>

        {error && <p className="error">{error}</p>}

        {products.length > 0 && (
          <section className="results">
            <h2>Kết quả tìm kiếm</h2>

            {products.map((product) => (
              <article className="product-card" key={product.product_id}>
                <h3>{product.product_name}</h3>
                <p><strong>Danh mục:</strong> {product.category}</p>
                <p><strong>Giá:</strong> ${product.price}</p>
                <p>{product.description}</p>
                <p className="score">
                  Độ tương đồng: {(product.score * 100).toFixed(2)}%
                </p>
              </article>
            ))}
          </section>
        )}

        {!loading && !error && products.length === 0 && (
          <p className="empty">Nhập từ khóa để bắt đầu tìm kiếm sản phẩm.</p>
        )}
      </main>
    </div>
  );
}

export default App;
