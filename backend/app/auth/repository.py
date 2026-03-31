from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import Store, AdminUser


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_store_by_name(self, name: str) -> Store | None:
        result = await self.db.execute(select(Store).where(Store.name == name))
        return result.scalar_one_or_none()

    async def create_store(self, name: str) -> Store:
        store = Store(name=name)
        self.db.add(store)
        await self.db.flush()
        return store

    async def get_admin_user(self, store_id: int, username: str) -> AdminUser | None:
        result = await self.db.execute(
            select(AdminUser).where(AdminUser.store_id == store_id, AdminUser.username == username)
        )
        return result.scalar_one_or_none()

    async def create_admin_user(self, store_id: int, username: str, password_hash: str) -> AdminUser:
        user = AdminUser(store_id=store_id, username=username, password_hash=password_hash)
        self.db.add(user)
        await self.db.flush()
        return user
