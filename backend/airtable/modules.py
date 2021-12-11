import asyncio
import re
import time
from typing import Any

import aiohttp
from psycopg2.extras import DictCursor

from tokens import Tokens


async def list_airtable_page(table_name, offset=None):
    """Возвращает записи из таблицы airtable с учетом offset"""
    async with aiohttp.ClientSession() as session:
        await asyncio.sleep(0.2 - (time.time() % 0.2))  # Максимум 1 запрос в 0.2 сек, чтобы не словить лимит
        headers = {
            'Authorization': f'Bearer {Tokens.AIRTABLE_TOKEN}'
        }
        if offset is None:
            url = f'https://api.airtable.com/v0/{Tokens.AIRTABLE_DATABASE_ID}/{table_name}'
        else:
            url = f'https://api.airtable.com/v0/{Tokens.AIRTABLE_DATABASE_ID}/{table_name}?offset={offset}'
        response = await session.get(url, headers=headers)
        response = await response.json()
        return response


async def list_airtable_table_records(table_name):
    """Возвращает все записи в airtable для таблицы table_name"""
    records = []
    response = await list_airtable_page(table_name)
    records.extend(response['records'])
    while 'offset' in response:
        response = await list_airtable_page(table_name, offset=response['offset'])
        records.extend(response['records'])

    return records


def filter_empty_records(
        records: list[dict[Any, Any]],
        name_column: str
):
    """Удаляет из records записи, у которых нет имени
    Также убирает все знаки переноса строки в начале и конце названия
    """
    filtered_records = []
    for record in records:
        if name_column in record['fields']:
            record['fields'][name_column] = re.sub(r"\n+(?<=\Z)", "", record['fields'][name_column])
            record['fields'][name_column] = re.sub(r"(?=\A)\n+", "", record['fields'][name_column])
            filtered_records.append(record)

    return filtered_records


def get_new_records(
        local_records: list[dict[Any, Any]],
        airtable_records: list[dict[Any, Any]]
):
    """Возвращает записи, которых ещё нет в базе данных"""
    local_records_ids = [x['id'] for x in local_records]
    return [record for record in airtable_records if record['id'] not in local_records_ids]


def get_deprecated_records(
        local_records: list[dict[Any, Any]],
        airtable_records: list[dict[Any, Any]]
):
    """Возвращает список идентификаторов записей, которые удалены в airtable, но остались в локальной базе данных"""
    airtable_records_ids = [x['id'] for x in airtable_records]
    local_records_ids = [x['id'] for x in local_records]
    return list(set(local_records_ids) - set(airtable_records_ids))


def get_updated_records(
        local_records: list[dict[Any, Any]],
        airtable_records: list[dict[Any, Any]],
        airtable_field: str,
        local_field: str
):
    """Возвращает словарь в формате id: новое_имя с записями, в которых обновились значения определенного поля"""
    updated_records = {}
    for local_record in local_records:
        new_record = [x for x in airtable_records if x['id'] == local_record['id']]
        if new_record != [] and (new_value := new_record[0]['fields'].get(airtable_field, "")) != local_record[local_field]:
            updated_records[new_record[0]['id']] = new_value

    return updated_records


def get_new_connections(
        local_connections: list[dict[str, str]],
        airtable_connections: dict[str, list[str]],
        child_column: str,
        parent_column: str
):
    """Возвращает новые связи между сущностями, которых ещё нет в базе данных"""
    result = []
    for entity_id, new_connections in airtable_connections.items():
        old_connections = [x[parent_column] for x in local_connections if x[child_column] == entity_id]
        for new_parent in set(new_connections) - set(old_connections):
            result.append({'parent': new_parent, 'child': entity_id})

    return result


def get_deprecated_connections(
        local_connections: list[dict[str, str]],
        airtable_connections: dict[str, list[str]],
        child_column: str,
        parent_column: str
):
    """Возвращает устаревшие связи между сущностями, которые удалены в airtable, но остались в локальной базе данных"""
    result = []
    for connection in local_connections:
        parent = connection[parent_column]
        child = connection[child_column]
        if parent not in airtable_connections.get(child, []):
            result.append({'parent': parent, 'child': child})

    return result


