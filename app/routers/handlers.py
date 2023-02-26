from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def home():
    return {"status_code": 200, "detail": "ok", "result": "working"}
