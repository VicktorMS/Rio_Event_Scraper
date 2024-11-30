from peewee import Model, ForeignKeyField, TextField, DateTimeField, AutoField
from src.db.models.event import Event
from src.db.database import database

class EventData(Model):
    id = AutoField()  
    event = ForeignKeyField(Event, backref='data', on_delete='CASCADE')
    date = DateTimeField()
    location = TextField() 

    class Meta:
        database = database  
        table_name = 'event_data' 
        indexes = (
            (('event', 'date'), True), 
        )

    def __str__(self):
        return f"EventData(id={self.id}, event={self.event.name}, date={self.date}, location={self.location})"
