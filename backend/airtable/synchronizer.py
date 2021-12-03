import json
import time
import traceback

from airtable.modules import synchronize_courses, synchronize_themes, synchronize_knowledges, synchronize_quantums, \
    synchronize_targets, synchronize_tasks, synchronize_metrics, synchronize_activities, synchronize_skills, \
    synchronize_competences, synchronize_professions, synchronize_competences_suos
from api.modules import get_all_courses, get_entire_course
from utils.psql_utils import get_psql_cursor
from utils.redis_utils import get_redis_cursor


async def airtable_synchronizer():
    """Синхронизирует все локальные таблицы в базе данных с airtable"""
    while True:
        try:
            psql_cursor = get_psql_cursor()
            await synchronize_database(psql_cursor)
            update_caches(psql_cursor)
            time.sleep(300 - (time.time() % 300))
        except:
            traceback.print_exc()
            time.sleep(300 - (time.time() % 300))


async def synchronize_database(psql_cursor):
    await synchronize_courses(psql_cursor)
    await synchronize_themes(psql_cursor)
    await synchronize_knowledges(psql_cursor)
    await synchronize_quantums(psql_cursor)
    await synchronize_targets(psql_cursor)
    await synchronize_tasks(psql_cursor)
    await synchronize_metrics(psql_cursor)
    await synchronize_activities(psql_cursor)
    await synchronize_skills(psql_cursor)
    await synchronize_competences(psql_cursor)
    await synchronize_professions(psql_cursor)
    await synchronize_competences_suos(psql_cursor)


def update_caches(psql_cursor):
    redis_cursor = get_redis_cursor()

    all_courses = get_all_courses(psql_cursor)
    redis_cursor.set('cache:all_courses', json.dumps(all_courses, ensure_ascii=False))

    for course in all_courses['courses']:
        course_id = course['id']
        entire_course = get_entire_course(course_id, psql_cursor)
        redis_cursor.set(f'cache:courses:{course_id}', json.dumps(entire_course, ensure_ascii=False))
