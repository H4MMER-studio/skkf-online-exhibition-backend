from src.schema.response_example.base_response import GetResponseModel


get_multi_response = {
    "404": {
        "model": GetResponseModel,
        "description": "엔티티 미존재",
        "content": {"application/json": {"example": {"data": []}}},
    },
}
