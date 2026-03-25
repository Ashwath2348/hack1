# Rock vs Mine AI/ML Project - Backend

Complete end-to-end machine learning backend for Rock vs Mine (Sonar) classification.

## 🎯 Project Overview

This is a full-stack ML backend built with:
- **FastAPI** - Modern async web framework
- **PostgreSQL** - Persistent data storage
- **scikit-learn** - ML model training
- **Pandas** - Data processing
- **SQLAlchemy** - ORM for database

## ✨ Key Features

✅ **Complete ML Pipeline**
- Data preprocessing (cleaning, scaling, splitting)
- Model training (RandomForest, SVM, LogisticRegression)
- Async background training tasks
- Real-time predictions

✅ **Database Integration**
- PostgreSQL with SQLAlchemy ORM
- Store models as binary + joblib files
- Track model metrics and predictions
- User session management

✅ **REST API**
- 15+ API endpoints
- Auto-generated Swagger/ReDoc docs
- Full error handling
- Request/response validation

✅ **Production Ready**
- Docker & docker-compose support
- CORS enabled
- Health checks
- Comprehensive logging

## 📁 Project Structure

```
hack1/
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── routes/          # API endpoints
│   ├── services/        # ML services
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   └── main.py          # FastAPI app
├── datasets/            # CSV datasets
├── models/              # Trained models
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── Dockerfile           # Container image
├── docker-compose.yml   # Container orchestration
├── test_api.py          # API tests
└── README.md            # This file
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Start services
docker-compose up -d

# Backend will be available at: http://localhost:8000
# PostgreSQL will be available at: localhost:5432
```

### Option 2: Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Run backend
python main.py
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Common Tasks

### Generate Sample Dataset

```bash
python generate_sample_data.py
```

### Test API Endpoints

```bash
python test_api.py
```

### Access Database

```bash
# If using Docker
docker exec -it rock_vs_mine_db psql -U rock_user -d rock_vs_mine
```

## 📖 API Endpoints

### Users
- `POST /api/users/register` - Register user
- `POST /api/users/login` - Login user
- `GET /api/users/{id}` - Get user info

### Datasets
- `POST /api/datasets/upload` - Upload CSV
- `GET /api/datasets` - List datasets
- `GET /api/datasets/{id}` - Get dataset info

### Training
- `POST /api/training/train` - Start training
- `GET /api/training/status/{model_id}` - Training status
- `GET /api/training/models` - List models

### Predictions
- `POST /api/predictions/predict/{model_id}` - Make prediction
- `GET /api/predictions/history/{model_id}` - Prediction history
- `GET /api/predictions/metrics/{model_id}` - Model metrics

## 💾 Database Models

- **User**: User accounts and metadata
- **UserSession**: Active sessions
- **Dataset**: Uploaded datasets
- **Model**: Trained models
- **ModelMetrics**: Model performance (accuracy, precision, recall, f1)
- **Prediction**: Prediction history with confidence

## 🛠 Configuration

Edit `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost:5432/rock_vs_mine
SECRET_KEY=your-secret-key
DEBUG=True
```

## 📦 Dependencies

- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- PostgreSQL compatible
- scikit-learn 1.3.2
- pandas 2.1.3

See `requirements.txt` for complete list.

## 🧪 Testing

```bash
# Run workflow test
python test_api.py

# Or use curl
curl http://localhost:8000/health
```

## 📝 Example Workflow

1. **Register User**
   ```bash
   curl -X POST "http://localhost:8000/api/users/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com"
     }'
   ```

2. **Upload Dataset**
   ```bash
   curl -X POST "http://localhost:8000/api/datasets/upload" \
     -F "file=@datasets/sample_sonar.csv" \
     -F "user_id=1"
   ```

3. **Train Model**
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

4. **Make Prediction**
   ```bash
   curl -X POST "http://localhost:8000/api/predictions/predict/1" \
     -H "Content-Type: application/json" \
     -d '{"features": [...]}'
   ```

5. **Get Metrics**
   ```bash
   curl "http://localhost:8000/api/predictions/metrics/1?user_id=1"
   ```

## 🐛 Troubleshooting

**PostgreSQL connection error?**
- Check DATABASE_URL in .env
- Ensure PostgreSQL is running
- Verify credentials

**Port 8000 already in use?**
- Change port: `uvicorn app.main:app --port 8001`

**Models not found?**
- Wait for training to complete
- Check `/api/training/status/{model_id}`

## 📚 Additional Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [scikit-learn Docs](https://scikit-learn.org/)

## 📋 Detailed Setup Guide

See `BACKEND_SETUP.md` for comprehensive setup instructions.

## ✅ Status

- ✅ API endpoints implemented
- ✅ Database models created
- ✅ ML pipeline built
- ✅ Docker support
- ✅ Testing scripts
- ⏳ Frontend integration (coming soon)

---

**Next branch to checkout**: Frontend development  
**Questions?** Check API docs at `/docs` when running the server
# AI Sonar Detection System

Frontend-only React simulation for submarine sonar-based Rock vs Mine detection.

## Stack
- React (hooks + functional components)
- Tailwind CSS
- Recharts
- Framer Motion

## Run
1. `npm install`
2. `npm run dev`

## Features
- Landing page with animated sonar
- Dashboard with 60-point sonar input grid
- Manual mode + random sonar generator
- Frontend AI simulation (`Rock` vs `Mine`) with confidence score
- Result alert animation + warning beep for mine detection
- Line + bar charts for sonar data
- Detection history in local state
- Dark/light mode toggle
