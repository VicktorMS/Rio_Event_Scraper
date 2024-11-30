from peewee import Model, ForeignKeyField, CharField, TextField, DateTimeField, AutoField
from src.db.models.event import Event
from src.db.database import database
import datetime

class Metadata(Model):
    id = AutoField()  
    event = ForeignKeyField(Event, backref='metadata', on_delete='CASCADE') 
    key = CharField()  # Metadata key
    value = TextField() 
    updated_at = DateTimeField(default=datetime.datetime.utcnow)  

    class Meta:
        database = database 
        table_name = 'metadata' 
        indexes = (
            (('event', 'key'), True),
        )

    def __str__(self):
        return f"Metadata(id={self.id}, event={self.event.name}, key={self.key}, value={self.value})"
