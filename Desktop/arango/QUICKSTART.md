# Quick Start Guide

## Start the Application

### Terminal 1 - Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend will run on: http://localhost:8000

### Terminal 2 - Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend will run on: http://localhost:5173

## Test the Application

1. **Open** http://localhost:5173 in your browser

2. **Try a Demo Scenario**:
   - Select "Dangerous Combo" from the dropdown
   - Click "Check Interactions"
   - See severe interactions displayed

3. **Search for Drugs**:
   - Type "warfarin" in the search box
   - Select "Warfarin" from results
   - Add more drugs
   - Check interactions

4. **View API Docs**:
   - Visit http://localhost:8000/docs
   - Test endpoints directly

## Verify Backend Connection

```bash
curl http://localhost:8000/api/health
```

Should return:
```json
{"status":"healthy","database":"connected"}
```

## Common Issues

**Backend won't start:**
- Check `.env` file exists in `backend/` directory
- Verify ArangoDB credentials are correct
- Ensure Python 3.11+ is installed

**Frontend can't connect:**
- Ensure backend is running on port 8000
- Check browser console for CORS errors
- Verify API_BASE_URL in `frontend/src/services/api.ts`

**No search results:**
- Verify database connection in backend logs
- Check ArangoDB is accessible
- Test with: `curl "http://localhost:8000/api/drugs?search=warfarin"`

