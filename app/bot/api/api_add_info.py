import httpx
import logging

http_client = httpx.AsyncClient(base_url="http://backend:8000", timeout=5.0)

async def add_info(number: int, info: str):
    try:
        payload = {
            "client_phone": number,
            "description": info
        }

        response = await http_client.post(
            "/add_order",
            json=payload
        )

        if response.status_code == 200:
            return {"success": True, "message": "Ок"}
        error_detail = response.json().get("detail", "Ошибка сервера")

        return {"success": False, "message": error_detail}

    except Exception as e:
        logging.error(f"Ошибка API: {e}")
        return {"success": False, "message": "Проблемы с соединением"}