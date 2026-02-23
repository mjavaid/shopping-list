# Shopping List

Angular frontend + FastAPI backend packaged as a **single container**.

## Endpoints
- `GET /api/health` -> health check

## Development

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
The Angular 17 app is located in `frontend/` (routing enabled, SCSS styling).

```bash
cd frontend
npm install
npm start
```

## Single-container build (recommended)

The Docker image builds the Angular app and copies the built assets into the FastAPI app's `static/` directory.

```bash
docker build -t shopping-list .
docker run --rm -p 8080:80 shopping-list
```

Open:
- http://localhost:8080/
- http://localhost:8080/api/health
