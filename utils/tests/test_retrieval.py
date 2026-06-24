import asyncio
from db_utils import user_retrieval

async def main():
    user = await user_retrieval("admin")
    print(user)

asyncio.run(main())
