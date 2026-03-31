from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    store_id: int
    name: str
    sort_order: int

    class Config:
        from_attributes = True


class MenuCreate(BaseModel):
    category_id: int
    name: str
    price: int = Field(ge=0)
    description: str | None = None


class MenuUpdate(BaseModel):
    category_id: int | None = None
    name: str | None = None
    price: int | None = Field(default=None, ge=0)
    description: str | None = None


class MenuResponse(BaseModel):
    id: int
    store_id: int
    category_id: int
    name: str
    price: int
    description: str | None
    image_url: str | None
    sort_order: int

    class Config:
        from_attributes = True


class MenuOrderItem(BaseModel):
    menu_id: int
    sort_order: int


class MenuOrderUpdate(BaseModel):
    items: list[MenuOrderItem]
