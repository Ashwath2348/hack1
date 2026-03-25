import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from typing import Tuple

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load CSV file into DataFrame"""
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise ValueError(f"Error loading data: {str(e)}")
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean data by handling missing values and outliers"""
        # Remove duplicate rows
        df = df.drop_duplicates()
        
        # Handle missing values (if any)
        df = df.dropna()
        
        return df
    
    def preprocess_features(self, df: pd.DataFrame, target_column: str = None) -> Tuple[pd.DataFrame, pd.Series]:
        """Preprocess features: separate features and target"""
        if target_column:
            X = df.drop(columns=[target_column])
            y = df[target_column]
        else:
            # Assume last column is target
            X = df.iloc[:, :-1]
            y = df.iloc[:, -1]
        
        # Encode categorical target if needed
        if y.dtype == 'object':
            self.label_mapping = {label: idx for idx, label in enumerate(y.unique())}
            y = y.map(self.label_mapping)
        
        return X, y
    
    def scale_features(self, X: pd.DataFrame, fit: bool = True) -> np.ndarray:
        """Standardize features"""
        if fit:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        return X_scaled
    
    def split_data(self, X: np.ndarray, y: pd.Series, test_size: float = 0.2, random_state: int = 42) -> Tuple:
        """Split data into train and test sets"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        return X_train, X_test, y_train, y_test
    
    def get_feature_names(self, df: pd.DataFrame, target_column: str = None):
        """Get feature names excluding target"""
        if target_column:
            return df.drop(columns=[target_column]).columns.tolist()
        else:
            return df.iloc[:, :-1].columns.tolist()
