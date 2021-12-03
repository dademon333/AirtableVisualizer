from typing import Any

from psycopg2.extras import DictCursor


def get_all_courses(psql_cursor):
    return {
        'courses': get_courses(psql_cursor),
        'themes': get_themes(psql_cursor),
        'knowledges': get_knowledges(psql_cursor),
        'quantums': get_quantums(psql_cursor),
        'competences': get_competences(psql_cursor)
    }


def get_entire_course(course_id, psql_cursor):
    psql_cursor.execute('SELECT * FROM courses WHERE id = %s', [course_id])
    course = psql_cursor.fetchone()

    if course is None:
        return None

    themes = get_themes(psql_cursor, course_id)
    knowledges = get_knowledges(psql_cursor, themes)
    quantums = get_quantums(psql_cursor, knowledges)
    targets = get_targets(psql_cursor, knowledges)
    tasks = get_tasks(psql_cursor, targets)
    metrics = get_metrics(psql_cursor, targets)
    activities = get_activities(psql_cursor, targets)
    skills = get_skills(psql_cursor, activities)
    competences = get_competences(psql_cursor, skills)
    professions = get_professions(psql_cursor, competences)
    suos_competences = get_suos_competences(psql_cursor, competences)

    return {
        'id': course['id'],
        'name': course['name'],
        'themes': themes,
        'knowledges': knowledges,
        'quantums': quantums,
        'targets': targets,
        'metrics': metrics,
        'tasks': tasks,
        'activities': activities,
        'skills': skills,
        'competences': competences,
        'professions': professions,
        'suosCompetences': suos_competences
    }


def add_parents_links(
        children: list[dict[Any, Any]],
        connections_table: str,
        child_column: str,
        parent_column: str,
        link_field: str,
        psql_cursor: DictCursor,
):
    """Добавляет к записям ссылки на родительские элементы
    Например, к темам ссылки на их курсы

    :param children: Элементы для обработки
    :param connections_table: Название таблицы связей
    :param child_column: Название колонки в таблице с id потомков
    :param parent_column: Название колонки в таблице с id родителей
    :param link_field: Атрибут, в котором будут храниться ссылки на родителей
    :param psql_cursor: Курсор postgresql
    """
    psql_cursor.execute(f'SELECT * FROM {connections_table}')
    connections = psql_cursor.fetchall()

    for child in children:
        child[link_field] = [
            x[parent_column] for x in connections if x[child_column] == child['id']
        ]


def get_courses(psql_cursor):
    psql_cursor.execute('SELECT * FROM courses')
    return psql_cursor.fetchall()


def get_themes(psql_cursor, course_id=None):
    if course_id is None:
        psql_cursor.execute('SELECT * FROM themes')
    else:
        psql_cursor.execute('''
            SELECT themes.*
            FROM courses
            INNER JOIN themes_courses_connections
            ON courses.id = themes_courses_connections.course
            INNER JOIN themes
            ON themes.id = themes_courses_connections.theme
            WHERE courses.id = %s
        ''', [course_id])

    themes = psql_cursor.fetchall()
    add_parents_links(
        children=themes,
        connections_table='themes_themes_connections',
        child_column='theme',
        parent_column='top_level_theme',
        link_field='topLevelThemes',
        psql_cursor=psql_cursor
    )
    add_parents_links(
        children=themes,
        connections_table='themes_courses_connections',
        child_column='theme',
        parent_column='course',
        link_field='courses',
        psql_cursor=psql_cursor
    )
    return themes


def get_knowledges(psql_cursor, themes=None):
    if themes is None:
        psql_cursor.execute('SELECT * FROM knowledges')
        knowledges = psql_cursor.fetchall()

    elif len(themes) > 0:
        psql_cursor.execute('''
            SELECT knowledges.*
            FROM themes
            INNER JOIN knowledges_themes_connections
            ON themes.id = knowledges_themes_connections.theme
            INNER JOIN knowledges
            ON knowledges.id = knowledges_themes_connections.knowledge
            WHERE themes.id IN %s
        ''', [tuple(x['id'] for x in themes)])
        knowledges = psql_cursor.fetchall()

    else:
        knowledges = []

    add_parents_links(
        children=knowledges,
        connections_table='knowledges_quantums_connections',
        child_column='knowledge',
        parent_column='quantum',
        link_field='quantums',
        psql_cursor=psql_cursor
    )
    add_parents_links(
        children=knowledges,
        connections_table='knowledges_themes_connections',
        child_column='knowledge',
        parent_column='theme',
        link_field='themes',
        psql_cursor=psql_cursor
    )
    return knowledges


