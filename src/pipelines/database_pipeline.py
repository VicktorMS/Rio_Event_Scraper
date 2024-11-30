# src/pipelines/database_pipeline.py
from src.db.models.event import Event
from src.db.models.event_data import EventData
from src.db.models.metadata import Metadata
from peewee import IntegrityError
import logging
from datetime import datetime

class DatabasePipeline:
    def __init__(self):
        # Configuração de logging para o pipeline
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.__class__.__name__)

    def process_events(self, events):
        for event_data in events:
            try:
                with Event._meta.database.atomic():
                    # Processar Event
                    event = self.process_event(event_data)
                    
                    # Processar EventData
                    self.process_event_data(event, event_data)
                    
                    # Processar Metadata
                    self.process_metadata(event, event_data)
                    
            except IntegrityError as e:
                self.logger.error(f"Erro de integridade ao salvar o evento '{event_data['name']}': {e}")
                continue
            except Exception as e:
                self.logger.error(f"Erro inesperado ao processar o evento '{event_data['name']}': {e}")
                continue

    def process_event(self, event_data):
        """
        Cria ou atualiza um registro na tabela Event.
        Retorna a instância do Event.
        """
        event, created = Event.get_or_create(
            name=event_data['name'],
            defaults={
                'type': event_data['type'],
                'description': event_data['description'],
            }
        )
        if created:
            self.logger.info(f"Evento '{event.name}' criado.")
        else:
            self.logger.info(f"Evento '{event.name}' já existe. Atualizando informações.")
            event.type = event_data['type']
            event.description = event_data['description']
            event.save()
            self.logger.info(f"Evento '{event.name}' atualizado.")
        return event

    def process_event_data(self, event, event_data):
        """
        Cria ou atualiza um registro na tabela EventData.
        """
        start_date = self.parse_date(event_data.get('start_date'))
        end_date = self.parse_date(event_data.get('end_date')) if event_data.get('end_date') else None

        if start_date:
            # Verificar se já existe um EventData para este evento e data
            try:
                event_data_entry = EventData.get(
                    (EventData.event == event) &
                    (EventData.date == start_date)
                )
                self.logger.info(f"EventData para '{event.name}' na data {start_date} já existe. Atualizando informações.")
                event_data_entry.location = self.format_location(event_data)
                event_data_entry.save()
            except EventData.DoesNotExist:
                # Criar um novo EventData
                event_data_entry = EventData.create(
                    event=event,
                    date=start_date,
                    location=self.format_location(event_data)
                )
                self.logger.info(f"EventData para '{event.name}' na data {start_date} criado.")

    def process_metadata(self, event, event_data):
        """
        Cria múltiplas entradas na tabela Metadata para cada evento.
        """
        # Defina quais campos devem ser tratados como metadata
        metadata_fields = {
            'price': event_data.get('price'),
            'price_currency': event_data.get('price_currency'),
            'availability': event_data.get('availability'),
            'image': event_data.get('image'),
            'url': event_data.get('url')
        }

        for key, value in metadata_fields.items():
            if value is not None:
                metadata, meta_created = Metadata.get_or_create(
                    event=event,
                    key=key,
                    defaults={'value': value}
                )
                if meta_created:
                    self.logger.info(f"Metadata '{key}' para '{event.name}' criado com valor '{value}'.")
                else:
                    self.logger.info(f"Metadata '{key}' para '{event.name}' já existe. Atualizando valor para '{value}'.")
                    metadata.value = value
                    metadata.save()

    def parse_date(self, date_str):
        """
        Converte uma string de data para um objeto datetime.
        """
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            self.logger.warning(f"Formato de data desconhecido: {date_str}")
            return None

    def format_location(self, event_data):
        """
        Formata a localização combinando 'location' e 'address'.
        """
        location = event_data.get('location', 'Desconhecido')
        address = event_data.get('address', 'Desconhecido')
        return f"{location}, {address}"
