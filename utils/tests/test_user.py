import asyncio
from db_utils import create_user

asyncio.run(
    create_user(
        "admin",
        "admin@campuswatt.com",
        "password123"
    )
)
