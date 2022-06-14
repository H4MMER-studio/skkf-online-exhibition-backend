from enum import Enum

from pydantic import IPvAnyAddress, validator

from src.schema.base_crud import CRUDSchemaBase


class SlackManager(str, Enum):
    김건우 = "U02K5371TT7"
    이승호 = "U02KA8141LL"
    이태현 = "U02KXM336NL"
    최예흠 = "U02K82HPFHR"


class GuestBase(CRUDSchemaBase):
    pass


class CreateGuest(GuestBase):
    guest_ip_address: IPvAnyAddress
    guest_device: str
    guest_nickname: str
    guest_content: str

    @validator("guest_nickname")
    def title_length(cls, nickname):
        if not nickname:
            raise ValueError("Nickname must be required")

        elif len(nickname) > 10:
            raise ValueError("Nickname length must be smaller than 10")

        else:
            return nickname

    @validator("guest_content")
    def content_length(cls, content):
        if not content:
            raise ValueError("Content must be required")

        elif len(content) > 300:
            raise ValueError("Content length must be smaller than 300")

        else:
            return content

    class Config:
        schema_extra: dict[str, dict] = {
            "example": {
                "guest_ip_address": "62a3346d37209d075fa1b7e2",
                "guest_device": "PostmanRuntime/7.29.0",
                "guest_nickname": "작성자 닉네임",
                "guest_content": "방명록 작성 본문",
                "created_at": "2022-06-10T21:08:46.301912+09:00",
                "updated_at": "null",
                "deleted_at": "null",
            }
        }


class UpdateGuest(GuestBase):
    pass


class DeleteGuest(GuestBase):
    deleted_by: SlackManager

    class Config:
        schema_extra: dict[str, dict] = {
            "example": {
                "delete_at": "2022-06-10T21:08:46.301912+09:00",
                "deleted_by": "U02KXM336NL",
            }
        }
