# Quick Deploy Guide - Cloudflare Pages

## 🚀 Fastest Way to Deploy

### 1. Deploy Backend (Choose One)

**Option A: Railway (Easiest)**
```bash
# 1. Go to railway.app and sign up
# 2. New Project → Deploy from GitHub
# 3. Select repo, set root: backend
# 4. Add env vars:
#    ARANGO_HOST=your_host
#    ARANGO_DB=your_db
#    ARANGO_USER=your_user
#    ARANGO_PASSWORD=your_password
# 5. Copy deployment URL (e.g., https://app.railway.app)
```

**Option B: Render**
```bash
# 1. Go to render.com
# 2. New Web Service → Connect GitHub
# 3. Root: backend
# 4. Build: pip install -r requirements.txt
# 5. Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
# 6. Add env vars and deploy
```

### 2. Update Backend CORS

Edit `backend/app/config.py` and add your Cloudflare Pages URL to CORS_ORIGINS, or set:
```bash
CORS_ORIGINS=https://your-app.pages.dev,https://your-custom-domain.com
```

### 3. Deploy Frontend to Cloudflare Pages

**Via Dashboard:**
1. Go to [dash.cloudflare.com](https://dash.cloudflare.com)
2. Workers & Pages → Create → Pages → Connect to Git
3. Select your repository
4. Build settings:
   - Build command: `cd frontend && npm install && npm run build`
   - Build output: `frontend/dist`
5. Environment variables:
   - `VITE_API_BASE_URL` = `https://your-backend-url.com/api`
6. Deploy!

**Your site will be live at:** `https://your-project.pages.dev`

### 4. Test

Visit your Cloudflare Pages URL and test the app!

## 📝 Important Notes

- Backend must be deployed first
- Update CORS in backend to allow Cloudflare domain
- Set `VITE_API_BASE_URL` environment variable in Cloudflare Pages
- The `_redirects` file ensures SPA routing works

## 🔧 Troubleshooting

**CORS Error?**
- Add Cloudflare Pages URL to backend CORS_ORIGINS

**API 404?**
- Check `VITE_API_BASE_URL` is set correctly
- Verify backend is running

**Build Fails?**
- Check build logs in Cloudflare dashboard
- Ensure Node.js version is 18+
