# Shopping List

Angular frontend + FastAPI backend packaged as a **single container**.

## Endpoints
- `GET /api/health` → health check
- `POST /api/lists` → create a shopping list
- `GET /api/lists` → list all shopping lists
- `POST /api/lists/{list_id}/items` → add item to a list
- `GET /api/lists/{list_id}/items` → list items for a list
- `PATCH /api/items/{item_id}` → update an item (name, quantity, checked)
- `DELETE /api/items/{item_id}` → delete an item

## Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run database migrations (creates ./data/app.db)
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

### Frontend
Create the Angular app in `frontend/` (or use `ng new frontend`).

```bash
cd frontend
npm install
npm start
```

## Single-container build (recommended)

The Docker image builds the Angular app and copies the built assets into the FastAPI app's `static/` directory.

```bash
docker build -t shopping-list .

# Run without persistence (data lost on container restart)
docker run --rm -p 8080:80 shopping-list

# Run with persistent data volume
docker run --rm -p 8080:80 -v shopping-list-data:/app/data shopping-list
```

Open:
- http://localhost:8080/
- http://localhost:8080/api/health

## Database

The app uses SQLite stored at `./data/app.db` (relative to the working directory).
Migrations are managed with [Alembic](https://alembic.sqlalchemy.org/).

```bash
# Apply all migrations
cd backend
alembic upgrade head

# Create a new migration after model changes
alembic revision --autogenerate -m "describe change"
```

