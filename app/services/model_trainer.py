import joblib
import numpy as np
import io
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from typing import Dict, Any

class ModelTrainer:
    def __init__(self):
        self.model = None
        self.model_type = None
    
    def create_model(self, model_type: str = "RandomForest", **kwargs) -> Any:
        """Create a model based on type"""
        if model_type == "RandomForest":
            self.model = RandomForestClassifier(
                n_estimators=kwargs.get('n_estimators', 100),
                random_state=kwargs.get('random_state', 42),
                n_jobs=-1
            )
        elif model_type == "SVM":
            self.model = SVC(
                kernel=kwargs.get('kernel', 'rbf'),
                probability=True,
                random_state=kwargs.get('random_state', 42)
            )
        elif model_type == "LogisticRegression":
            self.model = LogisticRegression(
                max_iter=kwargs.get('max_iter', 1000),
                random_state=kwargs.get('random_state', 42)
            )
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        self.model_type = model_type
        return self.model
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the model"""
        if self.model is None:
            raise ValueError("Model not initialized. Call create_model first.")
        
        self.model.fit(X_train, y_train)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        return self.model.predict(X)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Get prediction probabilities"""
        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(X)
        else:
            # For SVM, use decision_function
            return self.model.decision_function(X)
    
    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """Evaluate model performance"""
        metrics = {
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "precision": float(precision_score(y_true, y_pred, average='weighted')),
            "recall": float(recall_score(y_true, y_pred, average='weighted')),
            "f1_score": float(f1_score(y_true, y_pred, average='weighted')),
        }
        return metrics
    
    def get_confusion_matrix(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        """Get confusion matrix"""
        cm = confusion_matrix(y_true, y_pred)
        return {
            "matrix": cm.tolist(),
            "labels": sorted(np.unique(y_true).tolist())
        }
    
    def save_model(self, file_path: str) -> None:
        """Save model to disk"""
        joblib.dump(self.model, file_path)
    
    def save_model_binary(self) -> bytes:
        """Save model as binary for database storage"""
        buffer = io.BytesIO()
        joblib.dump(self.model, buffer)
        return buffer.getvalue()
    
    def load_model(self, file_path: str) -> None:
        """Load model from disk"""
        self.model = joblib.load(file_path)
    
    def load_model_binary(self, model_binary: bytes) -> None:
        """Load model from binary"""
        buffer = io.BytesIO(model_binary)
        self.model = joblib.load(buffer)
