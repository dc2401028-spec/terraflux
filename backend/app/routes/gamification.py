"""Gamification Routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.gamification import (
    UserStatsResponse, AchievementResponse, LeaderboardEntryResponse, StreakInfoResponse
)
from app.services.gamification_service import (
    get_user_stats, get_user_achievements, get_leaderboard_global,
    get_leaderboard_city, get_leaderboard_neighborhood, get_streak_info,
    get_coin_shop_items, purchase_item, equip_item
)
from app.services.auth_service import verify_token
from app.models.users import User
from app.models.gamification import CoinShop, UserInventory

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

@router.get("/stats/{user_id}", response_model=UserStatsResponse)
def get_stats(user_id: int, db: Session = Depends(get_db)):
    """Get user statistics"""
    stats = get_user_stats(db, user_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Stats not found")
    
    return stats

@router.get("/streak/{user_id}", response_model=StreakInfoResponse)
def get_streak(user_id: int, db: Session = Depends(get_db)):
    """Get user's streak information"""
    streak = get_streak_info(db, user_id)
    if not streak:
        raise HTTPException(status_code=404, detail="Streak not found")
    
    return streak

@router.get("/achievements/{user_id}", response_model=List[AchievementResponse])
def get_achievements(user_id: int, db: Session = Depends(get_db)):
    """Get user's earned achievements"""
    achievements = get_user_achievements(db, user_id)
    return achievements

@router.get("/leaderboard/global", response_model=List[LeaderboardEntryResponse])
def get_global_leaderboard(limit: int = Query(100, le=1000), db: Session = Depends(get_db)):
    """Get global leaderboard"""
    users = get_leaderboard_global(db, limit)
    
    result = []
    for idx, user in enumerate(users, 1):
        result.append({
            "rank": idx,
            "username": user.username,
            "total_points": user.total_points,
            "total_actions": 0,  # Would need to count from eco_actions table
            "level": user.level,
            "avatar_url": user.avatar_url
        })
    
    return result

@router.get("/leaderboard/city/{city}", response_model=List[LeaderboardEntryResponse])
def get_city_leaderboard(city: str, limit: int = Query(100, le=1000), db: Session = Depends(get_db)):
    """Get city leaderboard"""
    entries = get_leaderboard_city(db, city, limit)
    
    result = []
    for entry in entries:
        result.append({
            "rank": entry.rank,
            "username": entry.username,
            "total_points": entry.total_points,
            "total_actions": 0,
            "level": 1,
            "avatar_url": None
        })
    
    return result

@router.get("/leaderboard/neighborhood/{neighborhood}", response_model=List[LeaderboardEntryResponse])
def get_neighborhood_leaderboard(neighborhood: str, limit: int = Query(100, le=1000), db: Session = Depends(get_db)):
    """Get neighborhood leaderboard"""
    entries = get_leaderboard_neighborhood(db, neighborhood, limit)
    
    result = []
    for entry in entries:
        result.append({
            "rank": entry.rank,
            "username": entry.username,
            "total_points": entry.total_points,
            "total_actions": 0,
            "level": 1,
            "avatar_url": None
        })
    
    return result

@router.get("/shop")
def get_shop(item_type: str = None, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Get coin shop items"""
    items = get_coin_shop_items(db, item_type, skip, limit)
    return items

@router.post("/shop/purchase/{item_id}")
def purchase_from_shop(
    item_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    """Purchase an item from coin shop"""
    user = get_current_user(token, db)
    
    if not purchase_item(db, user.id, item_id):
        raise HTTPException(status_code=400, detail="Purchase failed")
    
    return {"message": "Item purchased successfully"}

@router.get("/inventory")
def get_inventory(token: str, db: Session = Depends(get_db)):
    """Get user's inventory"""
    user = get_current_user(token, db)
    
    inventory = db.query(UserInventory).filter(UserInventory.user_id == user.id).all()
    return inventory

@router.post("/inventory/{inventory_id}/equip")
def equip_inventory_item(
    inventory_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    """Equip an item from inventory"""
    user = get_current_user(token, db)
    
    if not equip_item(db, user.id, inventory_id):
        raise HTTPException(status_code=400, detail="Cannot equip item")
    
    return {"message": "Item equipped"}
