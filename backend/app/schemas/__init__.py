"""Initialize schemas package"""
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserResponse, AvatarUpdate
from app.schemas.eco_actions import EcoActionCreate, EcoActionResponse, ChallengeResponse
from app.schemas.gamification import UserStatsResponse, AchievementResponse, LeaderboardEntryResponse, StreakInfoResponse
from app.schemas.community import PostCreate, PostResponse, CommentCreate, CommentResponse, VerifiedLoggerResponse

__all__ = [
    "UserRegister", "UserLogin", "TokenResponse", "UserResponse", "AvatarUpdate",
    "EcoActionCreate", "EcoActionResponse", "ChallengeResponse",
    "UserStatsResponse", "AchievementResponse", "LeaderboardEntryResponse", "StreakInfoResponse",
    "PostCreate", "PostResponse", "CommentCreate", "CommentResponse", "VerifiedLoggerResponse"
]
