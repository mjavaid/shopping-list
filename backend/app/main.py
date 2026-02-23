from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import Base, Item, List
from .schemas import ItemCreate, ItemRead, ItemUpdate, ListCreate, ListRead

# Ensure tables exist at startup (idempotent; migrations are the authoritative path)
Base.metadata.create_all(bind=engine)

app = FastAPI(title='Shopping List')

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / 'static'
INDEX_FILE = STATIC_DIR / 'index.html'


# ── Health ────────────────────────────────────────────────────────────────────

@app.get('/api/health')
def health():
    return {'status': 'ok'}


# ── Lists ─────────────────────────────────────────────────────────────────────

@app.post('/api/lists', response_model=ListRead, status_code=201)
def create_list(body: ListCreate, db: Session = Depends(get_db)):
    obj = List(name=body.name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get('/api/lists', response_model=list[ListRead])
def get_lists(db: Session = Depends(get_db)):
    return db.query(List).all()


# ── Items ─────────────────────────────────────────────────────────────────────

@app.post('/api/lists/{list_id}/items', response_model=ItemRead, status_code=201)
def create_item(list_id: int, body: ItemCreate, db: Session = Depends(get_db)):
    lst = db.get(List, list_id)
    if lst is None:
        raise HTTPException(status_code=404, detail='List not found')
    obj = Item(list_id=list_id, name=body.name, quantity=body.quantity, checked=body.checked)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get('/api/lists/{list_id}/items', response_model=list[ItemRead])
def get_items(list_id: int, db: Session = Depends(get_db)):
    if db.get(List, list_id) is None:
        raise HTTPException(status_code=404, detail='List not found')
    return db.query(Item).filter(Item.list_id == list_id).all()


@app.patch('/api/items/{item_id}', response_model=ItemRead)
def update_item(item_id: int, body: ItemUpdate, db: Session = Depends(get_db)):
    obj = db.get(Item, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail='Item not found')
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


@app.delete('/api/items/{item_id}', status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(Item, item_id)
    if obj is None:
        raise HTTPException(status_code=404, detail='Item not found')
    db.delete(obj)
    db.commit()


# ── Static / SPA ──────────────────────────────────────────────────────────────

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
