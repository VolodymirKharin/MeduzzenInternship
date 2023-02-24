from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import app.config as config
import aioredis
from app.utils.db_connection import get_db

app = FastAPI()

origins = [
    "https://0.0.0.0:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event('startup')
async def startup_event():
    app.state.redis_pool = aioredis.ConnectionPool.from_url(config.REDIS_URL)
    await get_db().connect()

@app.get('/redis')
async def read_redis():
    redis = aioredis.Redis(connection_pool=app.state.redis_pool)
    value = await redis.get('mykey')
    return {'key': 'mykey', 'value': value}
@app.get('/')
def home():
    return {"status_code": 200, "detail": "ok", "result": "working"}


if __name__ == '__main__':
    uvicorn.run('main:app', host=config.HOST, port=config.PORT, reload=True)
