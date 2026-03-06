"""Setup script to initialize project directories and run pipeline"""
import os
import subprocess
import sys

def create_directories():
    """Create necessary directories"""
    dirs = [
        "data/raw",
        "data/processed",
        "vector_db",
        "dataset",
        "outputs"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ Created {dir_path}")

def run_pipeline(scraper_type="basic"):
    """Run the complete pipeline"""
    print("\n=== SHL Assessment Recommender Setup ===\n")
    
    # Create directories
    print("1. Creating directories...")
    create_directories()
    
    # Scrape catalog
    print("\n2. Scraping SHL catalog...")
    print(f"   Using scraper: {scraper_type}")
    
    if scraper_type == "selenium":
        print("   Note: Selenium scraper requires Chrome/ChromeDriver installed")
        result = subprocess.run([sys.executable, "scraper/shl_scraper_selenium.py"])
    elif scraper_type == "mock":
        print("   Generating mock data for testing...")
        result = subprocess.run([sys.executable, "scraper/generate_mock_data.py"])
    else:
        result = subprocess.run([sys.executable, "scraper/shl_scraper.py"])
    
    # Check if scraping was successful
    if not os.path.exists("data/raw/shl_catalog_raw.csv"):
        print("\n⚠ Scraping failed or no data found!")
        print("   Falling back to mock data generation...")
        subprocess.run([sys.executable, "scraper/generate_mock_data.py"])
    
    # Process data
    print("\n3. Processing data...")
    subprocess.run([sys.executable, "scraper/data_processor.py"])
    
    # Build embeddings
    print("\n4. Building FAISS index...")
    subprocess.run([sys.executable, "embeddings/build_embeddings.py"])
    
    print("\n=== Setup Complete ===")
    print("\nNext steps:")
    print("1. Start API: uvicorn api.main:app --reload")
    print("2. Launch UI: streamlit run frontend/app.py")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup SHL Assessment Recommender")
    parser.add_argument(
        "--scraper",
        choices=["basic", "selenium", "mock"],
        default="basic",
        help="Scraper type: basic (requests), selenium (JavaScript), or mock (test data)"
    )
    
    args = parser.parse_args()
    run_pipeline(args.scraper)
