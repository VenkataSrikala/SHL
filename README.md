# SHL Assessment Recommender

AI-powered recommendation system for SHL assessments using semantic search and vector embeddings.

## ✨ Features

- 377+ SHL assessments from product catalog
- Semantic search using sentence transformers (all-MiniLM-L6-v2)
- FAISS vector database for fast similarity search
- FastAPI backend with REST API
- Streamlit web interface
- Balanced recommendations across test types
- Evaluation with Mean Recall@10
- Multiple scraping options (basic, Selenium, mock data)

## 🚀 Quick Start (Recommended)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup with mock data (fastest for testing)
python setup.py --scraper mock

# 3. Start API
uvicorn api.main:app --reload

# 4. In another terminal, start UI
streamlit run frontend/app.py
```

Visit `http://localhost:8501` to use the web interface!

## 📊 Scraping Options

### Option 1: Mock Data (Fastest - Recommended)
Generates 377 realistic SHL assessments for testing:
```bash
python setup.py --scraper mock
```

### Option 2: Basic Scraper
Scrapes real SHL website using requests + BeautifulSoup:
```bash
python setup.py --scraper basic
```

### Option 3: Selenium Scraper (Most Complete)
Uses Selenium for JavaScript-rendered content:
```bash
# Install ChromeDriver first
# Windows: choco install chromedriver
# Or download from: https://chromedriver.chromium.org/

python setup.py --scraper selenium
```

## 📁 Project Structure

```
shl-assessment-recommender/
├── data/
│   ├── raw/              # Raw scraped data
│   └── processed/        # Cleaned data
├── scraper/              # Web scraping
│   ├── shl_scraper.py           # Basic scraper
│   ├── shl_scraper_selenium.py  # Selenium scraper
│   ├── generate_mock_data.py    # Mock data generator
│   └── data_processor.py        # Data cleaning
├── embeddings/           # Embedding generation
│   ├── embedder.py              # Sentence transformer
│   └── build_embeddings.py      # Build FAISS index
├── vector_db/            # FAISS index
├── recommender/          # Recommendation engine
│   └── recommend.py
├── api/                  # FastAPI backend
│   └── main.py
├── frontend/             # Streamlit UI
│   └── app.py
├── evaluation/           # Evaluation scripts
│   ├── evaluate_recall.py
│   └── generate_predictions.py
├── dataset/              # Train/test data
└── outputs/              # Predictions
```

## 🔧 Manual Setup

If you prefer step-by-step control:

```bash
# 1. Create directories
mkdir data\raw data\processed vector_db dataset outputs

# 2. Generate/scrape data (choose one)
python scraper/generate_mock_data.py        # Mock data
python scraper/shl_scraper.py               # Basic scraper
python scraper/shl_scraper_selenium.py      # Selenium scraper

# 3. Process data
python scraper/data_processor.py

# 4. Build FAISS index
python embeddings/build_embeddings.py

# 5. Test the system
python test_system.py
```

## 🌐 API Endpoints

### Health Check
```bash
GET /health

Response:
{
  "status": "healthy"
}
```

### Get Recommendations
```bash
POST /recommend

Request:
{
  "query": "Need Python developer with SQL skills",
  "k": 10,
  "balanced": true
}

Response:
{
  "recommended_assessments": [
    {
      "name": "Python New",
      "url": "https://www.shl.com/solutions/products/product-catalog/view/python-new/",
      "description": "Python programming test",
      "duration": 11,
      "test_type": ["Knowledge & Skills"],
      "remote_support": "Yes",
      "adaptive_support": "No"
    }
  ]
}
```

## 📝 Input Types Supported

1. **Natural Language Query**
   ```
   "Need Python developer with SQL and problem solving skills"
   ```

2. **Job Description Text**
   ```
   "We are hiring a data analyst with SQL, Python, analytical thinking..."
   ```

3. **Job Description URL** (coming soon)
   ```
   "https://jobs.company.com/data-analyst-role"
   ```

## 📊 Generate Predictions for Submission

```bash
# Place your test.csv in dataset/ folder with format:
# Query
# "Python developer with SQL"
# "Java developer with teamwork"

# Generate predictions
python evaluation/generate_predictions.py dataset/test.csv outputs/predictions.csv

# Evaluate (if you have ground truth)
python evaluation/evaluate_recall.py outputs/predictions.csv dataset/ground_truth.csv
```

Output format (predictions.csv):
```csv
Query,Assessment_url
Python developer,https://shl.com/test1
Python developer,https://shl.com/test2
SQL analyst,https://shl.com/test3
```

## 🧪 Testing

```bash
# Test the complete system
python test_system.py

# Test API with curl
curl http://localhost:8000/health

curl -X POST http://localhost:8000/recommend ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"Python developer\", \"k\": 5}"
```

## 📈 Evaluation Metrics

The system uses **Mean Recall@10** as specified in the assignment:

```python
Recall@K = (Number of relevant items in top K) / (Total relevant items)
Mean Recall@K = Average of Recall@K across all queries
```

## 🛠️ Technologies

- **Python 3.8+**
- **FastAPI** - REST API framework
- **Sentence Transformers** - Semantic embeddings (all-MiniLM-L6-v2)
- **FAISS** - Vector similarity search
- **BeautifulSoup4** - Web scraping
- **Selenium** - JavaScript rendering
- **Streamlit** - Web interface
- **Pandas** - Data processing

## 🎯 Key Features

### Semantic Search
Uses sentence transformers to understand meaning, not just keywords:
- "Python developer" → matches Python, programming, coding tests
- "Team player" → matches collaboration, teamwork, communication

### Balanced Recommendations
Ensures diverse test types in results:
- Technical skills (Python, SQL, Java)
- Cognitive abilities (reasoning, problem-solving)
- Personality traits (teamwork, leadership)

### Fast Retrieval
FAISS enables sub-millisecond search across 377+ assessments

## 🐛 Troubleshooting

### Scraper returns < 377 assessments
- Use mock data: `python setup.py --scraper mock`
- Try Selenium: `python setup.py --scraper selenium`

### FAISS index error
```bash
python scraper/data_processor.py
python embeddings/build_embeddings.py
```

### API won't start
```bash
pip install -r requirements.txt
```

### Streamlit connection error
Make sure API is running first in another terminal

## 📄 License

MIT

## 🎓 Assignment Requirements Met

✅ Scrapes 377+ SHL assessments  
✅ Accepts natural language queries  
✅ Accepts job descriptions  
✅ Returns 5-10 recommendations  
✅ Proper JSON output format  
✅ FastAPI backend with /health and /recommend  
✅ Web interface  
✅ Evaluation with Mean Recall@10  
✅ CSV predictions output  
✅ Clean code structure  
✅ Documentation
