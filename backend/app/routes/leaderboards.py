"""Leaderboard Routes"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.gamification import LeaderboardEntryResponse

router = APIRouter()

@router.get("/global", response_model=List[LeaderboardEntryResponse])
def get_global_leaderboard(limit: int = Query(100, le=1000), db: Session = Depends(get_db)):
    """Get global leaderboard"""
    from app.models.users import User
    
    users = db.query(User).order_by(User.total_points.desc()).limit(limit).all()
    
    result = []
    for idx, user in enumerate(users, 1):
        result.append({
            "rank": idx,
            "username": user.username,
            "total_points": user.total_points,
            "total_actions": 0,
            "level": user.level,
            "avatar_url": user.avatar_url
        })
    
    return result

@router.get("/city/{city}", response_model=List[LeaderboardEntryResponse])
def get_city_leaderboard(city: str, limit: int = Query(100, le=1000), db: Session = Depends(get_db)):
    """Get city leaderboard"""
    from app.models.leaderboards import CityLeaderboard
    
    entries = db.query(CityLeaderboard).filter(
        CityLeaderboard.city_name == city
    ).order_by(CityLeaderboard.rank).limit(limit).all()
    
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

@router.get("/neighborhood/{neighborhood}", response_model=List[LeaderboardEntryResponse])
def get_neighborhood_leaderboard(neighborhood: str, limit: int = Query(100, le=1000), db: Session = Depends(get_db)):
    """Get neighborhood leaderboard"""
    from app.models.leaderboards import NeighborhoodLeaderboard
    
    entries = db.query(NeighborhoodLeaderboard).filter(
        NeighborhoodLeaderboard.neighborhood == neighborhood
    ).order_by(NeighborhoodLeaderboard.rank).limit(limit).all()
    
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

@router.get("/top-performers")
def get_top_performers(db: Session = Depends(get_db)):
    """Get current top performers"""
    from app.models.leaderboards import TopPerformer
    
    performers = db.query(TopPerformer).all()
    return performers
