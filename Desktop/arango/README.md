# Drug Interaction Checker

A professional medication safety analysis tool built with FastAPI and React, powered by ArangoDB graph database.

## Features

- **Drug Search**: Search and select medications from a comprehensive database
- **Interaction Detection**: Analyze potential drug interactions using graph traversal
- **Severity Classification**: Categorize interactions as severe, moderate, or minor
- **Clinical Information**: Detailed mechanism, management, and evidence for each interaction
- **Demo Scenarios**: Pre-configured test cases for demonstration
- **Performance Optimized**: Sub-100ms query times for interaction detection

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **ArangoDB** - Graph database for relationship queries
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Lucide React** - Icons

## Project Structure

```
drug-interaction-checker/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py             # Configuration
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic models
│   │   ├── services/
│   │   │   ├── arango_service.py      # DB connection
│   │   │   └── interaction_service.py  # Business logic
│   │   └── routes/
│   │       └── api.py            # API endpoints
│   ├── .env                      # Environment variables
│   └── requirements.txt          # Python dependencies
│
└── frontend/
    ├── src/
    │   ├── components/           # React components
    │   ├── services/             # API client
    │   ├── types/                # TypeScript types
    │   └── App.tsx               # Main app
    └── package.json
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- ArangoDB Cloud account (or local instance)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the `backend/` directory:
   ```env
   ARANGO_HOST=https://d8c1701e2a10.arangodb.cloud:8529
   ARANGO_DB=drug_interation_db
   ARANGO_USER=root
   ARANGO_PASSWORD=your_password
   ```

5. **Run the backend server**
   ```bash
   uvicorn app.main:app --reload
   ```
   
   The API will be available at `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/api/health`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   
   The app will be available at `http://localhost:5173`

## API Endpoints

### `GET /api/health`
Health check endpoint
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### `GET /api/drugs?search={query}&limit=20`
Search for drugs by name
```json
[
  {
    "_key": "warfarin_5mg",
    "name": "Warfarin",
    "generic_name": "Warfarin Sodium",
    "brand_names": ["Coumadin"],
    "strength": "5mg",
    "drug_class": "anticoagulant"
  }
]
```

### `POST /api/check-interactions`
Check for interactions between drugs
```json
Request:
{
  "drug_keys": ["warfarin_5mg", "aspirin_325mg"]
}

Response:
{
  "interactions_found": 2,
  "highest_severity": "severe",
  "query_time_ms": 45.2,
  "interactions": [...]
}
```

### `GET /api/stats`
Get database statistics
```json
{
  "total_drugs": 24,
  "total_compounds": 23,
  "total_interactions": 23,
  "interactions_by_severity": {
    "severe": 7,
    "moderate": 11,
    "minor": 5
  }
}
```

## Demo Scenarios

The application includes 4 pre-configured demo scenarios:

1. **Safe Combination**: Lisinopril, Metformin, Atorvastatin (0-1 minor interactions)
2. **Dangerous Combo**: Warfarin + Aspirin + Ibuprofen (3+ severe interactions)
3. **Moderate Risk**: Sertraline + Ibuprofen + Tramadol (2+ moderate/severe)
4. **Complex Polypharmacy**: 5 medications with multiple interactions

## Database

The application uses ArangoDB with the following structure:

- **Collections**:
  - `drugs` - Drug products (24 documents)
  - `compounds` - Active ingredients (23 documents)
  - `drug_contains_compound` - Edge collection linking drugs to compounds
  - `compound_interacts_with` - Edge collection for interactions

- **Graph**: `drug_interaction_graph`

The database is pre-populated with real-world drug interaction data.

## Development

### Backend Development
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Building for Production

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm run build
npm run preview
```

## Performance

- Interaction detection queries target <100ms execution time
- Optimized AQL queries with proper indexing
- Efficient graph traversal for pairwise interaction detection

## License

This project is for educational and demonstration purposes only.

## Disclaimer

**This tool is for educational purposes only. Always consult a healthcare provider before making medication changes.**

