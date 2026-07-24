"""Gamification Services"""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.users import User
from app.models.gamification import UserStats, Achievement, UserAchievement, StreakRecord, CoinShop, UserInventory
from app.models.leaderboards import Leaderboard
from typing import List, Optional

def get_user_stats(db: Session, user_id: int) -> Optional[UserStats]:
    """Get user statistics"""
    return db.query(UserStats).filter(UserStats.user_id == user_id).first()

def get_user_achievements(db: Session, user_id: int) -> List[UserAchievement]:
    """Get all achievements earned by user"""
    return db.query(UserAchievement).filter(UserAchievement.user_id == user_id).all()

def award_achievement(db: Session, user_id: int, achievement_id: int):
    """Award an achievement to a user"""
    existing = db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id,
        UserAchievement.achievement_id == achievement_id
    ).first()
    
    if not existing:
        achievement = db.query(Achievement).filter(Achievement.id == achievement_id).first()
        user_achievement = UserAchievement(user_id=user_id, achievement_id=achievement_id)
        db.add(user_achievement)
        
        # Award bonus coins
        if achievement:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.coins += achievement.reward_coins
        
        db.commit()

def get_streak_info(db: Session, user_id: int) -> Optional[StreakRecord]:
    """Get user's streak information"""
    return db.query(StreakRecord).filter(StreakRecord.user_id == user_id).first()

def get_leaderboard_global(db: Session, limit: int = 100) -> List:
    """Get global leaderboard"""
    return db.query(User).order_by(User.total_points.desc()).limit(limit).all()

def get_leaderboard_city(db: Session, city: str, limit: int = 100) -> List:
    """Get leaderboard for a specific city"""
    return db.query(Leaderboard).filter(
        Leaderboard.rank_city == city
    ).order_by(Leaderboard.total_points.desc()).limit(limit).all()

def get_leaderboard_neighborhood(db: Session, neighborhood: str, limit: int = 100) -> List:
    """Get leaderboard for a specific neighborhood"""
    return db.query(Leaderboard).filter(
        Leaderboard.rank_neighborhood == neighborhood
    ).order_by(Leaderboard.total_points.desc()).limit(limit).all()

def get_coin_shop_items(db: Session, item_type: Optional[str] = None, skip: int = 0, limit: int = 20) -> List[CoinShop]:
    """Get items available in coin shop"""
    query = db.query(CoinShop).filter(CoinShop.is_available == True)
    if item_type:
        query = query.filter(CoinShop.item_type == item_type)
    return query.offset(skip).limit(limit).all()

def purchase_item(db: Session, user_id: int, item_id: int) -> bool:
    """Purchase an item from coin shop"""
    user = db.query(User).filter(User.id == user_id).first()
    item = db.query(CoinShop).filter(CoinShop.id == item_id).first()
    
    if not user or not item:
        return False
    
    if user.coins < item.cost_coins:
        return False
    
    # Deduct coins
    user.coins -= item.cost_coins
    
    # Add to inventory
    inventory = UserInventory(user_id=user_id, item_id=item_id)
    db.add(inventory)
    db.commit()
    
    return True

def equip_item(db: Session, user_id: int, inventory_id: int) -> bool:
    """Equip an item from inventory"""
    inventory = db.query(UserInventory).filter(
        UserInventory.id == inventory_id,
        UserInventory.user_id == user_id
    ).first()
    
    if not inventory:
        return False
    
    inventory.is_equipped = True
    db.commit()
    return True
