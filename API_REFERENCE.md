# 📖 TerraFlux API Quick Reference

## 🔑 Authentication Header

All endpoints (except `/auth/register` and `/auth/login`) require this header:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Or pass token as query parameter:
```
?token=YOUR_ACCESS_TOKEN
```

---

## 👤 Authentication Endpoints

### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "ecowarrior",
  "email": "user@example.com",
  "password": "secure123",
  "full_name": "Jane Doe"
}
```

**Response (201):**
```json
{
  "id": 1,
  "username": "ecowarrior",
  "email": "user@example.com",
  "full_name": "Jane Doe",
  "bio": null,
  "location": null,
  "total_points": 0,
  "total_xp": 0,
  "coins": 0,
  "level": 1,
  "current_streak": 0,
  "is_verified": false
}
```

### Login User
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "ecowarrior"
}
```

### Get Current User
```http
GET /api/auth/me?token=YOUR_TOKEN
```

---

## 👥 User Profile Endpoints

### Get User Profile
```http
GET /api/users/profile/{user_id}
```

### Get User by Username
```http
GET /api/users/profile/username/{username}
```

### Update Profile
```http
PUT /api/users/profile?token=YOUR_TOKEN
Content-Type: application/json

{
  "bio": "I love sustainability! 🌿",
  "location": "San Francisco, CA",
  "full_name": "Jane Doe"
}
```

### Search Users
```http
GET /api/users/search?query=eco&skip=0&limit=10
```

### Get/Update Avatar
```http
GET /api/users/avatar/{user_id}

PUT /api/users/avatar?token=YOUR_TOKEN
Content-Type: application/json

{
  "base_body": "athletic",
  "outfit": "eco_shirt",
  "accessories": "green_hat",
  "theme": "nature"
}
```

---

## 🌿 Eco-Action Endpoints

### Log New Eco-Action
```http
POST /api/eco-actions/?token=YOUR_TOKEN
Content-Type: application/json

{
  "action_type": "recycling",
  "title": "Recycled Electronics",
  "description": "Recycled old computer parts at e-waste center",
  "location": "Downtown Recycling Center"
}
```

**Action Types:**
- `recycling`
- `composting`
- `repair`
- `upcycling`
- `energy_saving`
- `water_conservation`
- `sustainable_shopping`
- `other`

**Response (201):**
```json
{
  "id": 1,
  "user_id": 1,
  "action_type": "recycling",
  "title": "Recycled Electronics",
  "description": "Recycled old computer parts at e-waste center",
  "photo_url": null,
  "verification_status": "pending",
  "points_earned": 10,
  "xp_earned": 5,
  "coins_earned": 2,
  "created_at": "2026-07-24T12:15:00"
}
```

### Upload Photo Proof
```http
POST /api/eco-actions/{action_id}/upload-photo?token=YOUR_TOKEN
Content-Type: multipart/form-data

file: [image.jpg]
```

### Get My Eco-Actions
```http
GET /api/eco-actions/?token=YOUR_TOKEN&skip=0&limit=10
```

### Get Specific Eco-Action
```http
GET /api/eco-actions/{action_id}
```

### Get User's Eco-Actions
```http
GET /api/eco-actions/user/{user_id}?skip=0&limit=10
```

### Get Active Challenges
```http
GET /api/eco-actions/challenges/active?skip=0&limit=10
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Recycling Champion",
    "description": "Recycle 10 items this week",
    "action_type": "recycling",
    "reward_points": 100,
    "reward_coins": 20,
    "difficulty": "medium",
    "icon_url": "https://..."
  }
]
```

### Complete Challenge
```http
POST /api/eco-actions/challenges/{challenge_id}/complete?token=YOUR_TOKEN
```

---

## 🎮 Gamification Endpoints

### Get User Statistics
```http
GET /api/gamification/stats/{user_id}
```

**Response:**
```json
{
  "user_id": 1,
  "total_actions": 5,
  "current_streak": 3,
  "longest_streak": 5,
  "level": 2,
  "xp_progress": 45,
  "total_xp": 145,
  "total_points": 65,
  "coins_balance": 12
}
```

### Get Streak Information
```http
GET /api/gamification/streak/{user_id}
```

**Response:**
```json
{
  "current_streak": 3,
  "longest_streak": 5,
  "last_action_date": "2026-07-24T10:30:00",
  "grace_days_remaining": 2
}
```

### Get User Achievements
```http
GET /api/gamification/achievements/{user_id}
```

### Get Global Leaderboard
```http
GET /api/gamification/leaderboard/global?limit=100
```

