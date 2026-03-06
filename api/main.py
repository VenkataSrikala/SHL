from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recommender.recommend import recommend_assessments

app = FastAPI(
    title="SHL Assessment Recommender API",
    description="AI-powered recommendation system for SHL assessments",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    query: str
    k: Optional[int] = 10
    balanced: Optional[bool] = True

class HealthResponse(BaseModel):
    status: str

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/recommend")
def recommend(request: QueryRequest):
    """
    Recommend SHL assessments based on query
    
    - **query**: Job description or natural language query
    - **k**: Number of recommendations (default: 10)
    - **balanced**: Balance test types (default: True)
    """
    try:
        results = recommend_assessments(
            query=request.query,
            k=request.k,
            balanced=request.balanced
        )
        
        return {
            "recommended_assessments": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "SHL Assessment Recommender API",
        "endpoints": {
            "health": "/health",
            "recommend": "/recommend (POST)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
