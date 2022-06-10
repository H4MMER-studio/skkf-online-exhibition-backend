from src.schema.response_example import GetResponseModel, ErrorResponseModel
from src.schema.response_example import get_multi_response


get_multi_guests_response = get_multi_response
get_multi_guests_response["200"] = {
    "model": GetResponseModel,
    "description": "방명록 다량 조회 성공",
    "content": {
        "application/json": {
            "example": {
                "data": [
                    {
                        "_id": "62a3346d37209d075fa1b7e2",
                        "created_at": "2022-06-10T21:08:46.301912+09:00",
                        "updated_at": "null",
                        "deleted_at": "null",
                        "guest_ip_address": "127.0.0.1",
                        "guest_device": "PostmanRuntime/7.29.0",
                        "guest_nickname": "성균관대학교",
                        "guest_content": "성균과대학교 최고"
                    },
                    {
                        "_id": "62a32724da73972395384f11",
                        "created_at": "2022-06-10T20:11:52.737020+09:00",
                        "updated_at": "null",
                        "deleted_at": "null",
                        "guest_ip_address": "127.0.0.1",
                        "guest_device": "PostmanRuntime/7.29.0",
                        "guest_nickname": "2번 방명록 작성자",
                        "guest_content": "여기는 방명록 본문 2번"
                    }
                ],
                "size": 2
            }
        }
    },
}
get_multi_guests_response["422"] = {
    "model": ErrorResponseModel,
    "description": "유효하지 않은 매개변수를 사용",
    "content": {
        "application/json": {
            "example": {
                "detail": [
                    {
                        "loc": [
                            "guest_content"
                        ],
                        "msg": "Content length must be smaller than 300",
                        "type": "value_error"
                    }
                ]
            }
        }
    },
}
