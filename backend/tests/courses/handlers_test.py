from httpx import AsyncClient

from courses.dto import CoursesWithConnectionsOutputDTO, \
    CourseWithConnectionsOutputDTO
from courses.exceptions import CourseNotFoundResponse, NotACourseResponse
from infrastructure.db import Entity, EntityConnection


async def test_list_courses_success(
        test_client: AsyncClient,
        entity_course_list_in_db: list[Entity],
):
    result = await test_client.get('/api/courses/list')
    assert len(result.json()) == len(entity_course_list_in_db)


async def test_get_all_courses_success(
        test_client: AsyncClient,
        entity_course_list_in_db: list[Entity],
        entity_theme_list_in_db: list[Entity],
        entity_connection_list_in_db: list[EntityConnection],

):
    result = await test_client.get('/api/courses/all')
    result = CoursesWithConnectionsOutputDTO.parse_obj(result.json())
    assert len(result.courses) == len(entity_course_list_in_db)
    assert len(result.entities) == len(
        entity_course_list_in_db + entity_theme_list_in_db
    )
    assert len(result.entity_connections) == len(entity_connection_list_in_db)


async def test_get_course_success(
        test_client: AsyncClient,
        entity_course_list_in_db: list[Entity],
        entity_theme_list_in_db: list[Entity],
        entity_connection_list_in_db: list[EntityConnection],
):
    result = await test_client.get(
        f'/api/courses/{entity_course_list_in_db[0].id}'
    )
    result = CourseWithConnectionsOutputDTO.parse_obj(result.json())

    themes_per_course = len(entity_theme_list_in_db) / len(
        entity_course_list_in_db
    )

    assert result.id == entity_course_list_in_db[0].id
    assert len(result.entities) == 1 + themes_per_course
    assert len(result.entity_connections) == themes_per_course


async def test_get_course_not_a_course(
        entity_theme_in_db: Entity,
        test_client: AsyncClient,
):
    result = await test_client.get(
        f'/api/courses/{entity_theme_in_db.id}'
    )
    assert result.status_code == 400
    assert result.json()['detail'] == NotACourseResponse().detail


async def test_get_course_not_found(
        test_client: AsyncClient,
):
    result = await test_client.get(
        f'/api/courses/123'
    )
    assert result.status_code == 404
    assert result.json()['detail'] == CourseNotFoundResponse().detail

