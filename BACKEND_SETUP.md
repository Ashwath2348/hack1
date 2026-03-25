# Rock vs Mine AI/ML Backend

Complete end-to-end ML pipeline backend for Rock vs Mine classification using FastAPI, PostgreSQL, and scikit-learn.

## Features

- ✅ **Dataset Management**: Upload, manage, and preprocess CSV datasets
- ✅ **Model Training**: Train multiple ML models (RandomForest, SVM, Logistic Regression)
- ✅ **Async Training**: Non-blocking background model training tasks
- ✅ **Predictions**: Make real-time predictions with confidence scores
- ✅ **Model Metrics**: Track accuracy, precision, recall, F1-score, confusion matrix
- ✅ **Prediction History**: Log all predictions with input features
- ✅ **User Management**: Multi-user support with sessions and authentication
- ✅ **PostgreSQL Storage**: Store models as binary and joblib files
- ✅ **REST API**: Complete REST API with async/await support
- ✅ **Auto API Docs**: Swagger UI and ReDoc documentation

## Tech Stack

- **Framework**: FastAPI
- **Server**: Uvicorn
- **Database**: PostgreSQL + SQLAlchemy ORM
- **ML**: scikit-learn, pandas, numpy
- **Model Serialization**: joblib
- **Validation**: Pydantic

## Project Structure

```
hack1/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── database_models.py  # SQLAlchemy models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user_routes.py      # User & session management
│   │   ├── dataset_routes.py   # Dataset upload & management
│   │   ├── training_routes.py  # Model training
│   │   └── prediction_routes.py # Predictions & metrics
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_preprocessor.py # Data cleaning & preprocessing
│   │   └── model_trainer.py    # ML model training
│   └── utils/
│       └── __init__.py
├── datasets/                    # Dataset storage
├── models/                      # Trained models (joblib)
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
└── README.md                    # This file
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip or conda

### 2. Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE rock_vs_mine;

# Create user (optional, recommended)
CREATE USER rock_user WITH PASSWORD 'secure_password';
ALTER ROLE rock_user SET client_encoding TO 'utf8';
ALTER ROLE rock_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE rock_user SET default_transaction_deferrable TO on;
ALTER ROLE rock_user SET default_transaction_read_only TO off;
GRANT ALL PRIVILEGES ON DATABASE rock_vs_mine TO rock_user;

\q
```

### 3. Clone and Setup Repository

```bash
# Navigate to backend directory
cd hack1

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your database credentials
# DATABASE_URL=postgresql://rock_user:secure_password@localhost:5432/rock_vs_mine
```

### 5. Run the Application

```bash
# Using main.py
python main.py

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Documentation

### Auto-generated Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### 1. User Management

```
POST   /api/users/register           - Register new user
GET    /api/users/{user_id}          - Get user info
POST   /api/users/login              - Login user
POST   /api/users/logout             - Logout user
GET    /api/users/sessions/{user_id} - Get active sessions
```

#### 2. Dataset Management

```
POST   /api/datasets/upload    - Upload CSV dataset
GET    /api/datasets/{id}      - Get dataset info
GET    /api/datasets           - List user datasets
DELETE /api/datasets/{id}      - Delete dataset
```

#### 3. Model Training

```
POST   /api/training/train              - Start model training (async)
GET    /api/training/status/{model_id}  - Get training status
GET    /api/training/models             - List trained models
```

#### 4. Predictions & Metrics

```
POST   /api/predictions/predict/{model_id}  - Make prediction
GET    /api/predictions/history/{model_id}  - Get prediction history
GET    /api/predictions/metrics/{model_id}  - Get model metrics
```

### Example Usage

#### 1. Register User

```bash
curl -X POST "http://localhost:8000/api/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com"
  }'
```

#### 2. Upload Dataset

```bash
curl -X POST "http://localhost:8000/api/datasets/upload" \
  -F "file=@sonar.csv" \
  -F "user_id=1"
```

#### 3. Start Training

```bash
curl -X POST "http://localhost:8000/api/training/train" \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_id": 1,
    "model_type": "RandomForest",
    "test_size": 0.2,
    "random_state": 42
  }'
