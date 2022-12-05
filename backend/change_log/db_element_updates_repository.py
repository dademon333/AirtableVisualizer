from change_log.dto import DBElementUpdateDBInsertDTO, \
    DBElementUpdateDBUpdateDTO
from infrastructure.db import BaseRepository, DBElementUpdate


class DBElementUpdatesRepository(
    BaseRepository[
        DBElementUpdate,
        DBElementUpdateDBInsertDTO,
        DBElementUpdateDBUpdateDTO,
    ]
):
    model = DBElementUpdate
