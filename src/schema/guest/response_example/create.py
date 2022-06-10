from src.schema.response_example import create_response, ErrorResponseModel


create_guest_response = create_response
create_response["422"] = {
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
                        "msg": "field required",
                        "type": "value_error.missing"
                    }
                ]
            }
        }
    },
}
