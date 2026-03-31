from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repository import AuthRepository
from app.auth.schemas import RegisterRequest, LoginRequest, TableLoginRequest
from app.core.security import hash_password, verify_password, create_access_token
from app.table.repository import TableRepository


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = AuthRepository(db)
        self.table_repo = TableRepository(db)
        self.db = db

    async def register(self, req: RegisterRequest):
        existing = await self.repo.get_store_by_name(req.store_name)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Store name already exists")
        store = await self.repo.create_store(req.store_name)
        hashed = hash_password(req.password)
        user = await self.repo.create_admin_user(store.id, req.username, hashed)
        await self.db.commit()
        return {"store_id": store.id, "store_name": store.name, "user_id": user.id, "username": user.username}

    async def login_admin(self, req: LoginRequest):
        store = await self.repo.get_store_by_name(req.store_name)
        if not store:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        user = await self.repo.get_admin_user(store.id, req.username)
        if not user or not verify_password(req.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        token = create_access_token({"user_id": user.id, "store_id": store.id, "role": "admin"})
        return {"access_token": token, "token_type": "bearer"}

    async def login_table(self, req: TableLoginRequest):
        table = await self.table_repo.get_by_store_and_number(req.store_id, req.table_number)
        if not table or not verify_password(req.password, table.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        token = create_access_token({"table_id": table.id, "store_id": req.store_id, "role": "table"})
        return {"access_token": token, "token_type": "bearer"}
