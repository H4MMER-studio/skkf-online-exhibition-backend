import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from src.api import router
from src.core import get_settings

app = FastAPI(
    title=get_settings().PROJECT_TITLE,
    description=get_settings().PROJECT_DESCRIPTION,
    version=get_settings().PROJECT_VERSION,
)

app.include_router(router=router)
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=get_settings().ALLOW_ORIGINS,
    allow_credentials=get_settings().ALLOW_CREDENTIALS,
    allow_methods=get_settings().ALLOW_METHODS,
    allow_headers=get_settings().ALLOW_HEADERS,
)


@app.on_event("startup")
async def connect_db():
    app.db_client = AsyncIOMotorClient(get_settings().DB_URL)
    app.db = app.db_client[get_settings().DB_NAME]


@app.on_event("shutdown")
async def close_db():
    app.db_client.close()


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
