import asyncio

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_admin, get_current_table, get_current_user
from app.order.schemas import (
    CreateOrderRequest, OrderResponse, OrderStatusUpdate, OrderHistoryResponse,
)
from app.order.service import OrderService
from app.order.sse import sse_manager

router = APIRouter()


@router.post("/tables/{table_id}/orders", response_model=OrderResponse)
async def create_order(
    table_id: int, req: CreateOrderRequest,
    db: AsyncSession = Depends(get_db), payload: dict = Depends(get_current_table),
):
    store_id = payload["store_id"]
    return await OrderService(db).create_order(store_id, table_id, req)


@router.get("/sessions/{session_id}/orders", response_model=list[OrderResponse])
async def get_session_orders(
    session_id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_user),
):
    return await OrderService(db).get_orders_by_session(session_id)


@router.get("/tables/{table_id}/orders", response_model=list[OrderResponse])
async def get_table_orders(
    table_id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_admin),
):
    return await OrderService(db).get_orders_by_table(table_id)


@router.patch("/orders/{order_id}/status")
async def update_order_status(
    order_id: int, req: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db), payload: dict = Depends(get_current_admin),
):
    return await OrderService(db).update_status(order_id, req.status, payload["store_id"])


@router.delete("/orders/{order_id}")
async def delete_order(
    order_id: int, db: AsyncSession = Depends(get_db), payload: dict = Depends(get_current_admin),
):
    await OrderService(db).delete_order(order_id, payload["store_id"])
    return {"detail": "Order deleted"}


@router.get("/tables/{table_id}/order-history", response_model=list[OrderHistoryResponse])
async def get_order_history(
    table_id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_admin),
):
    return await OrderService(db).get_order_history(table_id)


@router.get("/stores/{store_id}/orders/stream")
async def stream_orders(store_id: int, _=Depends(get_current_admin)):
    queue = sse_manager.connect(store_id)

    async def event_generator():
        try:
            while True:
                data = await asyncio.wait_for(queue.get(), timeout=30)
                yield data
        except asyncio.TimeoutError:
            yield "event: ping\ndata: {}\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            sse_manager.disconnect(store_id, queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
