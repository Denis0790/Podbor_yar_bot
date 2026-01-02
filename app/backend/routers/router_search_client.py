import logging
import re
from fastapi import APIRouter, HTTPException, Depends
from db.DBManager import DBManager
from db.connection import get_db_session


search_client_router = APIRouter(tags=["Клиенты"])
logger = logging.getLogger(__name__)


@search_client_router.get("/{number}")
async def search_client(number: str):
    clean_number = re.sub(r"\D", "", number)

    if len(clean_number) < 10:
        return {"error": f"Номер '{number}' слишком короткий. Нужно минимум 10 цифр."}

    phone_tail = clean_number[-10:]

    async with get_db_session() as db:
        manager = DBManager(db)
        result = await manager.manager_search_client(phone_tail)
        if result is not None:
            return result
        else:
            return None