async def synchronize_table(
        psql_cursor: DictCursor,
        airtable_table: str,
        local_table: str,
        airtable_record_name_field: str,
        have_description: bool = False
):
    """Синхронизирует локальную таблицу базы данных с airtable

    :param psql_cursor: Курсор postgresql
    :param airtable_table: Название таблицы в airtable
    :param local_table: Название таблицы в локальной базе
    :param airtable_record_name_field: Название параметра в airtable, отвечающего за название строки
    :param have_description: Наличие у сущности описания
    """
    airtable_records = await list_airtable_table_records(airtable_table)
    airtable_records = filter_empty_records(airtable_records, name_column=airtable_record_name_field)
    # noinspection SqlResolve
    psql_cursor.execute(f'SELECT * FROM {local_table}')
    local_records = psql_cursor.fetchall()

    deprecated_records = get_deprecated_records(local_records, airtable_records)
    if len(deprecated_records) > 0:
        # noinspection SqlResolve
        psql_cursor.execute(f'DELETE FROM {local_table} WHERE id IN %s', [tuple(deprecated_records)])

    new_records = get_new_records(local_records, airtable_records)
    for record in new_records:
        # noinspection SqlResolve
        psql_cursor.execute(
            f'INSERT INTO {local_table} (id, name) VALUES (%s, %s)',
            [record['id'], record['fields'][airtable_record_name_field]]
        )

    # noinspection SqlResolve
    psql_cursor.execute(f'SELECT * FROM {local_table}')
    local_records = psql_cursor.fetchall()

    renamed_records = get_updated_records(
        local_records=local_records,
        airtable_records=airtable_records,
        airtable_field=airtable_record_name_field,
        local_field='name'
    )
    for record_id, new_name in renamed_records.items():
        # noinspection SqlResolve
        psql_cursor.execute(f'UPDATE {local_table} SET name = %s WHERE id = %s', [new_name, record_id])

    if have_description:
        renamed_records = get_updated_records(
            local_records=local_records,
            airtable_records=airtable_records,
            airtable_field='Описание',
            local_field='description'
        )
        for record_id, new_description in renamed_records.items():
            # noinspection SqlResolve
            psql_cursor.execute(f'UPDATE {local_table} SET description = %s WHERE id = %s', [new_description, record_id])


async def synchronize_tables_connections(
        psql_cursor: DictCursor,
        connections_table: str,
        child_column: str,
        parent_column: str,
        child_airtable_table: str,
        parent_airtable_field
):
    """Обновляет в локальной таблице связей данные о связях между сущностями

    :param psql_cursor: Курсор postgresql
    :param connections_table: Название таблицы связей в postgresql
    :param parent_column: название родительской сущности в локальной базе
    :param child_column: название подчиненной сущности в локальной базе
    :param child_airtable_table: название таблицы в airtable подчиненной сущности
    :param parent_airtable_field: название поля, указывающего на родителей сущности в airtable
    """
    airtable_connections = await list_airtable_table_records(child_airtable_table)
    airtable_connections = {x['id']: x['fields'].get(parent_airtable_field, []) for x in airtable_connections}

    psql_cursor.execute(f'SELECT * FROM {connections_table}')
    local_connections = psql_cursor.fetchall()

    deprecated_connections = get_deprecated_connections(local_connections, airtable_connections, child_column, parent_column)
    for connection in deprecated_connections:
        psql_cursor.execute(
            f'DELETE FROM {connections_table} WHERE {parent_column} = %s AND {child_column} = %s',
            [connection['parent'], connection['child']]
        )

    new_connections = get_new_connections(local_connections, airtable_connections, child_column, parent_column)
    for connection in new_connections:
        psql_cursor.execute(
            f'INSERT INTO {connections_table} VALUES (%s, %s)',
            [connection['child'], connection['parent']]
        )


async def synchronize_courses(psql_cursor):
    await synchronize_table(
        psql_cursor=psql_cursor,
        airtable_table='Курс',
        local_table='courses',
        airtable_record_name_field='Название'
    )


async def synchronize_themes(psql_cursor):
    await synchronize_table(
        psql_cursor=psql_cursor,
        airtable_table='Тема',
        local_table='themes',
        airtable_record_name_field='Название темы'
    )
    await synchronize_tables_connections(
        psql_cursor=psql_cursor,
        connections_table='themes_courses_connections',
        child_column='theme',
        parent_column='course',
        child_airtable_table='Тема',
        parent_airtable_field='Курс'
    )
    await synchronize_tables_connections(
        psql_cursor=psql_cursor,
        connections_table='themes_themes_connections',
        child_column='theme',
        parent_column='top_level_theme',
        child_airtable_table='Тема',
        parent_airtable_field='Раздел (тема верхнего уровня)'
    )


async def synchronize_knowledges(psql_cursor):
    await synchronize_table(
        psql_cursor=psql_cursor,
        airtable_table='Знание',
        local_table='knowledges',
        airtable_record_name_field='Название'
    )
    await synchronize_tables_connections(
        psql_cursor=psql_cursor,
        connections_table='knowledges_themes_connections',
        child_column='knowledge',
        parent_column='theme',
        child_airtable_table='Знание',
        parent_airtable_field='Содержится в Теме'
    )
    await synchronize_tables_connections(
        psql_cursor=psql_cursor,
        connections_table='knowledges_quantums_connections',
        child_column='knowledge',
        parent_column='quantum',
        child_airtable_table='Знание',
        parent_airtable_field='Тип (квант)'
    )


