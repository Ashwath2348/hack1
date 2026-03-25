from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import time
from app.database import get_db
from app.models.database_models import Model, Dataset, User, ModelMetrics
from app.schemas.schemas import TrainingRequest, TrainingResponse, Model as ModelSchema
from app.services.data_preprocessor import DataPreprocessor
from app.services.model_trainer import ModelTrainer
from pathlib import Path

router = APIRouter(prefix="/api/training", tags=["training"])

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

def train_model_task(
    model_id: int,
    dataset_id: int,
    model_type: str,
    test_size: float,
    random_state: int,
    db: Session
):
    """Background task for model training"""
    try:
        # Get dataset
        dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not dataset:
            return
        
        # Update model status
        model = db.query(Model).filter(Model.id == model_id).first()
        model.status = "training"
        db.commit()
        
        # Load and preprocess data
        preprocessor = DataPreprocessor()
        df = preprocessor.load_data(dataset.file_path)
        df = preprocessor.clean_data(df)
        X, y = preprocessor.preprocess_features(df)
        X_scaled = preprocessor.scale_features(X, fit=True)
        X_train, X_test, y_train, y_test = preprocessor.split_data(
            X_scaled, y, test_size=test_size, random_state=random_state
        )
        
        # Train model
        trainer = ModelTrainer()
        trainer.create_model(model_type, random_state=random_state)
        
        start_time = time.time()
        trainer.train(X_train, y_train)
        training_time = time.time() - start_time
        
        # Make predictions
        y_pred = trainer.predict(X_test)
        
        # Calculate metrics
        metrics = trainer.evaluate(y_test, y_pred)
        confusion_mat = trainer.get_confusion_matrix(y_test, y_pred)
        
        # Save model
        model_path = MODEL_DIR / f"model_{model_id}.joblib"
        trainer.save_model(str(model_path))
        model_binary = trainer.save_model_binary()
        
        # Update model in database
        model.status = "trained"
        model.model_file_path = str(model_path)
        model.model_binary = model_binary
        db.commit()
        
        # Save metrics
        model_metrics = ModelMetrics(
            model_id=model_id,
            accuracy=metrics["accuracy"],
            precision=metrics["precision"],
            recall=metrics["recall"],
            f1_score=metrics["f1_score"],
            confusion_matrix=confusion_mat,
            training_time=training_time
        )
        db.add(model_metrics)
        db.commit()
        
    except Exception as e:
        model = db.query(Model).filter(Model.id == model_id).first()
        if model:
            model.status = "failed"
            db.commit()

@router.post("/train")
async def start_training(
    request: TrainingRequest,
    background_tasks: BackgroundTasks,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """Start model training (async)"""
    try:
        # Validate dataset exists
        dataset = db.query(Dataset).filter(Dataset.id == request.dataset_id).first()
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        # Create model record
        model = Model(
            user_id=user_id,
            dataset_id=request.dataset_id,
            model_name=f"{request.model_type}_model_{int(time.time())}",
            model_type=request.model_type,
            status="queued"
        )
        
        db.add(model)
        db.commit()
        db.refresh(model)
        
        # Add training task to background
        background_tasks.add_task(
            train_model_task,
            model_id=model.id,
            dataset_id=request.dataset_id,
            model_type=request.model_type,
            test_size=request.test_size,
            random_state=request.random_state,
            db=db
        )
        
        return TrainingResponse(
            model_id=model.id,
            model_name=model.model_name,
            status="queued",
            message="Training started. Check status using model_id"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{model_id}")
def get_training_status(model_id: int, db: Session = Depends(get_db)):
    """Get model training status"""
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    response = {
        "model_id": model.id,
        "model_name": model.model_name,
        "status": model.status,
        "training_date": model.training_date
    }
    
    if model.metrics:
        response["metrics"] = {
            "accuracy": model.metrics.accuracy,
            "precision": model.metrics.precision,
            "recall": model.metrics.recall,
            "f1_score": model.metrics.f1_score,
            "training_time": model.metrics.training_time
        }
    
    return response

@router.get("/models")
def list_models(user_id: int = 1, db: Session = Depends(get_db)):
    """List all trained models for a user"""
    models = db.query(Model).filter(Model.user_id == user_id).all()
    
    response = []
    for model in models:
        model_data = {
            "id": model.id,
            "model_name": model.model_name,
            "model_type": model.model_type,
            "status": model.status,
            "training_date": model.training_date
        }
        if model.metrics:
            model_data["metrics"] = {
                "accuracy": model.metrics.accuracy,
                "precision": model.metrics.precision,
                "recall": model.metrics.recall,
                "f1_score": model.metrics.f1_score
            }
        response.append(model_data)
    
    return response
