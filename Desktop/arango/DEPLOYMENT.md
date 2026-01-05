# Deployment Guide - Cloudflare Pages

This guide will help you deploy the Drug Interaction Checker application to Cloudflare Pages.

## Architecture

- **Frontend**: React/Vite app → Cloudflare Pages
- **Backend**: FastAPI → Deploy separately (Railway, Render, Fly.io, or similar)

## Prerequisites

1. Cloudflare account (free tier works)
2. Git repository (GitHub, GitLab, or Bitbucket)
3. Backend deployment (see Backend Deployment section)

---

## Step 1: Deploy Backend

The FastAPI backend needs to be deployed separately. Here are recommended options:

### Option A: Railway (Recommended - Easy)

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Set root directory to `backend`
6. Add environment variables:
   ```
   ARANGO_HOST=your_arangodb_host
   ARANGO_DB=your_database_name
   ARANGO_USER=your_username
   ARANGO_PASSWORD=your_password
   ```
7. Railway will auto-detect Python and install dependencies
8. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
9. Copy the deployment URL (e.g., `https://your-app.railway.app`)

### Option B: Render

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repo
4. Set:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy and copy URL

### Option C: Fly.io

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. In `backend/` directory: `fly launch`
3. Follow prompts
4. Add secrets: `fly secrets set ARANGO_HOST=... ARANGO_DB=... etc.`
5. Deploy: `fly deploy`

---

## Step 2: Update Frontend API URL

1. Update `frontend/.env.production` with your backend URL:
   ```env
   VITE_API_BASE_URL=https://your-backend-url.com/api
   ```

2. Or set it in Cloudflare Pages environment variables (see Step 3)

---

## Step 3: Deploy Frontend to Cloudflare Pages

### Method 1: Via Cloudflare Dashboard (Recommended)

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Go to Cloudflare Dashboard**
   - Visit [dash.cloudflare.com](https://dash.cloudflare.com)
   - Go to "Workers & Pages" → "Create application" → "Pages" → "Connect to Git"

3. **Connect Repository**
   - Select your Git provider (GitHub/GitLab/Bitbucket)
   - Authorize Cloudflare
   - Select your repository

4. **Configure Build Settings**
   - **Project name**: `drug-interaction-checker` (or your choice)
   - **Production branch**: `main` (or `master`)
   - **Build command**: `cd frontend && npm install && npm run build`
   - **Build output directory**: `frontend/dist`

5. **Add Environment Variables**
   - Go to Settings → Environment Variables
   - Add:
     ```
     VITE_API_BASE_URL = https://your-backend-url.com/api
     ```
   - Make sure it's set for "Production"

6. **Deploy**
   - Click "Save and Deploy"
   - Cloudflare will build and deploy your site
   - You'll get a URL like: `https://your-app.pages.dev`

### Method 2: Via Wrangler CLI

1. **Install Wrangler**
   ```bash
   npm install -g wrangler
   ```

2. **Login**
   ```bash
   wrangler login
   ```

3. **Deploy**
   ```bash
   cd frontend
   npm run build
   wrangler pages deploy dist --project-name=drug-interaction-checker
   ```

---

## Step 4: Update CORS Settings

Update your backend CORS configuration to allow your Cloudflare Pages domain:

**File**: `backend/app/config.py`

```python
CORS_ORIGINS: list = [
    "http://localhost:5173",
    "http://localhost:5174",
    "https://your-app.pages.dev",  # Add your Cloudflare Pages URL
    "https://your-custom-domain.com"  # If you add a custom domain
]
```

Redeploy your backend after this change.

---

## Step 5: Custom Domain (Optional)

1. In Cloudflare Pages dashboard, go to your project
2. Click "Custom domains"
3. Add your domain
4. Follow DNS setup instructions
5. Cloudflare will automatically configure SSL

---

## Environment Variables Summary

### Frontend (Cloudflare Pages)
- `VITE_API_BASE_URL` - Your backend API URL

### Backend (Railway/Render/Fly.io)
- `ARANGO_HOST` - ArangoDB host URL
- `ARANGO_DB` - Database name
- `ARANGO_USER` - Database username
- `ARANGO_PASSWORD` - Database password

---

## Testing Deployment

1. Visit your Cloudflare Pages URL
2. Open browser console (F12)
3. Check for any CORS errors
4. Test the application:
   - Select a demo scenario
   - Add medications
   - Check interactions
   - Test condition warnings

---

## Troubleshooting

### CORS Errors
- Make sure backend CORS includes your Cloudflare Pages URL
- Check backend logs for CORS-related errors

### API Not Found (404)
- Verify `VITE_API_BASE_URL` is set correctly
- Check backend is running and accessible
- Test backend URL directly: `https://your-backend.com/api/health`

### Build Failures
- Check build logs in Cloudflare Pages dashboard
- Ensure `frontend/package.json` has correct build script
- Verify Node.js version (Cloudflare uses Node 18+ by default)

### Environment Variables Not Working
- Make sure variables start with `VITE_` prefix
- Rebuild after adding environment variables
- Check variable names match exactly (case-sensitive)

---

## Quick Deploy Checklist

- [ ] Backend deployed and accessible
- [ ] Backend CORS updated with frontend URL
- [ ] Frontend `.env.production` updated (or Cloudflare env vars set)
- [ ] Code pushed to Git repository
- [ ] Cloudflare Pages project created
- [ ] Build settings configured correctly
- [ ] Environment variables added
- [ ] Site deployed and tested

---

## Cost

- **Cloudflare Pages**: Free (unlimited requests, 500 builds/month)
- **Railway**: Free tier available, then pay-as-you-go
- **Render**: Free tier available (spins down after inactivity)
- **Fly.io**: Free tier available

---

## Support

If you encounter issues:
1. Check Cloudflare Pages build logs
2. Check backend deployment logs
3. Verify environment variables are set correctly
4. Test API endpoints directly with curl/Postman

