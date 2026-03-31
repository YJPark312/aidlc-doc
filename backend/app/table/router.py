from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.table.schemas import TableSetup, TableResponse
from app.table.service import TableService

router = APIRouter()


@router.post("/stores/{store_id}/tables", response_model=TableResponse)
async def setup_table(
    store_id: int, req: TableSetup,
    db: AsyncSession = Depends(get_db), _=Depends(get_current_admin),
):
    return await TableService(db).setup_table(store_id, req)


@router.get("/stores/{store_id}/tables", response_model=list[TableResponse])
async def get_tables(
    store_id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_admin),
):
    return await TableService(db).get_tables(store_id)


@router.post("/tables/{table_id}/complete")
async def complete_session(
    table_id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_admin),
):
    return await TableService(db).complete_session(table_id)
