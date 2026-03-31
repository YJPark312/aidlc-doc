from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.order.models import Order, OrderItem, OrderHistory


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order: Order) -> Order:
        self.db.add(order)
        await self.db.flush()
        return order

    async def create_order_item(self, item: OrderItem) -> OrderItem:
        self.db.add(item)
        await self.db.flush()
        return item

    async def get_order(self, order_id: int) -> Order | None:
        result = await self.db.execute(select(Order).where(Order.id == order_id))
        return result.scalar_one_or_none()

    async def get_orders_by_session(self, session_id: int) -> list[Order]:
        result = await self.db.execute(
            select(Order).where(Order.session_id == session_id).order_by(desc(Order.created_at))
        )
        return list(result.scalars().all())

    async def get_orders_by_table(self, table_id: int) -> list[Order]:
        result = await self.db.execute(
            select(Order).where(Order.table_id == table_id).order_by(desc(Order.created_at))
        )
        return list(result.scalars().all())

    async def get_order_items(self, order_id: int) -> list[OrderItem]:
        result = await self.db.execute(
            select(OrderItem).where(OrderItem.order_id == order_id)
        )
        return list(result.scalars().all())

    async def get_order_history(self, table_id: int) -> list[OrderHistory]:
        result = await self.db.execute(
            select(OrderHistory).where(OrderHistory.table_id == table_id)
            .order_by(desc(OrderHistory.completed_at))
        )
        return list(result.scalars().all())

    async def delete_order(self, order: Order):
        items = await self.get_order_items(order.id)
        for item in items:
            await self.db.delete(item)
        await self.db.delete(order)
