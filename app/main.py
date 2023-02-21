from fastapi import FastAPI
import uvicorn
from app import config

app = FastAPI()


@app.get('/')
def home():
    return {"status_code": 200, "detail": "ok", "result": "working"}


if __name__ == '__main__':
    uvicorn.run('main:app', host=config.HOST, port=config.PORT, reload=True)
