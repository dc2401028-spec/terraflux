"""Eco-Action Routes"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
from app.database import get_db
from app.schemas.eco_actions import EcoActionCreate, EcoActionResponse, ChallengeResponse
from app.services.eco_action_service import (
    create_eco_action, get_user_eco_actions, get_challenges, complete_challenge
)
from app.services.auth_service import verify_token
from app.models.users import User
from app.models.eco_actions import EcoAction, Challenge
from app.config import settings

router = APIRouter()

def get_current_user(token: str, db: Session = Depends(get_db)) -> User:
    """Get current authenticated user"""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.post("/", response_model=EcoActionResponse)
def log_eco_action(
    action: EcoActionCreate,
    token: str,
    db: Session = Depends(get_db)
):
    """Log a new eco-friendly action"""
    user = get_current_user(token, db)
    
    eco_action = create_eco_action(
        db,
        user.id,
        action.action_type,
        action.title,
        action.description,
        action.location
    )
    
    return eco_action

@router.post("/{action_id}/upload-photo")
def upload_photo(
    action_id: int,
    file: UploadFile = File(...),
    token: str = Depends(lambda t: t),
    db: Session = Depends(get_db)
):
    """Upload photo proof for an eco-action"""
    user = get_current_user(token, db)
    
    eco_action = db.query(EcoAction).filter(
        EcoAction.id == action_id,
        EcoAction.user_id == user.id
    ).first()
    
    if not eco_action:
        raise HTTPException(status_code=404, detail="Eco-action not found")
    
    # Validate file
    if file.content_type not in ["image/jpeg", "image/png", "image/gif", "image/webp"]:
        raise HTTPException(status_code=400, detail="Invalid image format")
    
    # Save file
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = f"{settings.UPLOAD_DIR}{action_id}_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    eco_action.photo_url = file_path
    db.commit()
    
    return {"message": "Photo uploaded successfully", "photo_url": file_path}

@router.get("/", response_model=List[EcoActionResponse])
def get_my_actions(
    skip: int = 0,
    limit: int = 10,
    token: str = Depends(lambda t: t),
    db: Session = Depends(get_db)
):
    """Get current user's eco-actions"""
    user = get_current_user(token, db)
    actions = get_user_eco_actions(db, user.id, skip, limit)
    return actions

@router.get("/{action_id}", response_model=EcoActionResponse)
def get_eco_action(action_id: int, db: Session = Depends(get_db)):
    """Get a specific eco-action"""
    action = db.query(EcoAction).filter(EcoAction.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Eco-action not found")
    
    return action

@router.get("/challenges/active", response_model=List[ChallengeResponse])
def get_active_challenges(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get all active challenges"""
    challenges = get_challenges(db, skip, limit)
    return challenges

@router.post("/challenges/{challenge_id}/complete")
def complete_challenge_endpoint(
    challenge_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    """Complete a challenge"""
    user = get_current_user(token, db)
    
    complete_challenge(db, user.id, challenge_id)
    
    return {"message": "Challenge completed!"}

@router.get("/user/{user_id}", response_model=List[EcoActionResponse])
def get_user_actions(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get eco-actions for a specific user"""
    actions = get_user_eco_actions(db, user_id, skip, limit)
    return actions
