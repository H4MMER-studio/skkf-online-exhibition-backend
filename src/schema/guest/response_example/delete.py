from src.schema.response_example import delete_response, ErrorResponseModel


delete_guest_response = delete_response
delete_guest_response["422"] = {
    "model": ErrorResponseModel,
    "description": "유효하지 않은 매개변수를 사용",
    "content": {
        "application/json": {
            "example": {
                "detail": [
                    {
                        "loc": [
                            "body"
                        ],
                        "msg": "field required",
                        "type": "value_error.missing"
                    }
                ]
            }
        }
    },
}
