from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("table_sessions.id"), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    total_amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)
    menu_name = Column(String(100), nullable=False)
    menu_price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Integer, nullable=False)


class OrderHistory(Base):
    __tablename__ = "order_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, nullable=False)
    store_id = Column(Integer, nullable=False)
    table_id = Column(Integer, nullable=False)
    session_id = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    total_amount = Column(Integer, nullable=False)
    order_created_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=False)
    items_json = Column(Text, nullable=False)
