from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.handlers import router
import uvicorn
import config
from db.db_connection import connect_to_database, close_database_connection, get_redis


def get_application() -> FastAPI:

    my_app = FastAPI()
    my_app.include_router(router)

    origins = [
        "https://0.0.0.0:8000"
    ]

    my_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @my_app.on_event("startup")
    async def startup():
        get_redis()
        await connect_to_database()

    @my_app.on_event("shutdown")
    async def shutdown():
        await close_database_connection()

    return my_app


app = get_application()

if __name__ == '__main__':
    uvicorn.run('main:app', host=config.HOST, port=config.PORT, reload=True)
