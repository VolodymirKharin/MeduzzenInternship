from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app import config


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
@app.get('/')
def home():
    return {"status_code": 200, "detail": "ok", "result": "working"}


if __name__ == '__main__':
    uvicorn.run('main:app', host=config.HOST, port=config.PORT, reload=True)
