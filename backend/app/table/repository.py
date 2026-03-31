from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.table.models import Table, TableSession


class TableRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_store_and_number(self, store_id: int, table_number: int) -> Table | None:
        result = await self.db.execute(
            select(Table).where(Table.store_id == store_id, Table.table_number == table_number)
        )
        return result.scalar_one_or_none()

    async def create_table(self, store_id: int, table_number: int, password_hash: str) -> Table:
        table = Table(store_id=store_id, table_number=table_number, password_hash=password_hash)
        self.db.add(table)
        await self.db.flush()
        return table

    async def get_tables(self, store_id: int) -> list[Table]:
        result = await self.db.execute(
            select(Table).where(Table.store_id == store_id).order_by(Table.table_number)
        )
        return list(result.scalars().all())

    async def get_active_session(self, table_id: int) -> TableSession | None:
        result = await self.db.execute(
            select(TableSession).where(TableSession.table_id == table_id, TableSession.is_active == True)
        )
        return result.scalar_one_or_none()

    async def create_session(self, table_id: int) -> TableSession:
        session = TableSession(table_id=table_id)
        self.db.add(session)
        await self.db.flush()
        return session
