from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from auth.di import UserStatusChecker
from auth.exceptions import UnauthorizedResponse, EditorStatusRequiredResponse, \
    AdminStatusRequiredResponse
from common.responses import OkResponse
from entity_type_connections.di import get_list_type_connections_use_case, \
    get_create_type_connection_use_case, get_type_connection_use_case, \
    get_update_type_connection_use_case, get_delete_type_connection_use_case
from entity_type_connections.dto import TypeConnectionOutputDTO, \
    TypeConnectionExtendedOutputDTO, CreateTypeConnectionInputDTO, \
    UpdateTypeConnectionInputDTO
from entity_type_connections.exceptions import TypeConnectionNotFoundResponse, \
    TypeConnectionAlreadyExistsResponse, TypeConnectionCreatesCycleResponse
from entity_type_connections.use_cases.create_connection import \
    CreateTypeConnectionUseCase
from entity_type_connections.use_cases.delete_connection import \
    DeleteTypeConnectionUseCase
from entity_type_connections.use_cases.get_connection_info import \
    GetTypeConnectionUseCase
from entity_type_connections.use_cases.list_connections import \
    ListTypeConnectionsUseCase
from entity_type_connections.use_cases.update_connection import \
    UpdateTypeConnectionUseCase
from infrastructure.db import UserStatus

type_connections_router = APIRouter()


@type_connections_router.get(
    '/list',
    response_model=list[TypeConnectionOutputDTO]
)
async def list_connections(
        use_case: ListTypeConnectionsUseCase = Depends(
            get_list_type_connections_use_case
        ),
):
    """Возвращает информацию о связях между типами сущностей.

    На основе этой информации необходимо строить колонки связей в таблицах.
    Если в названии колонки указан null, её отображать не надо.
    Также можно использовать эту информацию при построении графа.

    """
    return await use_case.execute()


@type_connections_router.get(
    '/{connection_id}',
    response_model=TypeConnectionExtendedOutputDTO,
    response_class=ORJSONResponse,
    responses={404: {'model': TypeConnectionNotFoundResponse}},
)
async def get_connection_info(
        connection_id: int,
        use_case: GetTypeConnectionUseCase = Depends(
            get_type_connection_use_case
        ),
):
    """Возвращает информацию о связи между типами сущностей
    вместе со списком связей самих сущностей.
    """
    result = await use_case.execute(connection_id)
    return ORJSONResponse(result.dict())


@type_connections_router.post(
    '',
    response_model=TypeConnectionOutputDTO,
    responses={
        400: {'model': TypeConnectionCreatesCycleResponse},
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        409: {'model': TypeConnectionAlreadyExistsResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def create_connection(
        input_dto: CreateTypeConnectionInputDTO,
        use_case: CreateTypeConnectionUseCase = Depends(
            get_create_type_connection_use_case
        )
):
    """Создает связь между типами сущностей. Требует статус admin."""
    return await use_case.execute(input_dto)


@type_connections_router.put(
    '/{connection_id}',
    response_model=TypeConnectionOutputDTO,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        404: {'model': TypeConnectionNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def update_column_name(
        connection_id: int,
        input_dto: UpdateTypeConnectionInputDTO,
        use_case: UpdateTypeConnectionUseCase = Depends(
            get_update_type_connection_use_case
        )
):
    """Обновляет название колонки связей в таблице.

    Если указать null, колонка скроется.
    Требует статус admin.

    """
    return await use_case.execute(connection_id, input_dto)


@type_connections_router.delete(
    '/{connection_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        404: {'model': TypeConnectionNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def delete_connection(
        connection_id: int,
        use_case: DeleteTypeConnectionUseCase = Depends(
            get_delete_type_connection_use_case
        ),
):
    """Удаляет связь между типами сущностей. Требует статус admin."""
    await use_case.execute(connection_id)
    return OkResponse()
