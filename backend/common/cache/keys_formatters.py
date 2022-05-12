def get_course_key(course_id: int) -> str:
    return f'cache:course:{course_id}'


def get_all_courses_key(exclude_hidden: bool = False) -> str:
    if exclude_hidden:
        return 'cache:all_courses_without_hidden'
    else:
        return 'cache:all_courses'


def get_entities_types_connection_key(connection_id: int) -> str:
    return f'cache:entities_types_connections:{connection_id}'
