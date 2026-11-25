import { useState, useEffect, useRef } from "react";
import { pipeline, env } from "@xenova/transformers";
import "./App.css";

// Tối ưu cấu hình transformers.js cho trình duyệt
env.allowLocalModels = false;

function cosineSimilarity(vecA, vecB) {
  let dot = 0;
  let normA = 0;
  let normB = 0;
  for (let i = 0; i < vecA.length; i++) {
    dot += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }
  if (normA === 0 || normB === 0) return 0;
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

function App() {
  const [query, setQuery] = useState("");
  const [allProducts, setAllProducts] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [error, setError] = useState("");
  const [searchTime, setSearchTime] = useState(null);

  const extractorRef = useRef(null);

  // Tải danh sách sản phẩm khi mở trang
  useEffect(() => {
    async function loadProducts() {
      try {
        const response = await fetch("./products.json");
        if (!response.ok) {
          throw new Error("Không thể tải danh sách sản phẩm.");
        }
        const data = await response.json();
        setAllProducts(data);
      } catch (err) {
        console.error(err);
        setError("Không thể tải dữ liệu sản phẩm. Vui lòng thử lại!");
      }
    }
    loadProducts();
  }, []);

  const handleSearch = async () => {
    const text = query.trim();
    if (!text) {
      setError("Vui lòng nhập nội dung tìm kiếm.");
      return;
    }

    if (allProducts.length === 0) {
      setError("Dữ liệu sản phẩm đang được tải, vui lòng đợi giây lát...");
      return;
    }

    setLoading(true);
    setError("");
    setResults([]);
    setSearchTime(null);

    const startTime = performance.now();

    try {
      // 1. Tải mô hình nếu chưa tải
      if (!extractorRef.current) {
        setStatusMessage("Đang tải mô hình AI vào trình duyệt (lần đầu sẽ mất ít giây)...");
        extractorRef.current = await pipeline(
          "feature-extraction",
          "Xenova/paraphrase-multilingual-MiniLM-L12-v2",
          {
            quantized: true,
            progress_callback: (progress) => {
              if (progress.status === "progress") {
                setStatusMessage(`Đang tải mô hình: ${Math.round(progress.progress)}%`);
              }
            },
          }
        );
      }

      setStatusMessage("Đang tính toán vector ngữ nghĩa...");

      // 2. Chuyển câu hỏi thành vector embedding
      const output = await extractorRef.current(text, {
        pooling: "mean",
        normalize: true,
      });
      const queryVector = Array.from(output.data);

      setStatusMessage("Đang xếp hạng kết quả tương đồng...");

      // 3. Tính độ tương đồng Cosine với từng sản phẩm
      const scored = allProducts.map((p) => {
        const score = cosineSimilarity(queryVector, p.embedding);
        return {
          ...p,
          score: score,
        };
      });

      // 4. Sắp xếp điểm giảm dần và lấy top 5
      scored.sort((a, b) => b.score - a.score);
      const topResults = scored.slice(0, 5);

      const endTime = performance.now();
      setSearchTime(Math.round(endTime - startTime));
      setResults(topResults);
      setStatusMessage("");
    } catch (err) {
      console.error(err);
      setError("Có lỗi khi phân tích ngữ nghĩa: " + (err.message || err));
    } finally {
      setLoading(false);
      setStatusMessage("");
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
            placeholder="Nhập nhu cầu tìm kiếm"
          />
          <button onClick={handleSearch} disabled={loading}>
            {loading ? "Đang tìm..." : "Tìm kiếm"}
          </button>
        </div>

        {statusMessage && (
          <p style={{ color: "#0066cc", fontStyle: "italic", textAlign: "center", marginTop: "12px" }}>
            ⏳ {statusMessage}
          </p>
        )}

        {error && <p className="error">{error}</p>}

        {searchTime !== null && results.length > 0 && (
          <p style={{ fontSize: "0.85rem", color: "#666", textAlign: "center", marginTop: "12px" }}>
            ⚡ Tìm thấy {results.length} sản phẩm phù hợp trong {searchTime}ms
          </p>
        )}

        {results.length > 0 && (
          <section className="results">
            <h2>Kết quả tìm kiếm</h2>

            {results.map((product) => (
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

        {!loading && !error && results.length === 0 && (
          <p className="empty">Nhập từ khóa để bắt đầu tìm kiếm sản phẩm.</p>
        )}
      </main>
    </div>
  );
}

export default App;
