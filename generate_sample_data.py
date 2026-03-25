"""
Generate sample Rock vs Mine dataset for testing
Simulates the Sonar dataset structure (60 features + 1 target)
"""
import pandas as pd
import numpy as np
from pathlib import Path

def generate_sample_dataset(
    n_samples=208,
    n_features=60,
    output_path="datasets/sample_sonar.csv"
):
    """
    Generate a sample Rock vs Mine dataset
    
    Args:
        n_samples: Number of samples to generate
        n_features: Number of features (default 60 for sonar dataset)
        output_path: Path to save the CSV file
    """
    
    print(f"Generating sample dataset...")
    print(f"  - Samples: {n_samples}")
    print(f"  - Features: {n_features}")
    
    # Create output directory if it doesn't exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Generate random features (0-1 range, typical for normalized sonar data)
    X = np.random.uniform(0.0, 0.35, size=(n_samples, n_features))
    
    # Generate target (0 = Rock, 1 = Mine)
    # Roughly 50-50 split
    y = np.random.binomial(1, 0.5, size=n_samples)
    
    # Create DataFrame with feature names
    feature_cols = [f"feature_{i}" for i in range(n_features)]
    data = pd.DataFrame(X, columns=feature_cols)
    
    # Add target column
    data['target'] = y
    data['target'] = data['target'].map({0: 'R', 1: 'M'})  # R = Rock, M = Mine
    
    # Save to CSV
    data.to_csv(output_path, index=False)
    
    print(f"\n✓ Sample dataset generated successfully!")
    print(f"✓ File: {output_path}")
    print(f"✓ Shape: {data.shape}")
    print(f"✓ Classes: {data['target'].value_counts().to_dict()}")
    print(f"\nFirst few rows:")
    print(data.head())
    
    return data

if __name__ == "__main__":
    # Generate sample dataset
    df = generate_sample_dataset()
    
    print("\n" + "="*60)
    print("You can now use this dataset for testing the backend!")
    print("Upload it via: POST /api/datasets/upload")
    print("="*60)
