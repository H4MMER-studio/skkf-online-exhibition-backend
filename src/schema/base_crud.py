from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class DeleteOption(str, Enum):
    SOFT = "soft"
    HARD = "hard"


class CRUDSchemaBase(BaseModel):
    created_at: datetime | None
    updated_at: datetime | None
    deleted_at: datetime | None
