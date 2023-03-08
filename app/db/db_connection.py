import aioredis
import databases
from config import DATABASE_URL, REDIS_URL, DATABASE_TEST_URL

database = databases.Database(DATABASE_TEST_URL)


def get_db() -> databases.Database:
    return database


async def connect_to_database():
    await database.connect()


async def close_database_connection():
    await database.disconnect()


async def get_redis():
    redis = await aioredis.from_url(REDIS_URL)
    yield redis
    redis.close()
    await redis.wait.closed()



