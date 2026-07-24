"""TerraFlux Backend - Application Entry Point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.config import settings
from app.database import engine, Base
from app.routes import auth, users, eco_actions, gamification, community, leaderboards

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Eco-habit tracking and gamification platform",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Add CORS middleware - Allow all origins for now (change in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Mount static files for uploads
try:
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
except Exception as e:
    print(f"Warning: Could not mount uploads directory: {e}")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(eco_actions.router, prefix="/api/eco-actions", tags=["Eco-Actions"])
app.include_router(gamification.router, prefix="/api/gamification", tags=["Gamification"])
app.include_router(community.router, prefix="/api/community", tags=["Community"])
app.include_router(leaderboards.router, prefix="/api/leaderboards", tags=["Leaderboards"])

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to TerraFlux API",
        "docs": "/docs",
        "version": "0.1.0",
        "status": "🌱 Running"
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "app": "TerraFlux"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
