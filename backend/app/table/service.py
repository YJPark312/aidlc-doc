import json
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.order.models import Order, OrderItem, OrderHistory
from app.order.repository import OrderRepository
from app.table.repository import TableRepository
from app.table.schemas import TableSetup


class TableService:
    def __init__(self, db: AsyncSession):
        self.repo = TableRepository(db)
        self.order_repo = OrderRepository(db)
        self.db = db

    async def setup_table(self, store_id: int, data: TableSetup):
        existing = await self.repo.get_by_store_and_number(store_id, data.table_number)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Table number already exists")
        hashed = hash_password(data.password)
        table = await self.repo.create_table(store_id, data.table_number, hashed)
        await self.db.commit()
        return table

    async def get_tables(self, store_id: int):
        return await self.repo.get_tables(store_id)

    async def complete_session(self, table_id: int):
        session = await self.repo.get_active_session(table_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active session")

        orders = await self.order_repo.get_orders_by_session(session.id)
        now = datetime.now(timezone.utc)

        for order in orders:
            if order.status != "completed":
                order.status = "completed"

            items = await self.order_repo.get_order_items(order.id)
            items_data = [
                {"menu_id": i.menu_id, "menu_name": i.menu_name, "menu_price": i.menu_price,
                 "quantity": i.quantity, "subtotal": i.subtotal}
                for i in items
            ]
            history = OrderHistory(
                order_id=order.id, store_id=order.store_id, table_id=order.table_id,
                session_id=order.session_id, status=order.status, total_amount=order.total_amount,
                order_created_at=order.created_at, completed_at=now, items_json=json.dumps(items_data),
            )
            self.db.add(history)

            for item in items:
                await self.db.delete(item)
            await self.db.delete(order)

        session.is_active = False
        session.completed_at = now
        await self.db.commit()
        return {"detail": "Session completed"}
