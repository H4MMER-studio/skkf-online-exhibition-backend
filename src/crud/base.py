from datetime import datetime, timedelta, timezone
from typing import Generic, TypeVar

from bson.objectid import ObjectId
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pymongo import ASCENDING, DESCENDING

CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class CRUDBase(Generic[CreateSchema, UpdateSchema]):
    def __init__(self, collection: str) -> None:
        self.collection = collection

    async def get_one(self, request: Request, id: str) -> dict | None:
        db = request.app.db[self.collection]
        if not (document := db.find_one({"_id": ObjectId(id)})):
            return None

        else:
            document["_id"] = str(document["_id"])
            return document

    async def get_multi(
        self,
        request: Request,
        skip: int,
        limit: int,
        sort: list[str] = [],
        filter: dict = {},
        projection: dict = {},
    ) -> dict | None:
        db = request.app.db[self.collection]

        filter["deleted_at"] = None
        if not (data_size := await db.count_documents(filter)):
            return None

        else:
            result = {"data_size": data_size}
            query = db.find(filter=filter, projection=projection)

        sort_field: list = []
        if sort:
            for query_string in sort:
                field, option = query_string.split(" ")
                field = field.replace("-", "_")

                if option == "asc":
                    option = ASCENDING
                elif option == "desc":
                    option = DESCENDING
                else:
                    raise ValueError

                sort_field.append((field, option))

        else:
            sort_field.append(("$natural", DESCENDING))

        query = query.sort(sort_field)

        if skip:
            skip -= 1

        documents = (
            await query.skip(skip).limit(limit - skip).to_list(length=None)
        )

        if not documents:
            return None

        for document in documents:
            document["_id"] = str(document["_id"])

        result["data"] = documents

        return result

    async def create(
        self, request: Request, insert_data: CreateSchema
    ) -> bool:
        insert_data.created_at = datetime.now(
            tz=timezone(offset=timedelta(hours=9))
        )
        inserted_document = await request.app.db[self.collection].insert_one(
            jsonable_encoder(insert_data)
        )

        result = inserted_document.acknowledged

        return result

    async def update(
        self, request: Request, id: str, update_data: UpdateSchema
    ) -> bool:
        update_data.updated_dat = datetime.now(
            tz=timezone(offset=timedelta(hours=9))
        )
        update_data = update_data.dict(exclude_none=True)

        updated_document = await request.app.db[
            self.collection
        ].find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": jsonable_encoder(update_data)},
            upsert=False,
        )

        return updated_document

    async def delete(self, request: Request, id: str) -> bool:
        deleted_document = await request.app.db[
            self.collection
        ].find_one_and_delete({"_id": ObjectId(id)})

        return deleted_document
