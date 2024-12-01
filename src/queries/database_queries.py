# src/queries/database_queries.py

from peewee import fn, prefetch
from src.db.database import database
from src.db.models.event import Event
from src.db.models.event_data import EventData
from src.db.models.metadata import Metadata
import logging

logger = logging.getLogger(__name__)

def get_all_events():
    """
    Consulta 1:
    Mostrar todos os eventos com suas datas, localização e tipo de evento.
    """
    try:
        prefetch_query = prefetch(
            Event.select().order_by(Event.name),
            EventData.select().order_by(EventData.date)
        )

        results = []
        event_count = 0
        eventdata_count = 0

        for event in prefetch_query:
            event_count += 1
            for event_data in event.data:
                eventdata_count += 1
                results.append({
                    'Nome': event.name,
                    'Tipo': event.type,
                    'Descrição': event.description,
                    'Data': event_data.date.strftime('%Y-%m-%d'),
                    'Localização': event_data.location
                })

        logger.info(f"Total de eventos: {event_count}")
        logger.info(f"Total de dados de eventos: {eventdata_count}")
        return results

    except Exception as e:
        logger.exception("Erro ao obter todos os eventos.")
        return []

def get_upcoming_events(limit=2):
    """
    Consulta 2:
    Mostrar os dados dos 2 eventos mais próximos de iniciar.
    """
    try:
        today = fn.DATE('now')
        query = (EventData
                 .select(Event, EventData)
                 .join(Event)
                 .where(EventData.date >= today)
                 .order_by(EventData.date)
                 .limit(limit))
        results = []
        for event_data in query:
            results.append({
                'Nome': event_data.event.name,
                'Tipo': event_data.event.type,
                'Descrição': event_data.event.description,
                'Data': event_data.date.strftime('%Y-%m-%d'),
                'Localização': event_data.location
            })
        return results
    except Exception as e:
        logger.exception("Erro ao obter eventos próximos.")
        return []

def get_events_in_rio():
    """
    Consulta 3:
    Mostrar os eventos que acontecem no Rio de Janeiro.
    """
    try:
        query = (
            Event
            .select(Event, EventData)
            .join(EventData)
            .where(EventData.location ** "%Rio de Janeiro%")  # Busca insensível a maiúsculas/minúsculas
            .order_by(Event.name)
        )
        results = []
        event_count = 0
        eventdata_count = 0
        for event in query:
            event_count += 1
            for event_data in event.data:  # Corrigido para 'data'
                if "Rio de Janeiro" in event_data.location:
                    eventdata_count += 1
                    results.append({
                        'Nome': event.name,
                        'Tipo': event.type,
                        'Descrição': event.description,
                        'Data': event_data.date.strftime('%Y-%m-%d'),
                        'Localização': event_data.location
                    })
        logger.info(f"Total de eventos no Rio de Janeiro: {event_count}")
        logger.info(f"Total de dados de eventos no Rio de Janeiro: {eventdata_count}")
        return results
    except Exception as e:
        logger.exception("Erro ao obter eventos no Rio de Janeiro.")
        return []

def get_outdoor_events():
    """
    Consulta 4:
    Mostrar todos os eventos que são ao ar livre.
    Presume-se que há uma metadata 'event_type' com valor 'Ao ar livre'.
    """
    try:
        query = (Event
                 .select(Event, EventData, Metadata)
                 .join(EventData)
                 .switch(Event)
                 .join(Metadata)
                 .where((Metadata.key == 'event_type') & (Metadata.value == 'Ao ar livre'))
                 .order_by(Event.name))
        results = []
        for event in query:
            for event_data in event.eventdata:
                results.append({
                    'Nome': event.name,
                    'Tipo': event.type,
                    'Descrição': event.description,
                    'Data': event_data.date.strftime('%Y-%m-%d'),
                    'Localização': event_data.location,
                    'Tipo de Evento': 'Ao ar livre'
                })
        return results
    except Exception as e:
        logger.exception("Erro ao obter eventos ao ar livre.")
        return []

def get_metadata_per_event():
    """
    Consulta 5:
    Mostrar todos os Metadados por evento.
    """
    try:
        query = (Metadata
                 .select(Metadata, Event)
                 .join(Event)
                 .order_by(Event.name, Metadata.key))
        results = {}
        for metadata in query:
            event_name = metadata.event.name
            if event_name not in results:
                results[event_name] = {}
            results[event_name][metadata.key] = metadata.value
        return results
    except Exception as e:
        logger.exception("Erro ao obter metadados por evento.")
        return {}
