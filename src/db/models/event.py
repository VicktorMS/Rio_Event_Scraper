import datetime
from peewee import Model, CharField, TextField, DateTimeField, AutoField
from src.db.database import database

class Event(Model):
    id = AutoField() 
    name = CharField(unique=True)
    type = TextField()  # Armazena o tipo do evento
    description = CharField(null=True) 
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = database
        table_name = 'event'

    def __str__(self):
        return self.name
