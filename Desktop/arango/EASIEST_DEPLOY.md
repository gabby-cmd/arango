# 🚀 Easiest Deployment - Railway (All-in-One)

Railway can deploy BOTH frontend and backend in one project. This is the simplest approach!

## Step 1: Deploy Everything to Railway

1. **Go to [railway.app](https://railway.app)** and sign up with GitHub

2. **Create New Project** → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect both services

3. **Add Backend Service:**
   - Railway should auto-detect the `backend/` folder
   - If not, click "New" → "GitHub Repo" → Select `backend/` as root
   - Add environment variables:
     ```
     ARANGO_HOST=your_arangodb_host
     ARANGO_DB=your_database_name
     ARANGO_USER=your_username
     ARANGO_PASSWORD=your_password
     ```
   - Railway will auto-detect Python and run it
   - Get the backend URL (e.g., `https://backend-production.up.railway.app`)

4. **Add Frontend Service:**
   - Click "New" → "GitHub Repo" → Select `frontend/` as root
   - Add environment variable:
     ```
     VITE_API_BASE_URL=https://your-backend-url.up.railway.app/api
     ```
   - Railway will auto-detect Node.js and build
   - Railway will give you a frontend URL

5. **Update Backend CORS:**
   - In `backend/app/config.py`, add your Railway frontend URL to CORS_ORIGINS
   - Or set environment variable: `CORS_ORIGINS=https://your-frontend.up.railway.app`

6. **Done!** Both services are live on Railway with automatic HTTPS and domains.

---

## Alternative: Vercel (Even Easier for Frontend)

### Frontend on Vercel + Backend on Railway

**Frontend (Vercel):**
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repo
3. Set root directory: `frontend`
4. Build command: `npm run build`
5. Output directory: `dist`
6. Environment variable: `VITE_API_BASE_URL=https://your-railway-backend.com/api`
7. Deploy!

**Backend (Railway):**
- Follow Step 1-3 above (just backend)

Vercel is specifically optimized for frontend deployments and has the best DX.

---

## Alternative: Render (Free Tier Friendly)

**Both on Render:**
1. Go to [render.com](https://render.com)
2. Create two services from the same repo:

   **Backend Service:**
   - Type: Web Service
   - Root: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add env vars

   **Frontend Service:**
   - Type: Static Site
   - Root: `frontend`
   - Build: `npm install && npm run build`
   - Publish: `dist`
   - Add env var: `VITE_API_BASE_URL`

---

## 🎯 Recommendation

**Railway** is the easiest for beginners:
- ✅ One platform for everything
- ✅ Auto-detects everything
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Simple environment variables

**Vercel + Railway** is best for production:
- ✅ Vercel = best frontend hosting (fastest CDN)
- ✅ Railway = simple backend hosting
- ✅ Both have great free tiers

Choose whichever feels easier to you!

