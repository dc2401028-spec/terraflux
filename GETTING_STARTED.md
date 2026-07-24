# 🚀 TerraFlux - Getting Started Guide

Welcome to TerraFlux! This guide will help you set up and run the project locally.

## ✅ Prerequisites

Before you start, make sure you have:
- **Python 3.10 or higher** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/)
- **pip** - Usually comes with Python
- **A code editor** - VS Code, PyCharm, etc.

## 📦 Step 1: Clone and Setup

### 1.1 Clone the repository
```bash
git clone https://github.com/dc2401028-spec/terraflux.git
cd terraflux
```

### 1.2 Create a Python virtual environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 1.3 Install dependencies
```bash
pip install -r requirements.txt
```

## ⚙️ Step 2: Configure Environment

### 2.1 Create .env file
```bash
cp .env.example .env
```

### 2.2 Edit .env file
Open `.env` and update these values:
```env
# Database (SQLite for development, PostgreSQL for production)
DATABASE_URL=sqlite:///./terraflux.db

# JWT Secret - Change this to a random string
SECRET_KEY=your-super-secret-key-change-this-12345

# Other settings
APP_ENV=development
DEBUG=True
```

**⚠️ Important:** Never commit `.env` file with real secrets!

## 🗄️ Step 3: Initialize Database

```bash
# Navigate to backend directory
cd backend

# Create database and tables
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

## 🎯 Step 4: Run the Server

```bash
# Make sure you're in the backend directory
cd backend

# Start the development server
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
```

## 📚 Step 5: Access the API

### API Documentation
- **Swagger UI (Interactive)**: http://localhost:8000/docs
- **ReDoc (Read-only)**: http://localhost:8000/redoc

### Test Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "healthy"}
```

## 🧪 Step 6: Test Authentication

### 1. Register a new user
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

Response:
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "total_points": 0,
  "level": 1,
  "coins": 0,
  ...
}
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "testuser"
}
```

### 3. Get current user profile
```bash
curl -X GET "http://localhost:8000/api/auth/me?token=YOUR_ACCESS_TOKEN"
```

## 🌿 Step 7: Log Your First Eco-Action

```bash
curl -X POST "http://localhost:8000/api/eco-actions/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "action_type": "recycling",
    "title": "Recycled Plastic Bottles",
    "description": "Recycled 5 plastic bottles today",
    "location": "Home"
  }'
```

Response:
```json
{
  "id": 1,
  "user_id": 1,
  "action_type": "recycling",
  "title": "Recycled Plastic Bottles",
  "points_earned": 10,
  "xp_earned": 5,
  "coins_earned": 2,
  "verification_status": "pending",
  ...
}
```

## 🎮 Step 8: Check Your Stats

```bash
curl -X GET "http://localhost:8000/api/gamification/stats/1"
```

## 🏆 Step 9: View Leaderboards

```bash
# Global leaderboard
curl -X GET "http://localhost:8000/api/leaderboards/global?limit=10"

# City leaderboard
curl -X GET "http://localhost:8000/api/leaderboards/city/New%20York?limit=10"
```

## 📁 Project Structure

```
terraflux/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Settings & config
│   │   ├── database.py          # Database setup
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── users.py
│   │   │   ├── eco_actions.py
│   │   │   ├── gamification.py
│   │   │   ├── community.py
│   │   │   └── leaderboards.py
│   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── auth.py
│   │   │   ├── eco_actions.py
│   │   │   ├── gamification.py
│   │   │   └── community.py
│   │   ├── routes/              # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── eco_actions.py
│   │   │   ├── gamification.py
│   │   │   ├── community.py
│   │   │   └── leaderboards.py
│   │   └── services/            # Business logic
│   │       ├── auth_service.py
│   │       ├── eco_action_service.py
│   │       ├── gamification_service.py
│   │       └── community_service.py
│   ├── requirements.txt
│   └── .env.example
├── .gitignore
├── README.md
└── GETTING_STARTED.md
```

## 🔌 API Endpoints Overview

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Users
- `GET /api/users/profile/{user_id}` - Get user profile
- `PUT /api/users/profile` - Update profile
- `GET /api/users/search?query=...` - Search users

### Eco-Actions
- `POST /api/eco-actions/` - Log new eco-action
- `GET /api/eco-actions/` - Get my actions
- `GET /api/eco-actions/challenges/active` - Get challenges
- `POST /api/eco-actions/{action_id}/upload-photo` - Upload proof photo

### Gamification
- `GET /api/gamification/stats/{user_id}` - Get user stats
- `GET /api/gamification/streak/{user_id}` - Get streak info
- `GET /api/gamification/achievements/{user_id}` - Get achievements
- `GET /api/gamification/leaderboard/global` - Global rankings
- `GET /api/gamification/shop` - Coin shop items
- `POST /api/gamification/shop/purchase/{item_id}` - Buy item

### Community (Eco-Tok)
- `POST /api/community/posts` - Create post
- `GET /api/community/feed` - Get feed
- `POST /api/community/posts/{post_id}/comments` - Comment on post
- `POST /api/community/posts/{post_id}/like` - Like post
- `POST /api/community/follow/{user_id}` - Follow user

### Leaderboards
- `GET /api/leaderboards/global` - Global leaderboard
- `GET /api/leaderboards/city/{city}` - City leaderboard
- `GET /api/leaderboards/neighborhood/{neighborhood}` - Neighborhood leaderboard

## 🐛 Troubleshooting

### Port 8000 already in use
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

### Database errors
```bash
# Reset database (delete .db file)
rm terraflux.db

# Recreate tables
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Virtual environment issues
```bash
# Deactivate current venv
deactivate

# Remove venv and create fresh one
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📖 Next Steps

1. **Explore the API** - Use Swagger UI at `/docs`
2. **Read the README** - Check `README.md` for full feature overview
3. **Set up Frontend** - Create a React/Vue app to consume this API
4. **Add Database Seeding** - Create sample data for development
5. **Configure Production** - Use PostgreSQL and proper secrets management

## 🚀 Ready to Deploy?

When you're ready to deploy to production:

1. **Update .env**
   ```env
   APP_ENV=production
   DEBUG=False
   DATABASE_URL=postgresql://user:password@host:5432/terraflux
   SECRET_KEY=generate-a-new-random-secret-key
   ```

2. **Use production server** (not uvicorn with reload)
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
   ```

3. **Set up database migrations** with Alembic
4. **Configure CORS** for your frontend domain
5. **Enable HTTPS/SSL** certificates

## 💬 Need Help?

- Check existing issues: https://github.com/dc2401028-spec/terraflux/issues
- Read the API docs: http://localhost:8000/docs
- Check logs for error messages

---

**Happy eco-tracking! 🌱**
