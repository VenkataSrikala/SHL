import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recommender.recommend import recommend_assessments

def generate_predictions(test_file: str, output_file: str, k: int = 10):
    """
    Generate predictions for test queries
    
    Args:
        test_file: CSV file with test queries
        output_file: Output CSV file for predictions
        k: Number of recommendations per query
    """
    print(f"Loading test queries from {test_file}")
    
    # Load test queries
    test_df = pd.read_csv(test_file)
    queries = test_df['Query'].unique()
    
    print(f"Found {len(queries)} unique queries")
    
    # Generate predictions
    predictions = []
    
    for i, query in enumerate(queries, 1):
        print(f"Processing query {i}/{len(queries)}: {query[:50]}...")
        
        try:
            results = recommend_assessments(query, k=k, balanced=True)
            
            for result in results:
                predictions.append({
                    'Query': query,
                    'Assessment_url': result['url']
                })
        
        except Exception as e:
            print(f"Error processing query: {e}")
            continue
    
    # Save predictions
    pred_df = pd.DataFrame(predictions)
    pred_df.to_csv(output_file, index=False)
    
    print(f"\nGenerated {len(predictions)} predictions")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_predictions.py <test.csv> [output.csv]")
        sys.exit(1)
    
    test_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "outputs/predictions.csv"
    
    os.makedirs("outputs", exist_ok=True)
    generate_predictions(test_file, output_file)
