from fastapi import APIRouter, Depends

from auth.di import UserStatusChecker
from auth.exceptions import UnauthorizedResponse, EditorStatusRequiredResponse
from common.responses import OkResponse
from entities.exceptions import EntityNotFoundResponse
from entity_connections.di import get_connect_entities_use_case, \
    get_disconnect_entities_use_case
from entity_connections.dto import EntityConnectionInputDTO, \
    EntityConnectionOutputDTO
from entity_connections.exceptions import \
    EntityConnectionAlreadyExistsResponse, EntityConnectionNotFoundResponse
from entity_connections.use_cases.connect_entities import \
    ConnectEntitiesUseCase
from entity_connections.use_cases.disconnect_entities import \
    DisconnectEntitiesUseCase
from entity_type_connections.exceptions import TypeConnectionNotFoundResponse
from infrastructure.db import UserStatus

entity_connections_router = APIRouter()


@entity_connections_router.post(
    '',
    response_model=EntityConnectionOutputDTO,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse},
        404: {
            'model': EntityNotFoundResponse | TypeConnectionNotFoundResponse
        },
        409: {'model': EntityConnectionAlreadyExistsResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def connect_entities(
        input_dto: EntityConnectionInputDTO,
        use_case: ConnectEntitiesUseCase = Depends(
            get_connect_entities_use_case
        )
):
    """Создает связь между сущностями. Требует статус editor."""
    result = await use_case.execute(input_dto)
    return EntityConnectionOutputDTO.from_orm(result)


@entity_connections_router.delete(
    '/{connection_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse},
        404: {'model': EntityConnectionNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def disconnect_entities(
        connection_id: int,
        use_case: DisconnectEntitiesUseCase = Depends(
            get_disconnect_entities_use_case
        )
):
    """Удаляет связь между сущностями. Требует статус editor."""
    await use_case.execute(connection_id)
    return OkResponse()
