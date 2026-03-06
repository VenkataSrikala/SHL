import pandas as pd
import re

def clean_text(text):
    """Clean and normalize text"""
    if pd.isna(text):
        return ""
    text = str(text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def process_catalog():
    """Process and clean scraped data"""
    print("Processing catalog data...")
    
    df = pd.read_csv("data/raw/shl_catalog_raw.csv")
    
    # Clean text fields
    df['name'] = df['name'].apply(clean_text)
    df['description'] = df['description'].apply(clean_text)
    
    # Create combined text for embeddings
    df['combined_text'] = df['name'] + " " + df['description'] + " " + df['test_type']
    
    # Fill missing values
    df['duration'] = df['duration'].fillna(0)
    df['remote_support'] = df['remote_support'].fillna("Yes")
    df['adaptive_support'] = df['adaptive_support'].fillna("No")
    
    # Save processed data
    df.to_csv("data/processed/shl_catalog_clean.csv", index=False)
    print(f"Processed {len(df)} assessments")
    print("Saved to data/processed/shl_catalog_clean.csv")
    
    return df

if __name__ == "__main__":
    process_catalog()
