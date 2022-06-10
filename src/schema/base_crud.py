from datetime import datetime, timedelta, timezone
from enum import Enum

from pydantic import BaseModel


class DeleteOption(str, Enum):
    SOFT = "soft"
    HARD = "hard"


class CRUDSchemaBase(BaseModel):
    created_at: datetime | None
    updated_at: datetime | None
    deleted_at: datetime | None


class CreateSchemaBase(CRUDSchemaBase):
    created_at: datetime = datetime.now(tz=timezone(offset=timedelta(hours=9)))


class UpdateSchemaBase(CRUDSchemaBase):
    updated_at: datetime = datetime.now(tz=timezone(offset=timedelta(hours=9)))


class DeleteSchemaBase(CRUDSchemaBase):
    deleted_at: datetime = datetime.now(tz=timezone(offset=timedelta(hours=9)))
