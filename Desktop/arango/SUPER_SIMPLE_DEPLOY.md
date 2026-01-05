# 🚀 Super Simple Deployment - Railway (3 Steps!)

## The Easiest Way Ever

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready to deploy"
git push origin main
```

### Step 2: Deploy on Railway
1. Go to **railway.app** → Sign up with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway will **automatically detect** both `backend/` and `frontend/` folders!

### Step 3: Add Environment Variables

**For Backend Service:**
- Click on the backend service
- Go to Variables tab
- Add:
  ```
  ARANGO_HOST=your_host
  ARANGO_DB=your_db
  ARANGO_USER=your_user
  ARANGO_PASSWORD=your_password
  ```

**For Frontend Service:**
- Click on the frontend service  
- Go to Variables tab
- Add:
  ```
  VITE_API_BASE_URL=https://your-backend-service.up.railway.app/api
  ```
  (Railway will show you the backend URL)

### Step 4: Update CORS (One Time)
- In `backend/app/config.py`, add your Railway frontend URL to CORS_ORIGINS
- Or set: `CORS_ORIGINS=https://your-frontend.up.railway.app`

### Done! 🎉

Both services are live with automatic HTTPS and custom domains!

---

## Why Railway is Easiest

✅ **One platform** - frontend + backend together  
✅ **Auto-detects** - no configuration needed  
✅ **Free tier** - $5 credit monthly  
✅ **Automatic HTTPS** - SSL certificates included  
✅ **Custom domains** - add your own domain easily  
✅ **Auto-deploys** - pushes to GitHub = auto deploy  

That's it! No complex setup, no separate services to manage.
