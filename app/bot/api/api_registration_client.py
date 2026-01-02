from dataclasses import asdict

import httpx
import logging

from data.data_registration_client import DataRegistrationClient

http_client = httpx.AsyncClient(base_url="http://backend:8000", timeout=5.0)


async def registration_client(reg_client: DataRegistrationClient):
    try:
        response = await http_client.post(
            "/add",
            json=asdict(reg_client)
        )

        if response.status_code == 200:
            return {"success": True, "message": "Ок"}
        error_detail = response.json().get("detail", "Ошибка сервера")

        return {"success": False, "message": error_detail}

    except Exception as e:
        logging.error(f"Ошибка API: {e}")
        return {"success": False, "message": "Проблемы с соединением"}