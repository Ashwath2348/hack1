from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Dataset Schemas
class DatasetBase(BaseModel):
    file_name: str

class DatasetCreate(DatasetBase):
    pass

class Dataset(DatasetBase):
    id: int
    user_id: int
    upload_date: datetime
    total_records: int
    features_count: int
    
    class Config:
        from_attributes = True

# Model Metrics Schemas
class ModelMetricsBase(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: Dict[str, Any]
    training_time: float

class ModelMetrics(ModelMetricsBase):
    id: int
    model_id: int
    calculated_at: datetime
    
    class Config:
        from_attributes = True

# Model Schemas
class ModelBase(BaseModel):
    model_name: str
    model_type: str

class ModelCreate(ModelBase):
    dataset_id: int

class Model(ModelBase):
    id: int
    user_id: int
    dataset_id: int
    training_date: datetime
    status: str
    metrics: Optional[ModelMetrics] = None
    
    class Config:
        from_attributes = True

# Prediction Schemas
class PredictionBase(BaseModel):
    input_features: Dict[str, Any]

class PredictionCreate(PredictionBase):
    model_id: int

class Prediction(PredictionBase):
    id: int
    model_id: int
    prediction: str
    confidence: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# Training Request Schema
class TrainingRequest(BaseModel):
    dataset_id: int
    model_type: str = "RandomForest"
    test_size: float = 0.2
    random_state: int = 42

# Prediction Request Schema
class PredictionRequest(BaseModel):
    features: List[float]

# Response Schemas
class TrainingResponse(BaseModel):
    model_id: int
    model_name: str
    status: str
    message: str

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    model_id: int
