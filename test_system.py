"""Quick test script to verify the system is working"""
import pandas as pd
import os

print("=== System Check ===\n")

# Check data files
print("1. Checking data files...")
if os.path.exists("data/raw/shl_catalog_raw.csv"):
    df_raw = pd.read_csv("data/raw/shl_catalog_raw.csv")
    print(f"   ✓ Raw data: {len(df_raw)} assessments")
else:
    print("   ✗ Raw data not found")

if os.path.exists("data/processed/shl_catalog_clean.csv"):
    df = pd.read_csv("data/processed/shl_catalog_clean.csv")
    print(f"   ✓ Processed data: {len(df)} assessments")
    print(f"\n   Test type breakdown:")
    print(df['test_type'].value_counts().to_string().replace('\n', '\n   '))
else:
    print("   ✗ Processed data not found")

# Check FAISS index
print("\n2. Checking FAISS index...")
if os.path.exists("vector_db/index.faiss"):
    import faiss
    index = faiss.read_index("vector_db/index.faiss")
    print(f"   ✓ FAISS index: {index.ntotal} vectors")
else:
    print("   ✗ FAISS index not found")

# Test recommender
print("\n3. Testing recommender...")
try:
    from recommender.recommend import recommend_assessments
    
    test_query = "Python developer with SQL skills"
    results = recommend_assessments(test_query, k=5)
    
    print(f"   ✓ Recommender working")
    print(f"\n   Query: '{test_query}'")
    print(f"   Top 5 recommendations:")
    for i, r in enumerate(results, 1):
        print(f"   {i}. {r['name']} ({r['test_type']})")
except Exception as e:
    print(f"   ✗ Recommender error: {e}")

print("\n=== System Ready ===")
print("\nStart the API with:")
print("  uvicorn api.main:app --reload")
print("\nStart the UI with:")
print("  streamlit run frontend/app.py")
