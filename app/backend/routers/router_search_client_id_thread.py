from db.DBManager import DBManager
from db.connection import get_db_session
import logging
from fastapi import APIRouter


search_client_id_thread_router = APIRouter(tags=["Клиенты"])
logger = logging.getLogger(__name__)


@search_client_id_thread_router.get("/client_by_id_thread/{id_thread}")
async def search_client_id_thread(id_thread: int):
    async with get_db_session() as db:
        manager = DBManager(db)
        result = await manager.manager_search_client_by_id_thread(id_thread=id_thread)
        if result is not None:
            return result
        else:
            return None