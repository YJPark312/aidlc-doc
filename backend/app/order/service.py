import json

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.menu.repository import MenuRepository
from app.order.models import Order, OrderItem
from app.order.repository import OrderRepository
from app.order.schemas import CreateOrderRequest
from app.order.sse import sse_manager
from app.table.repository import TableRepository


VALID_TRANSITIONS = {
    "pending": "preparing",
    "preparing": "completed",
}


class OrderService:
    def __init__(self, db: AsyncSession):
        self.repo = OrderRepository(db)
        self.menu_repo = MenuRepository(db)
        self.table_repo = TableRepository(db)
        self.db = db

    async def create_order(self, store_id: int, table_id: int, req: CreateOrderRequest):
        session = await self.table_repo.get_active_session(table_id)
        if not session:
            session = await self.table_repo.create_session(table_id)

        total = 0
        item_data = []
        for item in req.items:
            menu = await self.menu_repo.get_menu(item.menu_id)
            if not menu:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Menu {item.menu_id} not found")
            subtotal = menu.price * item.quantity
            total += subtotal
            item_data.append({"menu": menu, "quantity": item.quantity, "subtotal": subtotal})

        order = Order(store_id=store_id, table_id=table_id, session_id=session.id, total_amount=total)
        order = await self.repo.create_order(order)

        items_response = []
        for d in item_data:
            oi = OrderItem(
                order_id=order.id, menu_id=d["menu"].id, menu_name=d["menu"].name,
                menu_price=d["menu"].price, quantity=d["quantity"], subtotal=d["subtotal"],
            )
            oi = await self.repo.create_order_item(oi)
            items_response.append(oi)

        await self.db.commit()

        await sse_manager.broadcast(store_id, "new_order", json.dumps({
            "order_id": order.id, "table_id": table_id, "total_amount": total,
        }))

        return {"id": order.id, "store_id": order.store_id, "table_id": order.table_id,
                "session_id": order.session_id, "status": order.status, "total_amount": order.total_amount,
                "created_at": order.created_at, "items": items_response}

    async def get_orders_by_session(self, session_id: int):
        orders = await self.repo.get_orders_by_session(session_id)
        return await self._attach_items(orders)

    async def get_orders_by_table(self, table_id: int):
        orders = await self.repo.get_orders_by_table(table_id)
        return await self._attach_items(orders)

    async def update_status(self, order_id: int, new_status: str, store_id: int):
        order = await self.repo.get_order(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        expected = VALID_TRANSITIONS.get(order.status)
        if expected != new_status:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Invalid transition: {order.status} -> {new_status}")
        order.status = new_status
        await self.db.commit()

        await sse_manager.broadcast(store_id, "status_change", json.dumps({
            "order_id": order_id, "status": new_status,
        }))
        return order

    async def delete_order(self, order_id: int, store_id: int):
        order = await self.repo.get_order(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        await self.repo.delete_order(order)
        await self.db.commit()

        await sse_manager.broadcast(store_id, "order_deleted", json.dumps({"order_id": order_id}))

    async def get_order_history(self, table_id: int):
        return await self.repo.get_order_history(table_id)

    async def _attach_items(self, orders):
        result = []
        for o in orders:
            items = await self.repo.get_order_items(o.id)
            result.append({
                "id": o.id, "store_id": o.store_id, "table_id": o.table_id,
                "session_id": o.session_id, "status": o.status, "total_amount": o.total_amount,
                "created_at": o.created_at, "items": items,
            })
        return result
