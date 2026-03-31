from pydantic import BaseModel
from datetime import datetime


class TableSetup(BaseModel):
    table_number: int
    password: str


class TableResponse(BaseModel):
    id: int
    store_id: int
    table_number: int

    class Config:
        from_attributes = True


class TableSessionResponse(BaseModel):
    id: int
    table_id: int
    started_at: datetime
    completed_at: datetime | None
    is_active: bool

    class Config:
        from_attributes = True
