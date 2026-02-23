from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title='Shopping List')

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / 'static'
INDEX_FILE = STATIC_DIR / 'index.html'

@app.get('/api/health')
def health():
    return {'status': 'ok'}

# Serve built Angular assets (copied into app/static at build time)
if STATIC_DIR.exists():
    app.mount('/', StaticFiles(directory=str(STATIC_DIR), html=True), name='static')

# SPA fallback for client-side routes
@app.get('/{full_path:path}')
def spa_fallback(full_path: str):
    if INDEX_FILE.exists():
        return FileResponse(str(INDEX_FILE))
    return JSONResponse(
        status_code=404,
        content={
            'detail': 'Frontend not built. Build the Docker image or run Angular dev server.'
        },
    )