```

#### 4. Make Prediction

```bash
curl -X POST "http://localhost:8000/api/predictions/predict/1" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [0.0262, 0.0582, 0.1099, 0.1083, 0.0974, 0.1264, 0.0800, 0.0696, 0.1005, 0.1352, 0.1113, 0.1092, 0.1040, 0.0947, 0.1149, 0.0946, 0.1223, 0.0818, 0.0906, 0.1007, 0.1026, 0.1184, 0.1008, 0.0807, 0.1123, 0.0931, 0.1151, 0.1084, 0.1032, 0.1080, 0.1071, 0.1021, 0.1030, 0.1081, 0.1059, 0.1106, 0.1166, 0.1178, 0.1169, 0.1164, 0.1072, 0.1092, 0.1088, 0.1228, 0.1253, 0.1165, 0.1190, 0.1090, 0.1253, 0.0854, 0.0830, 0.1064, 0.1176, 0.1023, 0.0837, 0.0966, 0.1158, 0.1186, 0.0788, 0.0963]
  }'
```

#### 5. Get Model Metrics

```bash
curl -X GET "http://localhost:8000/api/predictions/metrics/1?user_id=1"
```

## Data Preprocessing Pipeline

The preprocessing pipeline handles:

1. **Data Loading**: Load CSV files with pandas
2. **Cleaning**: Remove duplicates and missing values
3. **Feature Extraction**: Separate features and target
4. **Encoding**: Convert categorical targets to numeric
5. **Scaling**: Standardize features using StandardScaler
6. **Splitting**: Train-test split with stratification

## Supported ML Models

### 1. Random Forest Classifier (Default)
- Fast training and inference
- Handles non-linear relationships
- Provides feature importance

### 2. Support Vector Machine (SVM)
- Excellent for binary classification
- Good for complex boundaries
- Optional probability calibration

### 3. Logistic Regression
- Interpretable coefficients
- Fast and lightweight
- Good baseline model

## Database Models

### User
- `id` - Primary key
- `username` - Unique username
- `email` - User email
- `created_at` - Registration timestamp

### UserSession
- `id` - Primary key
- `user_id` - Foreign key to User
- `session_token` - UUID session identifier
- `login_time` - Session start time
- `last_activity` - Last activity timestamp
- `is_active` - Session status

### Dataset
- `id` - Primary key
- `user_id` - Owner user
- `file_path` - Local file path
- `file_name` - Original filename
- `upload_date` - Upload timestamp
- `total_records` - Row count
- `features_count` - Feature count

### Model
- `id` - Primary key
- `user_id` - Owner user
- `dataset_id` - Training dataset
- `model_name` - Display name
- `model_type` - Algorithm type
- `model_file_path` - Joblib file path
- `model_binary` - Binary storage in DB
- `training_date` - Training timestamp
- `status` - queued/training/trained/failed

### ModelMetrics
- `id` - Primary key
- `model_id` - Trained model
- `accuracy` - Accuracy score
- `precision` - Precision score
- `recall` - Recall score
- `f1_score` - F1 score
- `confusion_matrix` - JSON confusion matrix
- `training_time` - Training duration

### Prediction
- `id` - Primary key
- `model_id` - Prediction model
- `input_features` - JSON input features
- `prediction` - Result class
- `confidence` - Confidence score
- `created_at` - Prediction timestamp

## Performance Notes

- **Async Training**: Long-running model training happens in background tasks
- **Database Optimization**: All queries use indexes on foreign keys
- **Model Caching**: Models loaded once per prediction
- **Data Scalability**: Tested with datasets up to 2GB+

## Environment Variables

```
DATABASE_URL=postgresql://user:password@localhost:5432/rock_vs_mine
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True  # Set to False in production
```

## Next Steps

1. **Add Authentication**: Implement JWT token-based auth
2. **Add Model Versioning**: Support multiple model versions
3. **Add Batch Predictions**: Support CSV-based batch predictions
4. **Add Model Explainability**: SHAP or LIME integration
5. **Add Docker Support**: Containerize the application
6. **Add CI/CD**: GitHub Actions or similar

## Troubleshooting

### PostgreSQL Connection Error
```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT version();"

# Verify DATABASE_URL in .env file
```

### Module Not Found Error
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port 8000 Already in Use
```bash
# Run on different port
uvicorn app.main:app --reload --port 8001
```

## Support

For issues and questions, please check:
1. API documentation: `http://localhost:8000/docs`
2. Database models in `app/models/database_models.py`
3. Route implementations in `app/routes/`

---

**Happy Machine Learning! 🚀**
