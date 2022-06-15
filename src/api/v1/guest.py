from bson.errors import InvalidId
from fastapi import APIRouter, Body, Header, Path, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.crud import guest_crud
from src.schema import (
    CreateGuest,
    DeleteGuest,
    DeleteOption,
    create_guest_response,
    delete_guest_response,
    get_multi_guests_response,
)

SINGLE_PREFIX = "/guest"
PLURAL_PREFIX = "/guests"

router = APIRouter()


@router.get(PLURAL_PREFIX, responses=get_multi_guests_response)
async def get_guests(
    request: Request,
    skip: int = Query(default=0, description="페이지네이션 시작값", example=1),
    limit: int = Query(default=0, description="페이지네이션 종료값", example=20),
) -> JSONResponse:
    """
    방명록 다량 조회(GET) 엔드포인트

    선택하여 전달할 수 있는 쿼리 매개변수 두 가지
    1. skip
    2. limit
    """
    try:
        result = await guest_crud.get_multi(
            request=request,
            skip=skip,
            limit=limit,
            projection={
                "created_at": True,
                "guest_nickname": True,
                "guest_content": True,
            },
        )
        if result["data"]:
            return JSONResponse(
                content={"data": result["data"], "size": result["data_size"]},
                status_code=status.HTTP_200_OK,
            )

        else:
            return JSONResponse(
                content={"data": []},
                status_code=status.HTTP_404_NOT_FOUND,
            )

    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post(SINGLE_PREFIX, responses=create_guest_response)
async def create_guest(
    request: Request,
    user_agent: str = Header(
        default=...,
        description="방명록 작성자의 IP 주소",
        example="PostmanRuntime/7.29.0",
    ),
    insert_data: dict[str, str] = Body(
        default=...,
        description="방명록 생성을 위한 본문",
        example={"guest_nickname": "이승호디자인짱", "guest_content": "이승호 너 천재냐?"},
    ),
) -> JSONResponse:
    """
    방명록 생성(CREATE) 엔드포인트

    필수로 전달해야 할 본문 매개변수 두 가지
    1. guest_nickname
    2. guest_content
    """
    try:
        insert_data["guest_ip_address"] = request.client.host
        insert_data["guest_device"] = user_agent

        await guest_crud.create(
            request=request, insert_data=CreateGuest(**insert_data)
        )

        return JSONResponse(
            content={"detail": "Success"},
            status_code=status.HTTP_200_OK,
        )

    except ValidationError as validation_error:
        return JSONResponse(
            content={"detail": validation_error.errors()},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.delete(SINGLE_PREFIX + "/{guest_id}", responses=delete_guest_response)
async def delete_guest(
    request: Request,
    guest_id: str = Path(
        default=...,
        description="삭제 대상이 되는 방명록의 ObjectId 값",
        example="62a3346d37209d075fa1b7e2",
    ),
    option: DeleteOption = Query(
        default=DeleteOption.SOFT,
        description="방명록 삭제 옵션 (논리적 삭제 / 물리적 삭제)",
        example="hard",
    ),
    delete_data: DeleteGuest = Body(
        default=...,
        description="방명록 논리적 삭제를 위한 본문",
        example={"deleted_by": "U02KXM336NL"},
    ),
) -> JSONResponse:
    """
    방명록 삭제(DELETE) 엔드포인트
    """
    try:
        if await guest_crud.delete(
            request=request,
            guest_id=guest_id,
            delete_option=option.value,
            delete_data=delete_data,
        ):
            return JSONResponse(
                content={"detail": "Success"},
                status_code=status.HTTP_200_OK,
            )

        else:
            return JSONResponse(
                content={"data": []},
                status_code=status.HTTP_404_NOT_FOUND,
            )

    except InvalidId as invalid_error:
        return JSONResponse(
            content={"detail": str(invalid_error)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
