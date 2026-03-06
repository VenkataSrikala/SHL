# How to Test the API

## Quick Start (Easiest Way)

### Step 1: Start the API
Open a terminal and run:
```bash
uvicorn api.main:app --reload
```

Wait until you see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 2: Test It

Choose one of these methods:

---

## Method 1: Use the Web UI (Recommended)

Open another terminal and run:
```bash
streamlit run frontend/app.py
```

Then:
1. Open http://localhost:8501 in your browser
2. Enter your query: "Python developer with SQL skills"
3. Click "Find Assessments"
4. See the results!

---

## Method 2: Use Python Script

```bash
python test_api.py
```

This will automatically test:
- Health endpoint
- Recommend endpoint
- Multiple queries

---

## Method 3: Use PowerShell Script

```powershell
.\test_api.ps1
```

---

## Method 4: Use curl (Manual)

### Test Health:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy"}
```

### Test Recommend:
```bash
curl -X POST http://localhost:8000/recommend ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"Python developer with SQL skills\", \"k\": 10, \"balanced\": true}"
```

Expected response:
```json
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
    },
    ...
  ]
}
```

---

## Method 5: Use Python Requests (Interactive)

```python
import requests

# Test health
response = requests.get("http://localhost:8000/health")
print(response.json())

# Test recommend
response = requests.post(
    "http://localhost:8000/recommend",
    json={
        "query": "Python developer with SQL skills",
        "k": 10,
        "balanced": True
    }
)

results = response.json()
for i, assessment in enumerate(results["recommended_assessments"][:5], 1):
    print(f"{i}. {assessment['name']}")
```

---

## Method 6: Use Postman

1. Download Postman: https://www.postman.com/downloads/
2. Create new request
3. Set method to POST
4. URL: `http://localhost:8000/recommend`
5. Headers: `Content-Type: application/json`
6. Body (raw JSON):
```json
{
  "query": "Python developer with SQL skills",
  "k": 10,
  "balanced": true
}
```
7. Click Send

---

## Method 7: Use Browser (for GET requests only)

Open in browser:
- Health: http://localhost:8000/health
- API Docs: http://localhost:8000/docs (Interactive Swagger UI!)
- Alternative Docs: http://localhost:8000/redoc

The `/docs` endpoint is the easiest - it has a built-in UI to test the API!

---

## Troubleshooting

### Error: "Connection refused"
**Problem**: API is not running

**Solution**: Start the API first:
```bash
uvicorn api.main:app --reload
```

---

### Error: "FAISS index not found"
**Problem**: System not set up

**Solution**: Run setup:
```bash
python setup.py --scraper mock
```

---

### Error: "Module not found"
**Problem**: Dependencies not installed

**Solution**: Install requirements:
```bash
pip install -r requirements.txt
```

---

## Sample Queries to Test

Try these different queries:

1. **Technical Skills**:
   - "Python developer with SQL skills"
   - "Java programmer with debugging experience"
   - "JavaScript developer for web applications"

2. **Data & Analytics**:
   - "Data analyst with visualization skills"
   - "SQL expert with statistical analysis"
   - "Excel power user with data analysis"

3. **Soft Skills**:
   - "Team player with communication skills"
   - "Leader with project management experience"
   - "Customer service representative"

4. **Mixed Skills**:
   - "Software engineer with teamwork and problem solving"
   - "Project manager with technical background"
   - "Sales professional with analytical thinking"

---

## Expected Results

For query: "Python developer with SQL skills"

You should get ~10 results including:
- Python New (Knowledge & Skills)
- SQL (Knowledge & Skills)
- Problem Solving tests (Cognitive)
- Possibly some teamwork assessments (Personality)

Results should be:
- ✅ Relevant to the query
- ✅ Balanced across test types
- ✅ Include URLs and descriptions
- ✅ Return in <100ms

---

## API Documentation

Once the API is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

These provide:
- Full API documentation
- Interactive testing interface
- Request/response examples
- Schema definitions

---

## Quick Test Commands

```bash
# 1. Start API (Terminal 1)
uvicorn api.main:app --reload

# 2. Test with Python (Terminal 2)
python test_api.py

# 3. Or test with PowerShell
.\test_api.ps1

# 4. Or start UI
streamlit run frontend/app.py
```

---

## Success Indicators

✅ Health endpoint returns `{"status":"healthy"}`
✅ Recommend endpoint returns 10 assessments
✅ Results are relevant to query
✅ Response time < 1 second
✅ No errors in console

---

## Next Steps

Once testing works:
1. Try different queries
2. Test the web UI
3. Generate predictions: `python evaluation/generate_predictions.py dataset/test.csv outputs/predictions.csv`
4. Deploy to cloud (see DEPLOYMENT.md)