def get_quantums(psql_cursor, knowledges=None):
    if knowledges is None:
        psql_cursor.execute('SELECT * FROM quantums')
        quantums = psql_cursor.fetchall()

    elif len(knowledges) > 0:
        psql_cursor.execute('''
            SELECT quantums.*
            FROM knowledges
            INNER JOIN knowledges_quantums_connections
            ON knowledges.id = knowledges_quantums_connections.knowledge
            INNER JOIN quantums
            ON quantums.id = knowledges_quantums_connections.quantum
            WHERE knowledges.id IN %s
        ''', [tuple(x['id'] for x in knowledges)])
        quantums = psql_cursor.fetchall()

    else:
        quantums = []

    return quantums


def get_targets(psql_cursor, knowledges=None):
    if knowledges is None:
        psql_cursor.execute('SELECT * FROM targets')
        targets = psql_cursor.fetchall()

    elif len(knowledges) > 0:
        psql_cursor.execute('''
            SELECT targets.*
            FROM knowledges
            INNER JOIN targets_knowledges_connections
            ON knowledges.id = targets_knowledges_connections.knowledge
            INNER JOIN targets
            ON targets.id = targets_knowledges_connections.target
            WHERE knowledges.id IN %s
        ''', [tuple(x['id'] for x in knowledges)])
        targets = psql_cursor.fetchall()

    else:
        targets = []

    add_parents_links(
        children=targets,
        connections_table='targets_knowledges_connections',
        child_column='target',
        parent_column='knowledge',
        link_field='knowledges',
        psql_cursor=psql_cursor
    )
    add_parents_links(
        children=targets,
        connections_table='targets_metrics_connections',
        child_column='target',
        parent_column='metric',
        link_field='metrics',
        psql_cursor=psql_cursor
    )
    return targets


def get_metrics(psql_cursor, targets=None):
    if targets is None:
        psql_cursor.execute('SELECT * FROM metrics')
        metrics = psql_cursor.fetchall()

    elif len(targets) > 0:
        psql_cursor.execute('''
            SELECT metrics.*
            FROM targets
            INNER JOIN targets_metrics_connections
            ON targets.id = targets_metrics_connections.target
            INNER JOIN metrics
            ON metrics.id = targets_metrics_connections.metric
            WHERE targets.id IN %s
        ''', [tuple(x['id'] for x in targets)])
        metrics = psql_cursor.fetchall()

    else:
        metrics = []

    return metrics


def get_tasks(psql_cursor, targets=None):
    if targets is None:
        psql_cursor.execute('SELECT * FROM tasks')
        tasks = psql_cursor.fetchall()

    elif len(targets) > 0:
        psql_cursor.execute('''
            SELECT tasks.*
            FROM targets
            INNER JOIN tasks_targets_connections
            ON targets.id = tasks_targets_connections.target
            INNER JOIN tasks
            ON tasks.id = tasks_targets_connections.task
            WHERE targets.id IN %s
        ''', [tuple(x['id'] for x in targets)])
        tasks = psql_cursor.fetchall()

    else:
        tasks = []

    add_parents_links(
        children=tasks,
        connections_table='tasks_targets_connections',
        child_column='task',
        parent_column='target',
        link_field='targets',
        psql_cursor=psql_cursor
    )
    return tasks


def get_activities(psql_cursor, targets=None):
    if targets is None:
        psql_cursor.execute('SELECT * FROM activities')
        activities = psql_cursor.fetchall()

    elif len(targets) > 0:
        psql_cursor.execute('''
            SELECT activities.*
            FROM targets
            INNER JOIN activities_targets_connections
            ON targets.id = activities_targets_connections.target
            INNER JOIN activities
            ON activities.id = activities_targets_connections.activity
            WHERE targets.id IN %s
        ''', [tuple(x['id'] for x in targets)])
        activities = psql_cursor.fetchall()

    else:
        activities = []

    add_parents_links(
        children=activities,
        connections_table='activities_activities_connections',
        child_column='activity',
        parent_column='top_level_activity',
        link_field='topLevelActivities',
        psql_cursor=psql_cursor
    )
    add_parents_links(
        children=activities,
        connections_table='activities_targets_connections',
        child_column='activity',
        parent_column='target',
        link_field='targets',
        psql_cursor=psql_cursor
    )
    return activities


