"""User Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import UserResponse, AvatarUpdate
from app.models.users import User, Avatar
from app.services.auth_service import verify_token

router = APIRouter()

def get_current_user(token: str, db: Session = Depends(get_db)) -> User:
    """Dependency to get current authenticated user"""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/profile/{user_id}", response_model=UserResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Get user profile by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/profile/username/{username}", response_model=UserResponse)
def get_user_by_username_route(username: str, db: Session = Depends(get_db)):
    """Get user profile by username"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.put("/profile", response_model=UserResponse)
def update_profile(
    update_data: dict,
    token: str,
    db: Session = Depends(get_db)
):
    """Update user profile"""
    user = get_current_user(token, db)
    
    if "bio" in update_data:
        user.bio = update_data["bio"]
    if "location" in update_data:
        user.location = update_data["location"]
    if "full_name" in update_data:
        user.full_name = update_data["full_name"]
    
    db.commit()
    db.refresh(user)
    return user

@router.get("/avatar/{user_id}")
def get_avatar(user_id: int, db: Session = Depends(get_db)):
    """Get user's avatar configuration"""
    avatar = db.query(Avatar).filter(Avatar.user_id == user_id).first()
    if not avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    
    return avatar

@router.put("/avatar")
def update_avatar(
    avatar_data: AvatarUpdate,
    token: str,
    db: Session = Depends(get_db)
):
    """Update user's avatar"""
    user = get_current_user(token, db)
    
    avatar = db.query(Avatar).filter(Avatar.user_id == user.id).first()
    if not avatar:
        avatar = Avatar(user_id=user.id)
        db.add(avatar)
    
    if avatar_data.base_body:
        avatar.base_body = avatar_data.base_body
    if avatar_data.outfit:
        avatar.outfit = avatar_data.outfit
    if avatar_data.accessories:
        avatar.accessories = avatar_data.accessories
    if avatar_data.theme:
        avatar.theme = avatar_data.theme
    
    db.commit()
    db.refresh(avatar)
    return avatar

@router.get("/search")
def search_users(query: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Search for users by username or full name"""
    users = db.query(User).filter(
        (User.username.ilike(f"%{query}%")) | 
        (User.full_name.ilike(f"%{query}%"))
    ).offset(skip).limit(limit).all()
    
    return users
