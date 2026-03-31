from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.menu.schemas import CategoryCreate, CategoryResponse, MenuResponse, MenuUpdate, MenuOrderUpdate
from app.menu.service import MenuService

router = APIRouter()


# --- Categories ---

@router.post("/stores/{store_id}/categories", response_model=CategoryResponse)
async def create_category(
    store_id: int, req: CategoryCreate,
    db: AsyncSession = Depends(get_db), _=Depends(get_current_admin),
):
    return await MenuService(db).create_category(store_id, req.name)


@router.get("/stores/{store_id}/categories", response_model=list[CategoryResponse])
async def get_categories(store_id: int, db: AsyncSession = Depends(get_db)):
    return await MenuService(db).get_categories(store_id)


# --- Menus ---

@router.get("/stores/{store_id}/menus", response_model=list[MenuResponse])
async def get_menus(
    store_id: int, category_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await MenuService(db).get_menus(store_id, category_id)


@router.post("/stores/{store_id}/menus", response_model=MenuResponse)
async def create_menu(
    store_id: int,
    category_id: int = Form(...), name: str = Form(...), price: int = Form(..., ge=0),
    description: str | None = Form(None), image: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db), _=Depends(get_current_admin),
):
    from app.menu.schemas import MenuCreate
    data = MenuCreate(category_id=category_id, name=name, price=price, description=description)
    return await MenuService(db).create_menu(store_id, data, image)


@router.put("/menus/{menu_id}", response_model=MenuResponse)
async def update_menu(
    menu_id: int,
    category_id: int | None = Form(None), name: str | None = Form(None),
    price: int | None = Form(None), description: str | None = Form(None),
    image: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db), _=Depends(get_current_admin),
):
    data = MenuUpdate(category_id=category_id, name=name, price=price, description=description)
    return await MenuService(db).update_menu(menu_id, data, image)


@router.delete("/menus/{menu_id}")
async def delete_menu(
    menu_id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_admin),
):
    await MenuService(db).delete_menu(menu_id)
    return {"detail": "Menu deleted"}


@router.patch("/stores/{store_id}/menus/order")
async def update_menu_order(
    store_id: int, data: MenuOrderUpdate,
    db: AsyncSession = Depends(get_db), _=Depends(get_current_admin),
):
    await MenuService(db).update_menu_order(store_id, data)
    return {"detail": "Order updated"}
