from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.database_models import Dataset, User
from app.schemas.schemas import Dataset as DatasetSchema
import os
from pathlib import Path

router = APIRouter(prefix="/api/datasets", tags=["datasets"])

DATASET_DIR = Path("datasets")
DATASET_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    user_id: int = 1,  # In production, get from auth token
    db: Session = Depends(get_db)
):
    """Upload a dataset CSV file"""
    try:
        # Validate file extension
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")
        
        # Check user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Save file
        file_path = DATASET_DIR / file.filename
        contents = await file.read()
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Read metadata
        import pandas as pd
        df = pd.read_csv(file_path)
        
        # Create dataset record
        dataset = Dataset(
            user_id=user_id,
            file_path=str(file_path),
            file_name=file.filename,
            total_records=len(df),
            features_count=len(df.columns) - 1  # Assuming last column is target
        )
        
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        
        return {
            "id": dataset.id,
            "message": f"Dataset {file.filename} uploaded successfully",
            "total_records": dataset.total_records,
            "features_count": dataset.features_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{dataset_id}")
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Get dataset information"""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return dataset

@router.get("")
def list_datasets(user_id: int = 1, db: Session = Depends(get_db)):
    """List all datasets for a user"""
    datasets = db.query(Dataset).filter(Dataset.user_id == user_id).all()
    return datasets

@router.delete("/{dataset_id}")
def delete_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Delete a dataset"""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Delete file
    if os.path.exists(dataset.file_path):
        os.remove(dataset.file_path)
    
    # Delete from database
    db.delete(dataset)
    db.commit()
    
    return {"message": "Dataset deleted successfully"}
