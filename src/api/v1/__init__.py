from fastapi import APIRouter

from src.api.v1 import guest

router = APIRouter(prefix="/v1")

router.include_router(router=guest.router, tags=["방명록"])
