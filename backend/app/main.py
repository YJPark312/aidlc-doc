from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import engine, Base
from app.auth.router import router as auth_router
from app.menu.router import router as menu_router
from app.table.router import router as table_router
from app.order.router import router as order_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    yield


app = FastAPI(title="Table Order API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(menu_router, prefix="/api/v1", tags=["menu"])
app.include_router(table_router, prefix="/api/v1", tags=["table"])
app.include_router(order_router, prefix="/api/v1", tags=["order"])
