import logging
import re
from fastapi import APIRouter
from db.DBManager import DBManager
from db.connection import get_db_session

logger = logging.getLogger(__name__)

search_order_router = APIRouter(tags=["Ордера"])

@search_order_router.get("/description{client_phone}")
async def search_order(client_phone: str):
    clean_number = re.sub(r"\D", "", client_phone)

    if len(clean_number) < 10:
        return {"error": f"Номер '{client_phone}' слишком короткий. Нужно минимум 10 цифр."}

    phone_tail = clean_number[-10:]
    async with get_db_session() as db:
        manager = DBManager(db)
        result = await manager.manager_search_order(phone_tail)
        if result is not None:
            return result
        else:
            return {"message":"Данных нет!"}