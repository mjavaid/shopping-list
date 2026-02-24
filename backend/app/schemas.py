from datetime import datetime
from pydantic import BaseModel


# ── List schemas ──────────────────────────────────────────────────────────────

class ListCreate(BaseModel):
    name: str


class ListRead(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Item schemas ──────────────────────────────────────────────────────────────

class ItemCreate(BaseModel):
    name: str
    quantity: int | None = None
    checked: bool = False


class ItemUpdate(BaseModel):
    name: str | None = None
    quantity: int | None = None
    checked: bool | None = None


class ItemRead(BaseModel):
    id: int
    list_id: int
    name: str
    quantity: int | None
    checked: bool
    created_at: datetime

    model_config = {"from_attributes": True}
