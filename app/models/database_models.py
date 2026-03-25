from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
)
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("UserSession", back_populates="user")
    datasets = relationship("Dataset", back_populates="user")
    models = relationship("Model", back_populates="user")


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_token = Column(String(255), unique=True, index=True)
    login_time = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="sessions")


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_path = Column(String(255))
    file_name = Column(String(100))
    upload_date = Column(DateTime, default=datetime.utcnow)
    total_records = Column(Integer)
    features_count = Column(Integer)

    user = relationship("User", back_populates="datasets")
    models = relationship("Model", back_populates="dataset")


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    model_name = Column(String(100), index=True)
    model_type = Column(String(50))
    # Path to joblib model file on local storage.
    model_file_path = Column(String(255))  # Path to joblib file
    # Serialized joblib model data stored in PostgreSQL.
    model_binary = Column(LargeBinary)
    training_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="untrained")

    user = relationship("User", back_populates="models")
    dataset = relationship("Dataset", back_populates="models")
    metrics = relationship(
        "ModelMetrics", back_populates="model", uselist=False
    )
    predictions = relationship("Prediction", back_populates="model")


class ModelMetrics(Base):
    __tablename__ = "model_metrics"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("models.id"), unique=True)
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    confusion_matrix = Column(JSON)  # Store as JSON array
    training_time = Column(Float)  # in seconds
    calculated_at = Column(DateTime, default=datetime.utcnow)

    model = relationship("Model", back_populates="metrics")


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("models.id"))
    input_features = Column(JSON)  # Store input features as JSON
    prediction = Column(String(20))  # e.g., 'Rock' or 'Mine'
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    model = relationship("Model", back_populates="predictions")