def get_skills(psql_cursor, activities=None):
    if activities is None:
        psql_cursor.execute('SELECT * FROM skills')
        skills = psql_cursor.fetchall()

    elif len(activities) > 0:
        psql_cursor.execute('''
            SELECT skills.*
            FROM activities
            INNER JOIN skills_activities_connections
            ON activities.id = skills_activities_connections.activity
            INNER JOIN skills
            ON skills.id = skills_activities_connections.skill
            WHERE activities.id IN %s
        ''', [tuple(x['id'] for x in activities)])
        skills = psql_cursor.fetchall()

    else:
        skills = []

    add_parents_links(
        children=skills,
        connections_table='skills_activities_connections',
        child_column='skill',
        parent_column='activity',
        link_field='activities',
        psql_cursor=psql_cursor
    )
    return skills


def get_competences(psql_cursor, skills=None):
    if skills is None:
        psql_cursor.execute('SELECT * FROM competences')
        competences = psql_cursor.fetchall()

    elif len(skills) > 0:
        psql_cursor.execute('''
            SELECT competences.*
            FROM skills
            INNER JOIN competences_skills_connections
            ON skills.id = competences_skills_connections.skill
            INNER JOIN competences
            ON competences.id = competences_skills_connections.competence
            WHERE skills.id IN %s
        ''', [tuple(x['id'] for x in skills)])
        competences = psql_cursor.fetchall()

    else:
        competences = []

    add_parents_links(
        children=competences,
        connections_table='competences_competences_connections',
        child_column='competence',
        parent_column='top_level_competence',
        link_field='topLevelCompetences',
        psql_cursor=psql_cursor
    )
    add_parents_links(
        children=competences,
        connections_table='competences_skills_connections',
        child_column='competence',
        parent_column='skill',
        link_field='skills',
        psql_cursor=psql_cursor
    )
    add_parents_links(
        children=competences,
        connections_table='competences_knowledges_connections',
        child_column='competence',
        parent_column='knowledge',
        link_field='knowledges',
        psql_cursor=psql_cursor
    )
    return competences


def get_professions(psql_cursor, competences=None):
    if competences is None:
        psql_cursor.execute('SELECT * FROM professions')
        professions = psql_cursor.fetchall()

    elif len(competences) > 0:
        psql_cursor.execute('''
            SELECT professions.*
            FROM competences
            INNER JOIN professions_competences_connections
            ON competences.id = professions_competences_connections.competence
            INNER JOIN professions
            ON professions.id = professions_competences_connections.profession
            WHERE competences.id IN %s
        ''', [tuple(x['id'] for x in competences)])
        professions = psql_cursor.fetchall()

    else:
        professions = []

    add_parents_links(
        children=professions,
        connections_table='professions_competences_connections',
        child_column='profession',
        parent_column='competence',
        link_field='competences',
        psql_cursor=psql_cursor
    )
    return professions


def get_suos_competences(psql_cursor, competences=None):
    if competences is None:
        psql_cursor.execute('SELECT * FROM suos_competences')
        suos_competences = psql_cursor.fetchall()

    elif len(competences) > 0:
        psql_cursor.execute('''
            SELECT suos_competences.*
            FROM competences
            INNER JOIN suos_competences_competences_connections
            ON competences.id = suos_competences_competences_connections.competence
            INNER JOIN suos_competences
            ON suos_competences.id = suos_competences_competences_connections.suos_competence
            WHERE competences.id IN %s
        ''', [tuple(x['id'] for x in competences)])
        suos_competences = psql_cursor.fetchall()

    else:
        suos_competences = []

    add_parents_links(
        children=suos_competences,
        connections_table='suos_competences_competences_connections',
        child_column='suos_competence',
        parent_column='competence',
        link_field='competences',
        psql_cursor=psql_cursor
    )
    return suos_competences
