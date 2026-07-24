# 🚀 Deploy TerraFlux to Render.com

## Step 1: Prepare Your Repository

Your repo is already prepared! ✅

## Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repositories

## Step 3: Create a Web Service

1. Click **"New +"** → Select **"Web Service"**
2. Connect your GitHub repository: `dc2401028-spec/terraflux`
3. Fill in these details:

   - **Name:** `terraflux-api`
   - **Environment:** Python 3
   - **Region:** Choose closest to you
   - **Branch:** main
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `cd backend && gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`

## Step 4: Set Environment Variables

In Render dashboard:

1. Go to **Environment** section
2. Add these variables:

   ```
   APP_ENV=production
   DEBUG=False
   SECRET_KEY=your-super-secret-key-min-32-chars-12345678901234567890
   DATABASE_URL=postgresql://username:password@host:5432/terraflux
   ```

3. For DATABASE_URL, you need a PostgreSQL database:
   - Create a PostgreSQL instance on Render
   - Copy the connection string
   - Paste as DATABASE_URL

## Step 5: Add PostgreSQL Database (FREE)

1. In Render dashboard: **New +** → **PostgreSQL**
2. Fill in:
   - **Name:** `terraflux-db`
   - **Database:** `terraflux`
   - **Region:** Same as your web service
   - **PostgreSQL Version:** 15

3. Once created, copy the **External Database URL**
4. Add it as `DATABASE_URL` environment variable

## Step 6: Deploy!

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repo
   - Install dependencies
   - Run build commands
   - Start your server

3. Wait 3-5 minutes for deployment
4. You'll get a live URL like: `https://terraflux-api.onrender.com`

## Step 7: Test Your Deployment

### Check Health
```bash
https://terraflux-api.onrender.com/health
```

### Access API Docs
```bash
https://terraflux-api.onrender.com/docs
```

### Test Registration
```bash
curl -X POST https://terraflux-api.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

## ✨ Your App is Live!

Share this URL with anyone:
```
https://terraflux-api.onrender.com
```

They can:
- 📖 View API docs: `/docs`
- 🔑 Register & login
- 🌿 Log eco-actions
- 🎮 Check leaderboards
- 💬 Use community features

## 🔄 Auto-Deploy on Git Push

Render automatically redeploys when you push to `main` branch!

Just push your changes:
```bash
git add .
git commit -m "Update TerraFlux"
git push origin main
```

Render will automatically rebuild and deploy! 🚀

## 📊 Monitor Your App

In Render Dashboard:
- View logs in real-time
- Monitor resource usage
- Set up alerts
- View analytics

## 🆘 Troubleshooting

### App not starting?
- Check logs in Render dashboard
- Verify all environment variables are set
- Make sure PostgreSQL database is running

### Database connection error?
- Verify DATABASE_URL format
- Check PostgreSQL is running on Render
- Ensure network access is allowed

### Need to update?
- Just push to GitHub
- Render auto-deploys in 2-5 minutes

---

**Your TerraFlux API is now live and accessible to everyone! 🌱🚀**
