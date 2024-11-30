from src.db.database import database
from src.db.models import Event, EventData, Metadata  

def initialize_db():
    """Connect to Database and Create New Tables"""
    with database:
        database.create_tables([Event, EventData, Metadata], safe=True)
        print("Tables successfully created.")