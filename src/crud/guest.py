from datetime import datetime, timedelta, timezone

from bson import ObjectId
from fastapi import Request
from fastapi.encoders import jsonable_encoder

from src.crud.base import CRUDBase
from src.schema import CreateGuest, DeleteGuest, DeleteOption, UpdateGuest


class CRUDGuest(CRUDBase[CreateGuest, UpdateGuest]):
    async def delete(
        self,
        request: Request,
        guest_id: str,
        delete_option: DeleteOption,
        delete_data: DeleteGuest,
    ) -> dict | None:
        db = request.app.db[self.collection]

        if delete_option == "soft":
            delete_data.deleted_by = delete_data.deleted_by.name
            delete_data.deleted_at = datetime.now(
                tz=timezone(offset=timedelta(hours=9))
            )
            deleted_document = await db.find_one_and_update(
                {"_id": ObjectId(guest_id), "deleted_at": None},
                {"$set": jsonable_encoder(delete_data)},
                upsert=False,
            )

        else:
            deleted_document = await db.find_one_and_delete(
                {"_id": ObjectId(guest_id)}
            )

        return deleted_document


guest_crud = CRUDGuest(collection="guests")
