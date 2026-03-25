from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.database_models import User, UserSession
from app.schemas.schemas import UserCreate, User as UserSchema
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.username == user_data.username) | (User.email == user_data.email)
        ).first()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Username or email already exists")
        
        # Create new user
        user = User(
            username=user_data.username,
            email=user_data.email
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at,
            "message": "User registered successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    }

@router.post("/login")
def login_user(username: str, db: Session = Depends(get_db)):
    """Login user and create session"""
    try:
        # Find user
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create session
        session_token = str(uuid.uuid4())
        user_session = UserSession(
            user_id=user.id,
            session_token=session_token,
            is_active=True
        )
        
        db.add(user_session)
        db.commit()
        db.refresh(user_session)
        
        return {
            "user_id": user.id,
            "username": user.username,
            "session_token": session_token,
            "login_time": user_session.login_time,
            "message": "Login successful"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/logout")
def logout_user(session_token: str, db: Session = Depends(get_db)):
    """Logout user (deactivate session)"""
    try:
        user_session = db.query(UserSession).filter(
            UserSession.session_token == session_token
        ).first()
        
        if not user_session:
            raise HTTPException(status_code=401, detail="Invalid session token")
        
        user_session.is_active = False
        db.commit()
        
        return {"message": "Logout successful"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{user_id}")
def get_active_sessions(user_id: int, db: Session = Depends(get_db)):
    """Get all active sessions for a user"""
    sessions = db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.is_active == True
    ).all()
    
    return [
        {
            "session_id": s.id,
            "session_token": s.session_token,
            "login_time": s.login_time,
            "last_activity": s.last_activity
        }
        for s in sessions
    ]
