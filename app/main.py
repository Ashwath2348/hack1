from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import user_routes, dataset_routes, training_routes, prediction_routes

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rock vs Mine ML Backend",
    description="Complete ML Pipeline Backend for Rock vs Mine Classification",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(user_routes.router)
app.include_router(dataset_routes.router)
app.include_router(training_routes.router)
app.include_router(prediction_routes.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Rock vs Mine ML Backend",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Rock vs Mine ML Backend"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
