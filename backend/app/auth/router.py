from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.auth.schemas import RegisterRequest, RegisterResponse, LoginRequest, TableLoginRequest, TokenResponse
from app.auth.service import AuthService

router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).register(req)


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).login_admin(req)


@router.post("/table-login", response_model=TokenResponse)
async def table_login(req: TableLoginRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).login_table(req)
