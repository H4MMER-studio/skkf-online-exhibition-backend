from src.schema.response_example.base_response import AlterResponseModel


create_response = {
    "200": {
        "model": AlterResponseModel,
        "description": "생성 성공",
        "content": {"application/json": {"example": {"detail": "Success"}}}
    }
}
