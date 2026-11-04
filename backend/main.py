
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from backend.semantic_search import semantic_search

app = FastAPI(
    title="Semantic Search API",
    description="API tìm kiếm sản phẩm bằng ngữ nghĩa",
    version="1.0.0"
)

# Cho phép frontend React kết nối với backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Semantic Search API đang hoạt động!"
    }

@app.get("/api/search")
def search_products(
    query: str = Query(..., min_length=1),
    limit: int = Query(5, ge=1, le=20)
):
    results = semantic_search(query, limit)

    return {
        "query": query,
        "total": len(results),
        "results": results
    }
