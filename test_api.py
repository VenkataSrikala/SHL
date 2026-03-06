"""Test the SHL Recommender API"""
import requests
import json

API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure API is running: uvicorn api.main:app --reload")
        return False

def test_recommend():
    """Test recommend endpoint"""
    print("\n2. Testing Recommend Endpoint...")
    
    # Test query
    payload = {
        "query": "Python developer with SQL skills",
        "k": 10,
        "balanced": True
    }
    
    try:
        response = requests.post(
            f"{API_URL}/recommend",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            assessments = data.get("recommended_assessments", [])
            
            print(f"\n   Got {len(assessments)} recommendations")
            print("\n   Top 5 Results:")
            
            for i, assessment in enumerate(assessments[:5], 1):
                print(f"\n   {i}. {assessment['name']}")
                print(f"      Type: {', '.join(assessment['test_type'])}")
                print(f"      Duration: {assessment.get('duration', 'N/A')} min")
                print(f"      URL: {assessment['url']}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_different_queries():
    """Test with different queries"""
    print("\n3. Testing Different Queries...")
    
    queries = [
        "Java developer with teamwork",
        "Data analyst with visualization",
        "Customer service representative"
    ]
    
    for query in queries:
        try:
            response = requests.post(
                f"{API_URL}/recommend",
                json={"query": query, "k": 5},
                timeout=10
            )
            
            if response.status_code == 200:
                count = len(response.json()["recommended_assessments"])
                print(f"   ✅ '{query}' → {count} results")
            else:
                print(f"   ❌ '{query}' → Error {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ '{query}' → {e}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Testing SHL Recommender API")
    print("="*60)
    
    if test_health():
        test_recommend()
        test_different_queries()
    
    print("\n" + "="*60)
    print("Test Complete!")
    print("="*60)
    print()
