import peewee_async
from conf import settings, Settings


def _init_clients(params: Settings):
    db = peewee_async.PostgresqlDatabase(
        params.DB.DATABASE,
        host=params.DB.HOST,
        user=params.DB.USER,
        password=params.DB.PASSWORD
    )
    return db, peewee_async.Manager(db)


db_client, db_manager = _init_clients(settings)
