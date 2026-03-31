import os
import uuid

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.menu.models import Menu
from app.menu.repository import MenuRepository
from app.menu.schemas import MenuCreate, MenuUpdate, MenuOrderUpdate


class MenuService:
    def __init__(self, db: AsyncSession):
        self.repo = MenuRepository(db)
        self.db = db

    async def create_category(self, store_id: int, name: str):
        cat = await self.repo.create_category(store_id, name)
        await self.db.commit()
        return cat

    async def get_categories(self, store_id: int):
        return await self.repo.get_categories(store_id)

    async def create_menu(self, store_id: int, data: MenuCreate, image: UploadFile | None = None):
        cat = await self.repo.get_category(data.category_id)
        if not cat or cat.store_id != store_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category")
        image_url = await self._save_image(image) if image else None
        menu = Menu(
            store_id=store_id, category_id=data.category_id, name=data.name,
            price=data.price, description=data.description, image_url=image_url,
        )
        menu = await self.repo.create_menu(menu)
        await self.db.commit()
        return menu

    async def update_menu(self, menu_id: int, data: MenuUpdate, image: UploadFile | None = None):
        menu = await self.repo.get_menu(menu_id)
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
        if data.category_id is not None:
            menu.category_id = data.category_id
        if data.name is not None:
            menu.name = data.name
        if data.price is not None:
            menu.price = data.price
        if data.description is not None:
            menu.description = data.description
        if image:
            if menu.image_url:
                self._delete_image(menu.image_url)
            menu.image_url = await self._save_image(image)
        await self.db.commit()
        return menu

    async def delete_menu(self, menu_id: int):
        menu = await self.repo.get_menu(menu_id)
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
        menu.is_deleted = True
        await self.db.commit()

    async def get_menus(self, store_id: int, category_id: int | None = None):
        return await self.repo.get_menus_by_store(store_id, category_id)

    async def update_menu_order(self, store_id: int, data: MenuOrderUpdate):
        for item in data.items:
            menu = await self.repo.get_menu(item.menu_id)
            if menu and menu.store_id == store_id:
                menu.sort_order = item.sort_order
        await self.db.commit()

    async def _save_image(self, image: UploadFile) -> str:
        ext = os.path.splitext(image.filename or "")[1] or ".jpg"
        filename = f"{uuid.uuid4()}{ext}"
        path = os.path.join(settings.UPLOAD_DIR, filename)
        content = await image.read()
        with open(path, "wb") as f:
            f.write(content)
        return f"/uploads/{filename}"

    def _delete_image(self, image_url: str):
        path = os.path.join(settings.UPLOAD_DIR, os.path.basename(image_url))
        if os.path.exists(path):
            os.remove(path)