async def synchronize_quantums(psql_cursor):
    await synchronize_table(
        psql_cursor=psql_cursor,
        airtable_table='Кванты знаний',
        local_table='quantums',
        airtable_record_name_field='Название',
        have_description=True
    )


async def synchronize_targets(psql_cursor):
    await synchronize_table(
        psql_cursor=psql_cursor,
        airtable_table='Цель(задания)',
        local_table='targets',
        airtable_record_name_field='Название'
    )
    await synchronize_tables_connections(
        psql_cursor=psql_cursor,
        connections_table='targets_metrics_connections',
        child_column='target',
        parent_column='metric',
        child_airtable_table='Цель(задания)',
        parent_airtable_field='Метрика'
    )
    await synchronize_tables_connections(
        psql_cursor=psql_cursor,
        connections_table='targets_knowledges_connections',
        child_column='target',
        parent_column='knowledge',
        child_airtable_table='Цель(задания)',
        parent_airtable_field='Необходимые знания'
    )


async def synchronize_tasks(psql_cursor):
    await synchronize_table(
        psql_cursor=psql_cursor,
        airtable_table='Задание',
        local_table='tasks',
        airtable_record_name_field='Название',
        have_description=True
    )
    await synchronize_tables_connections(
        psql_cursor=psql_cursor,
        connections_table='tasks_targets_connections',
        child_column='task',
        parent_column='target',
        child_airtable_table='Задание',
        parent_airtable_field='Цель'
    )


async def synchronize_metrics(psql_cursor):
    await synchronize_table(
        psql_cursor=psql_cursor,
        airtable_table='Метрика',
        local_table='metrics',
        airtable_record_name_field='Название',
        have_description=True
    )


async def synchronize_activities(psql_cursor):
    await synchronize_table(
        psql_cursor=psql_cursor,
        airtable_table='Деятельность',
        local_table='activities',
        airtable_record_name_field='Название деятельности'
    )
    await synchronize_tables_connections(
        psql_cursor=psql_cursor,
        connections_table='activities_activities_connections',
        child_column='activity',
        parent_column='top_level_activity',
        child_airtable_table='Деятельность',
        parent_airtable_field='Родительская деятельность'
    )
    await synchronize_tables_connections(
        psql_cursor=psql_cursor,
        connections_table='activities_targets_connections',
        child_column='activity',
        parent_column='target',
        child_airtable_table='Деятельность',
        parent_airtable_field='Цель(задания)'
    )


async def synchronize_skills(psql_cursor):
    await synchronize_table(
        psql_cursor=psql_cursor,
        airtable_table='Навык',
        local_table='skills',
        airtable_record_name_field='Название'
    )
    await synchronize_tables_connections(
        psql_cursor=psql_cursor,
        connections_table='skills_activities_connections',
        child_column='skill',
        parent_column='activity',
        child_airtable_table='Навык',
        parent_airtable_field='Деятельность'
    )


async def synchronize_competences(psql_cursor):
    await synchronize_table(
        psql_cursor=psql_cursor,
        airtable_table='Компетенция',
        local_table='competences',
        airtable_record_name_field='Название компетенции'
    )
    await synchronize_tables_connections(
        psql_cursor=psql_cursor,
        connections_table='competences_competences_connections',
        child_column='competence',
        parent_column='top_level_competence',
        child_airtable_table='Компетенция',
        parent_airtable_field='Родительская компетенция'
    )
    await synchronize_tables_connections(
        psql_cursor=psql_cursor,
        connections_table='competences_skills_connections',
        child_column='competence',
        parent_column='skill',
        child_airtable_table='Компетенция',
        parent_airtable_field='Навыки'
    )
    await synchronize_tables_connections(
        psql_cursor=psql_cursor,
        connections_table='competences_knowledges_connections',
        child_column='competence',
        parent_column='knowledge',
        child_airtable_table='Компетенция',
        parent_airtable_field='Знания'
    )


async def synchronize_professions(psql_cursor):
    await synchronize_table(
        psql_cursor=psql_cursor,
        airtable_table='Профессия',
        local_table='professions',
        airtable_record_name_field='Название'
    )
    await synchronize_tables_connections(
        psql_cursor=psql_cursor,
        connections_table='professions_competences_connections',
        child_column='profession',
        parent_column='competence',
        child_airtable_table='Профессия',
        parent_airtable_field='Компетенции'
    )


async def synchronize_competences_suos(psql_cursor):
    await synchronize_table(
        psql_cursor=psql_cursor,
        airtable_table='Компетенции СУОС',
        local_table='suos_competences',
        airtable_record_name_field='Название'
    )
    await synchronize_tables_connections(
        psql_cursor=psql_cursor,
        connections_table='suos_competences_competences_connections',
        child_column='suos_competence',
        parent_column='competence',
        child_airtable_table='Компетенции СУОС',
        parent_airtable_field='Компетенция'
    )
