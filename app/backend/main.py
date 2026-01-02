from contextlib import asynccontextmanager

from fastapi import FastAPI
import logging

from routers.router_search_client_id_thread import search_client_id_thread_router
from routers.router_search_client_id import search_client_id_router
from routers.router_search_order import search_order_router
from routers.router_create_order import create_order_router
from routers.router_update_client import update_client_router
from routers.router_search_client import search_client_router
from db.init_db import init_db
from routers.router_create_client import create_client_router
from routers.router_start import start_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("PodborBot")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения: инициализация базы данных...")
    try:
        await init_db()
        logger.info("База данных успешно подготовлена")
    except Exception as e:
        logger.error(f"Критическая ошибка при инициализации БД: {e}")

    yield

    logger.info("Остановка приложения...")


app = FastAPI(lifespan=lifespan)

app.include_router(start_router)
app.include_router(search_order_router)
app.include_router(create_client_router)
app.include_router(search_client_router)
app.include_router(update_client_router)
app.include_router(create_order_router)
app.include_router(search_client_id_router)
app.include_router(search_client_id_thread_router)


