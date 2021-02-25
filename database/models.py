import database
from datetime import datetime
from peewee import Model, DateTimeField, CharField
from playhouse.postgres_ext import JSONField


class BaseModel(Model):

    created_at = DateTimeField(
        verbose_name='Datetime of creating object',
        default=datetime.now,
        index=True)

    updated_at = DateTimeField(
        verbose_name='Datetime of updating object',
        default=datetime.now,
    )

    class Meta:
        database = database.db_client

    def save(self, force_insert=False, only=None):
        self.updated_at = datetime.now()
        return super().save(force_insert=force_insert, only=only)


class GameObject(BaseModel):
    name = CharField(
        verbose_name='Unique name of game object',
        index=True,
        unique=True
    )
    params = JSONField(verbose_name='Available params for object', default="")