**Response:**
```json
[
  {
    "rank": 1,
    "username": "ecowarrior",
    "total_points": 500,
    "total_actions": 25,
    "level": 5,
    "avatar_url": "https://..."
  },
  {
    "rank": 2,
    "username": "greenthumb",
    "total_points": 450,
    "total_actions": 20,
    "level": 4,
    "avatar_url": "https://..."
  }
]
```

### Get City Leaderboard
```http
GET /api/gamification/leaderboard/city/San%20Francisco?limit=50
```

### Get Neighborhood Leaderboard
```http
GET /api/gamification/leaderboard/neighborhood/Marina%20District?limit=50
```

### Get Coin Shop
```http
GET /api/gamification/shop?item_type=outfit&skip=0&limit=20
```

**Item Types:** `outfit`, `accessory`, `theme`, etc.

### Purchase Shop Item
```http
POST /api/gamification/shop/purchase/{item_id}?token=YOUR_TOKEN
```

### Get Inventory
```http
GET /api/gamification/inventory?token=YOUR_TOKEN
```

### Equip Item
```http
POST /api/gamification/inventory/{inventory_id}/equip?token=YOUR_TOKEN
```

---

## 💬 Community (Eco-Tok) Endpoints

### Create Post
```http
POST /api/community/posts?token=YOUR_TOKEN
Content-Type: application/json

{
  "content": "Just completed my first eco-challenge! 🌱",
  "image_url": "https://example.com/photo.jpg",
  "is_verified": false
}
```

### Get Feed
```http
GET /api/community/feed?token=YOUR_TOKEN&skip=0&limit=20
```

### Add Comment
```http
POST /api/community/posts/{post_id}/comments?token=YOUR_TOKEN
Content-Type: application/json

{
  "content": "Great job! Keep it up! 👍"
}
```

### Get Post Comments
```http
GET /api/community/posts/{post_id}/comments
```

### Like Post
```http
POST /api/community/posts/{post_id}/like?token=YOUR_TOKEN
```

### Unlike Post
```http
POST /api/community/posts/{post_id}/unlike?token=YOUR_TOKEN
```

### Follow User
```http
POST /api/community/follow/{user_id}?token=YOUR_TOKEN
```

### Unfollow User
```http
POST /api/community/unfollow/{user_id}?token=YOUR_TOKEN
```

### Get User's Followers
```http
GET /api/community/followers/{user_id}
```

### Get Following List
```http
GET /api/community/following/{user_id}
```

### Get Verified Loggers
```http
GET /api/community/verified-loggers?skip=0&limit=20
```

**Response:**
```json
[
  {
    "user_id": 1,
    "username": "ecowarrior",
    "verified_actions_count": 50,
    "approval_rate": 95,
    "badge_url": "https://...",
    "verified_at": "2026-06-01T00:00:00"
  }
]
```

---

## 🏆 Leaderboard Endpoints

### Get Global Leaderboard
```http
GET /api/leaderboards/global?limit=100
```

### Get City Leaderboard
```http
GET /api/leaderboards/city/{city}?limit=100
```

### Get Neighborhood Leaderboard
```http
GET /api/leaderboards/neighborhood/{neighborhood}?limit=100
```

### Get Top Performers
```http
GET /api/leaderboards/top-performers
```

---

## ⚠️ Error Responses

### 400 Bad Request
```json
{
  "detail": "Username already taken"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid token"
}
```

### 404 Not Found
```json
{
  "detail": "User not found"
}
```

### 500 Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## 🧪 Testing with cURL

### Complete Workflow Example

```bash
# 1. Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","email":"demo@test.com","password":"pass123","full_name":"Demo User"}'

# 2. Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@test.com","password":"pass123"}'
# Copy the access_token

# 3. Log Eco-Action
curl -X POST http://localhost:8000/api/eco-actions/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -d '{"action_type":"recycling","title":"Recycled bottles","description":"10 plastic bottles"}'

# 4. Check Stats
curl -X GET http://localhost:8000/api/gamification/stats/1

# 5. View Leaderboard
curl -X GET http://localhost:8000/api/gamification/leaderboard/global
```

---

## 📱 Integration Tips

### For Frontend Developers

1. **Store Token Safely**
   - Use `localStorage` or `sessionStorage` (not `localStorage` for sensitive apps)
   - Include in Authorization header for all requests

2. **Refresh Token** (When implemented)
   - Implement token refresh endpoint for longer sessions
   - Handle 401 responses by re-authenticating

3. **Image Upload**
   - Use `FormData` for multipart requests
   - Validate file size before upload (max 5MB)

4. **Real-time Updates** (Future)
   - Consider WebSocket for live feed updates
   - Use polling for stats/leaderboards in MVP

---

**For more examples, visit:** http://localhost:8000/docs
