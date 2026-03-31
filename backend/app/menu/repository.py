from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.menu.models import Category, Menu


class MenuRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_category(self, store_id: int, name: str) -> Category:
        cat = Category(store_id=store_id, name=name)
        self.db.add(cat)
        await self.db.flush()
        return cat

    async def get_categories(self, store_id: int) -> list[Category]:
        result = await self.db.execute(
            select(Category).where(Category.store_id == store_id).order_by(Category.sort_order)
        )
        return list(result.scalars().all())

    async def get_category(self, category_id: int) -> Category | None:
        result = await self.db.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()

    async def create_menu(self, menu: Menu) -> Menu:
        self.db.add(menu)
        await self.db.flush()
        return menu

    async def get_menu(self, menu_id: int) -> Menu | None:
        result = await self.db.execute(
            select(Menu).where(Menu.id == menu_id, Menu.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def get_menus_by_store(self, store_id: int, category_id: int | None = None) -> list[Menu]:
        query = select(Menu).where(Menu.store_id == store_id, Menu.is_deleted == False)
        if category_id:
            query = query.where(Menu.category_id == category_id)
        result = await self.db.execute(query.order_by(Menu.sort_order))
        return list(result.scalars().all())

    async def get_menu_by_id_any(self, menu_id: int) -> Menu | None:
        """Get menu regardless of is_deleted status (for order snapshot)."""
        result = await self.db.execute(select(Menu).where(Menu.id == menu_id))
        return result.scalar_one_or_none()
