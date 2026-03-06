import pandas as pd
import numpy as np
from typing import List, Dict

def recall_at_k(predicted: List[str], actual: List[str], k: int = 10) -> float:
    """
    Calculate Recall@K
    
    Args:
        predicted: List of predicted assessment URLs
        actual: List of actual relevant assessment URLs
        k: Number of top predictions to consider
    
    Returns:
        Recall@K score
    """
    if not actual:
        return 0.0
    
    predicted_k = predicted[:k]
    relevant_found = len(set(predicted_k) & set(actual))
    
    return relevant_found / len(actual)

def mean_recall_at_k(predictions: Dict[str, List[str]], 
                     ground_truth: Dict[str, List[str]], 
                     k: int = 10) -> float:
    """
    Calculate Mean Recall@K across all queries
    
    Args:
        predictions: Dict mapping query to list of predicted URLs
        ground_truth: Dict mapping query to list of actual URLs
        k: Number of top predictions to consider
    
    Returns:
        Mean Recall@K score
    """
    recalls = []
    
    for query in ground_truth:
        if query in predictions:
            recall = recall_at_k(predictions[query], ground_truth[query], k)
            recalls.append(recall)
    
    return np.mean(recalls) if recalls else 0.0

def evaluate_from_csv(predictions_file: str, ground_truth_file: str, k: int = 10):
    """
    Evaluate predictions from CSV files
    
    CSV format:
    Query,Assessment_url
    query1,url1
    query1,url2
    """
    # Load predictions
    pred_df = pd.read_csv(predictions_file)
    predictions = pred_df.groupby('Query')['Assessment_url'].apply(list).to_dict()
    
    # Load ground truth
    gt_df = pd.read_csv(ground_truth_file)
    ground_truth = gt_df.groupby('Query')['Assessment_url'].apply(list).to_dict()
    
    # Calculate metrics
    mean_recall = mean_recall_at_k(predictions, ground_truth, k)
    
    print(f"Mean Recall@{k}: {mean_recall:.4f}")
    
    # Per-query breakdown
    print("\nPer-Query Results:")
    for query in ground_truth:
        if query in predictions:
            recall = recall_at_k(predictions[query], ground_truth[query], k)
            print(f"  {query[:50]}... : {recall:.4f}")
    
    return mean_recall

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python evaluate_recall.py <predictions.csv> <ground_truth.csv>")
        sys.exit(1)
    
    predictions_file = sys.argv[1]
    ground_truth_file = sys.argv[2]
    
    evaluate_from_csv(predictions_file, ground_truth_file)
