# Quick Start Guide

## Option 1: Use Mock Data (Fastest - Recommended for Testing)

```bash
# Install dependencies
pip install -r requirements.txt

# Generate mock data and setup
python setup.py --scraper mock

# Start API
uvicorn api.main:app --reload

# In another terminal, start UI
streamlit run frontend/app.py
```

## Option 2: Scrape Real SHL Website (Basic)

```bash
# Install dependencies
pip install -r requirements.txt

# Run basic scraper
python setup.py --scraper basic

# Start API
uvicorn api.main:app --reload

# In another terminal, start UI
streamlit run frontend/app.py
```

## Option 3: Scrape with Selenium (Most Complete)

```bash
# Install dependencies
pip install -r requirements.txt

# Install Chrome and ChromeDriver
# Windows: Download from https://chromedriver.chromium.org/
# Or use: choco install chromedriver

# Run Selenium scraper
python setup.py --scraper selenium

# Start API
uvicorn api.main:app --reload

# In another terminal, start UI
streamlit run frontend/app.py
```

## Manual Step-by-Step

If you want to run each step manually:

```bash
# 1. Create directories
mkdir data\raw data\processed vector_db dataset outputs

# 2. Choose ONE scraping method:

# Option A: Mock data (fastest)
python scraper/generate_mock_data.py

# Option B: Basic scraper
python scraper/shl_scraper.py

# Option C: Selenium scraper
python scraper/shl_scraper_selenium.py

# 3. Process data
python scraper/data_processor.py

# 4. Build FAISS index
python embeddings/build_embeddings.py

# 5. Start API
uvicorn api.main:app --reload

# 6. Start UI (in another terminal)
streamlit run frontend/app.py
```

## Testing the API

Once the API is running, test it:

```bash
# Health check
curl http://localhost:8000/health

# Get recommendations
curl -X POST http://localhost:8000/recommend ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"Python developer with SQL skills\", \"k\": 10}"
```

## Generate Predictions for Submission

```bash
# Create test dataset (if you have one)
# Place your test.csv in dataset/ folder

# Generate predictions
python evaluation/generate_predictions.py dataset/test.csv outputs/predictions.csv

# Evaluate (if you have ground truth)
python evaluation/evaluate_recall.py outputs/predictions.csv dataset/ground_truth.csv
```

## Troubleshooting

### Scraper returns < 377 assessments

The SHL website might use JavaScript rendering. Try:
1. Use mock data: `python setup.py --scraper mock`
2. Use Selenium: `python setup.py --scraper selenium`
3. Manually add more assessments to `data/raw/shl_catalog_raw.csv`

### FAISS index error

Make sure you have processed data:
```bash
python scraper/data_processor.py
python embeddings/build_embeddings.py
```

### API won't start

Check that all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Streamlit connection error

Make sure the API is running first:
```bash
uvicorn api.main:app --reload
```

Then in another terminal:
```bash
streamlit run frontend/app.py
```

## Project Structure

```
shl-assessment-recommender/
├── data/
│   ├── raw/                    # Raw scraped data
│   └── processed/              # Cleaned data
├── scraper/
│   ├── shl_scraper.py         # Basic scraper
│   ├── shl_scraper_selenium.py # Selenium scraper
│   ├── generate_mock_data.py  # Mock data generator
│   └── data_processor.py      # Data cleaning
├── embeddings/
│   ├── embedder.py            # Embedding model
│   └── build_embeddings.py    # Build FAISS index
├── vector_db/
│   └── index.faiss            # FAISS vector database
├── recommender/
│   └── recommend.py           # Recommendation engine
├── api/
│   └── main.py                # FastAPI backend
├── frontend/
│   └── app.py                 # Streamlit UI
├── evaluation/
│   ├── evaluate_recall.py     # Evaluation metrics
│   └── generate_predictions.py # Generate predictions
└── outputs/
    └── predictions.csv        # Submission file
```
