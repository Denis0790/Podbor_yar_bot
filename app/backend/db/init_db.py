import aiosqlite
from db.connection import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_tg INTEGER UNIQUE,
                name TEXT,
                number TEXT UNIQUE,
                vin TEXT,
                id_thread INTEGER
            )
        """)
        await db.commit()
        print(f"✅ База данных 'clients' инициализирована по пути: {DB_PATH}")

        await db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_phone TEXT,
                description TEXT,
                FOREIGN KEY (client_phone) REFERENCES clients (number))""")
        await db.commit()
        print(f"✅ База данных 'orders' инициализирована по пути: {DB_PATH}")