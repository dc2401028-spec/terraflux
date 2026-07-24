"""Community Routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.community import PostCreate, PostResponse, CommentCreate, CommentResponse, VerifiedLoggerResponse
from app.services.community_service import (
    create_post, get_feed, create_comment, like_post, unlike_post,
    follow_user, unfollow_user, get_user_followers, get_user_following,
    mark_as_verified_logger, get_verified_loggers
)
from app.services.auth_service import verify_token
from app.models.users import User
from app.models.community import Post, Comment

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

@router.post("/posts", response_model=PostResponse)
def create_new_post(
    post: PostCreate,
    token: str,
    db: Session = Depends(get_db)
):
    """Create a new post"""
    user = get_current_user(token, db)
    
    new_post = create_post(db, user.id, post.content, post.image_url, post.is_verified)
    
    return {
        "id": new_post.id,
        "author_id": new_post.author_id,
        "author_username": user.username,
        "content": new_post.content,
        "image_url": new_post.image_url,
        "likes_count": new_post.likes_count,
        "comments_count": new_post.comments_count,
        "is_verified": new_post.is_verified,
        "created_at": new_post.created_at
    }

@router.get("/feed", response_model=List[PostResponse])
def get_user_feed(
    skip: int = 0,
    limit: int = 20,
    token: str = Depends(lambda t: t),
    db: Session = Depends(get_db)
):
    """Get user's feed"""
    user = get_current_user(token, db)
    
    posts = get_feed(db, user.id, skip, limit)
    
    result = []
    for post in posts:
        result.append({
            "id": post.id,
            "author_id": post.author_id,
            "author_username": post.author.username,
            "content": post.content,
            "image_url": post.image_url,
            "likes_count": post.likes_count,
            "comments_count": post.comments_count,
            "is_verified": post.is_verified,
            "created_at": post.created_at
        })
    
    return result

@router.post("/posts/{post_id}/comments", response_model=CommentResponse)
def add_comment(
    post_id: int,
    comment: CommentCreate,
    token: str,
    db: Session = Depends(get_db)
):
    """Add a comment to a post"""
    user = get_current_user(token, db)
    
    new_comment = create_comment(db, post_id, user.id, comment.content)
    if not new_comment:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {
        "id": new_comment.id,
        "post_id": new_comment.post_id,
        "author_id": new_comment.author_id,
        "author_username": user.username,
        "content": new_comment.content,
        "likes_count": new_comment.likes_count,
        "created_at": new_comment.created_at
    }

@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    """Get comments on a post"""
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    
    result = []
    for comment in comments:
        result.append({
            "id": comment.id,
            "post_id": comment.post_id,
            "author_id": comment.author_id,
            "author_username": comment.author.username,
            "content": comment.content,
            "likes_count": comment.likes_count,
            "created_at": comment.created_at
        })
    
    return result

@router.post("/posts/{post_id}/like")
def like_post_endpoint(
    post_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    """Like a post"""
    user = get_current_user(token, db)
    
    if not like_post(db, post_id, user.id):
        raise HTTPException(status_code=400, detail="Cannot like post")
    
    return {"message": "Post liked"}

@router.post("/posts/{post_id}/unlike")
def unlike_post_endpoint(
    post_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    """Unlike a post"""
    user = get_current_user(token, db)
    
    if not unlike_post(db, post_id, user.id):
        raise HTTPException(status_code=400, detail="Cannot unlike post")
    
    return {"message": "Post unliked"}

@router.post("/follow/{user_id}")
def follow_user_endpoint(
    user_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    """Follow a user"""
    user = get_current_user(token, db)
    
    if not follow_user(db, user.id, user_id):
        raise HTTPException(status_code=400, detail="Cannot follow user")
    
    return {"message": "User followed"}

@router.post("/unfollow/{user_id}")
def unfollow_user_endpoint(
    user_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    """Unfollow a user"""
    user = get_current_user(token, db)
    
    if not unfollow_user(db, user.id, user_id):
        raise HTTPException(status_code=400, detail="Cannot unfollow user")
    
    return {"message": "User unfollowed"}

@router.get("/followers/{user_id}")
def get_followers(user_id: int, db: Session = Depends(get_db)):
    """Get user's followers"""
    followers = get_user_followers(db, user_id)
    return followers

@router.get("/following/{user_id}")
def get_following(user_id: int, db: Session = Depends(get_db)):
    """Get users that a user is following"""
    following = get_user_following(db, user_id)
    return following

@router.get("/verified-loggers", response_model=List[VerifiedLoggerResponse])
def get_verified_logger_list(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Get verified loggers"""
    verified_loggers = get_verified_loggers(db, skip, limit)
    return verified_loggers
