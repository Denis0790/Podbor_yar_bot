import logging
from fastapi import APIRouter, HTTPException
from db.DBManager import DBManager
from db.connection import get_db_session
from schemas.CreateOrderSchema import CreateOrder

logger = logging.getLogger(__name__)

create_order_router = APIRouter(tags=["Ордера"])

@create_order_router.post("/add_order")
async def create_order(order: CreateOrder):
    async with get_db_session() as db:
        manager = DBManager(db)
        await manager.manager_create_order(order)
        try:
            return {"message": "Данные успешно добавлены"}
        except Exception as e:
            return {"message": str(e)}