from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import numpy as np
from app.database import get_db
from app.models.database_models import Model, Prediction, User
from app.schemas.schemas import PredictionRequest, PredictionResponse
from app.services.model_trainer import ModelTrainer
import json

router = APIRouter(prefix="/api/predictions", tags=["predictions"])

# Label mapping for Rock vs Mine
LABEL_MAP = {0: "Rock", 1: "Mine"}
REVERSE_LABEL_MAP = {"Rock": 0, "Mine": 1}

@router.post("/predict/{model_id}")
def make_prediction(
    model_id: int,
    request: PredictionRequest,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """Make prediction using a trained model"""
    try:
        # Get model
        model = db.query(Model).filter(
            Model.id == model_id,
            Model.user_id == user_id
        ).first()
        
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        
        if model.status != "trained":
            raise HTTPException(status_code=400, detail="Model is not trained yet")
        
        # Load model
        trainer = ModelTrainer()
        trainer.load_model_binary(model.model_binary)
        
        # Prepare features
        features = np.array(request.features).reshape(1, -1)
        
        # Make prediction
        prediction = trainer.predict(features)[0]
        
        # Get confidence
        proba = trainer.predict_proba(features)[0]
        confidence = float(max(proba))
        
        # Convert prediction to label
        prediction_label = LABEL_MAP.get(prediction, str(prediction))
        
        # Save prediction to database
        db_prediction = Prediction(
            model_id=model_id,
            input_features={f"feature_{i}": float(f) for i, f in enumerate(request.features)},
            prediction=prediction_label,
            confidence=confidence
        )
        
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        
        return PredictionResponse(
            prediction=prediction_label,
            confidence=confidence,
            model_id=model_id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{model_id}")
def get_prediction_history(
    model_id: int,
    user_id: int = 1,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get prediction history for a model"""
    try:
        # Verify model belongs to user
        model = db.query(Model).filter(
            Model.id == model_id,
            Model.user_id == user_id
        ).first()
        
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        
        predictions = db.query(Prediction).filter(
            Prediction.model_id == model_id
        ).order_by(Prediction.created_at.desc()).limit(limit).all()
        
        return [
            {
                "id": p.id,
                "prediction": p.prediction,
                "confidence": p.confidence,
                "created_at": p.created_at,
                "input_features": p.input_features
            }
            for p in predictions
        ]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/{model_id}")
def get_model_metrics(
    model_id: int,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """Get model evaluation metrics"""
    try:
        model = db.query(Model).filter(
            Model.id == model_id,
            Model.user_id == user_id
        ).first()
        
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        
        if not model.metrics:
            raise HTTPException(status_code=404, detail="Model metrics not found")
        
        metrics = model.metrics
        
        return {
            "model_id": model_id,
            "model_name": model.model_name,
            "model_type": model.model_type,
            "accuracy": metrics.accuracy,
            "precision": metrics.precision,
            "recall": metrics.recall,
            "f1_score": metrics.f1_score,
            "confusion_matrix": metrics.confusion_matrix,
            "training_time": metrics.training_time,
            "calculated_at": metrics.calculated_at
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
