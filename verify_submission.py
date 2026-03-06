"""
Verification script to check if submission is ready
Run this before submitting to ensure everything is in place
"""

import os
import sys
import pandas as pd

def check_file(path, description):
    """Check if a file exists"""
    if os.path.exists(path):
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description}: {path} NOT FOUND")
        return False

def check_directory(path, description):
    """Check if a directory exists"""
    if os.path.isdir(path):
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description}: {path} NOT FOUND")
        return False

def main():
    print("="*60)
    print("SHL Assessment Recommender - Submission Verification")
    print("="*60)
    print()
    
    all_checks = []
    
    # 1. Check data files
    print("1. Checking Data Files...")
    all_checks.append(check_file("data/raw/shl_catalog_raw.csv", "Raw data"))
    all_checks.append(check_file("data/processed/shl_catalog_clean.csv", "Processed data"))
    
    if os.path.exists("data/processed/shl_catalog_clean.csv"):
        df = pd.read_csv("data/processed/shl_catalog_clean.csv")
        if len(df) >= 377:
            print(f"✅ Assessment count: {len(df)} (>= 377)")
            all_checks.append(True)
        else:
            print(f"❌ Assessment count: {len(df)} (< 377)")
            all_checks.append(False)
    print()
    
    # 2. Check FAISS index
    print("2. Checking FAISS Index...")
    all_checks.append(check_file("vector_db/index.faiss", "FAISS index"))
    print()
    
    # 3. Check core modules
    print("3. Checking Core Modules...")
    all_checks.append(check_file("scraper/shl_scraper.py", "Scraper"))
    all_checks.append(check_file("embeddings/embedder.py", "Embedder"))
    all_checks.append(check_file("embeddings/build_embeddings.py", "Build embeddings"))
    all_checks.append(check_file("recommender/recommend.py", "Recommender"))
    all_checks.append(check_file("api/main.py", "API"))
    all_checks.append(check_file("frontend/app.py", "Frontend"))
    print()
    
    # 4. Check evaluation
    print("4. Checking Evaluation...")
    all_checks.append(check_file("evaluation/evaluate_recall.py", "Evaluation script"))
    all_checks.append(check_file("evaluation/generate_predictions.py", "Prediction generator"))
    all_checks.append(check_file("dataset/test.csv", "Test dataset"))
    all_checks.append(check_file("outputs/predictions.csv", "Predictions output"))
    
    if os.path.exists("outputs/predictions.csv"):
        pred_df = pd.read_csv("outputs/predictions.csv")
        if len(pred_df) > 0:
            print(f"✅ Predictions generated: {len(pred_df)} rows")
            all_checks.append(True)
        else:
            print(f"❌ Predictions file is empty")
            all_checks.append(False)
    print()
    
    # 5. Check documentation
    print("5. Checking Documentation...")
    all_checks.append(check_file("README.md", "README"))
    all_checks.append(check_file("requirements.txt", "Requirements"))
    all_checks.append(check_file("setup.py", "Setup script"))
    print()
    
    # 6. Check deployment configs
    print("6. Checking Deployment Configs...")
    all_checks.append(check_file("render.yaml", "Render config"))
    all_checks.append(check_file(".streamlit/config.toml", "Streamlit config"))
    print()
    
    # 7. Test imports
    print("7. Testing Imports...")
    try:
        import fastapi
        print("✅ FastAPI installed")
        all_checks.append(True)
    except ImportError:
        print("❌ FastAPI not installed")
        all_checks.append(False)
    
    try:
        import streamlit
        print("✅ Streamlit installed")
        all_checks.append(True)
    except ImportError:
        print("❌ Streamlit not installed")
        all_checks.append(False)
    
    try:
        import faiss
        print("✅ FAISS installed")
        all_checks.append(True)
    except ImportError:
        print("❌ FAISS not installed")
        all_checks.append(False)
    
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ Sentence Transformers installed")
        all_checks.append(True)
    except ImportError:
        print("❌ Sentence Transformers not installed")
        all_checks.append(False)
    print()
    
    # 8. Test recommender
    print("8. Testing Recommender...")
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from recommender.recommend import recommend_assessments
        
        results = recommend_assessments("Python developer", k=5)
        if len(results) == 5:
            print(f"✅ Recommender working (returned {len(results)} results)")
            all_checks.append(True)
        else:
            print(f"❌ Recommender returned {len(results)} results (expected 5)")
            all_checks.append(False)
    except Exception as e:
        print(f"❌ Recommender error: {e}")
        all_checks.append(False)
    print()
    
    # Summary
    print("="*60)
    print("SUMMARY")
    print("="*60)
    passed = sum(all_checks)
    total = len(all_checks)
    percentage = (passed / total) * 100
    
    print(f"Checks passed: {passed}/{total} ({percentage:.1f}%)")
    print()
    
    if all(all_checks):
        print("🎉 ALL CHECKS PASSED! 🎉")
        print()
        print("Your submission is ready!")
        print()
        print("Next steps:")
        print("1. Deploy API to Render")
        print("2. Deploy UI to Streamlit Cloud")
        print("3. Write 2-page technical report")
        print("4. Submit all 5 items")
        print()
        return 0
    else:
        print("⚠️  SOME CHECKS FAILED")
        print()
        print("Please fix the issues above before submitting.")
        print()
        print("Quick fixes:")
        print("- Missing data: Run 'python setup.py --scraper mock'")
        print("- Missing packages: Run 'pip install -r requirements.txt'")
        print("- Missing predictions: Run 'python evaluation/generate_predictions.py dataset/test.csv outputs/predictions.csv'")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
