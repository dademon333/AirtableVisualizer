from fastapi import APIRouter, Depends, Query
from fastapi.responses import ORJSONResponse

from auth.di import UserStatusChecker
from auth.exceptions import UnauthorizedResponse, EditorStatusRequiredResponse
from common.responses import OkResponse
from entities.di import get_list_entities_use_case, \
    get_search_entities_use_case, get_get_entity_use_case, \
    get_update_entity_use_case, get_create_entity_use_case, \
    get_delete_entity_use_case
from entities.dto import EntityOutputDTO, CreateEntityInputDTO, \
    UpdateEntityInputDTO
from entities.exceptions import EntityNotFoundResponse, EntityNotFoundError
from entities.use_cases.create_entity import CreateEntityUseCase
from entities.use_cases.delete_entity import DeleteEntityUseCase
from entities.use_cases.get_entity import GetEntityUseCase
from entities.use_cases.list_entities import ListEntitiesUseCase
from entities.use_cases.search_entity import SearchEntitiesUseCase
from entities.use_cases.update_entity import UpdateEntityUseCase
from infrastructure.db import EntityType, UserStatus

entities_router = APIRouter()


@entities_router.get(
    '/list/{entity_type}',
    response_model=list[EntityOutputDTO],
    response_class=ORJSONResponse,
    responses={401: {'model': UnauthorizedResponse}},
)
async def list_entities(
        entity_type: EntityType,
        limit: int = Query(250, le=1000),
        offset: int = Query(0),
        use_case: ListEntitiesUseCase = Depends(get_list_entities_use_case),
):
    """Возвращает список сущностей по их типу."""
    result = await use_case.execute(entity_type, limit, offset)
    return ORJSONResponse([x.dict() for x in result])


@entities_router.get(
    '/search',
    response_model=list[EntityOutputDTO],
    response_class=ORJSONResponse,
    responses={401: {'model': UnauthorizedResponse}},
)
async def search_entities(
        entity_type: EntityType | None = Query(None),
        query: str = Query(...),
        limit: int = Query(250, le=1000),
        offset: int = 0,
        use_case: SearchEntitiesUseCase = Depends(get_search_entities_use_case)
):
    """Ищет сущности по названию и типу.

    Case-insensitive. Если тип не указан, ищет по всем сущностям."""
    result = await use_case.execute(query, entity_type, limit, offset)
    return ORJSONResponse([x.dict() for x in result])


@entities_router.get(
    '/{entity_id}',
    response_model=EntityOutputDTO,
    responses={
        401: {'model': UnauthorizedResponse},
        404: {'model': EntityNotFoundResponse}
    },
)
async def get_entity(
        entity_id: int,
        use_case: GetEntityUseCase = Depends(get_get_entity_use_case),
):
    result = await use_case.execute(entity_id)
    if result is None:
        raise EntityNotFoundError()
    return result


@entities_router.post(
    '',
    response_model=EntityOutputDTO,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def create_entity(
        input_dto: CreateEntityInputDTO,
        use_case: CreateEntityUseCase = Depends(get_create_entity_use_case),
):
    """Создает новую сущность. Требует статус editor."""
    result = await use_case.execute(input_dto)
    return EntityOutputDTO.from_orm(result)


@entities_router.put(
    '/{entity_id}',
    response_model=EntityOutputDTO,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse},
        404: {'model': EntityNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def update_entity(
        entity_id: int,
        update_dto: UpdateEntityInputDTO,
        use_case: UpdateEntityUseCase = Depends(get_update_entity_use_case),
):
    """Обновляет данные о сущности.

    Все поля в теле запроса являются необязательными,
    передавать нужно только необходимые дня обновления.
    Требует статус editor.

    """
    return await use_case.execute(entity_id, update_dto)


@entities_router.delete(
    '/{entity_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse},
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def delete_entity(
        entity_id: int,
        use_case: DeleteEntityUseCase = Depends(get_delete_entity_use_case),
):
    """Удаляет сущность. Требует статус editor."""
    await use_case.execute(entity_id)
    return OkResponse()
