
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
file_path = DATA_DIR / "products_cleaned.csv"

df = pd.read_csv(file_path)

print("1. Kiem tra du lieu trung lap")
print("Ma san pham trung:", df["product_id"].duplicated().sum())
print("Ten san pham trung:", df["product_name"].duplicated().sum())

print("\n2. Kiem tra du lieu rong")
print(df.isnull().sum())

print("\n3. Thong ke do dai mo ta")
print(df["description"].str.len().describe())

print("\n4. Kiem tra gia san pham")
print(df["price"].describe())

print("\n5. Kiem tra so luong danh muc")
print("So danh muc:", df["category"].nunique())

print("\nDa kiem tra xong!")
