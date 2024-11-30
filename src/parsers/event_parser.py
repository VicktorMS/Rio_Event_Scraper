from bs4 import BeautifulSoup
import logging
import json

class EventParser:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def parse_events_from_html(self, html_content):
        """
        Extrai eventos dos scripts JSON-LD presentes no conteúdo HTML.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        scripts = soup.find_all('script', type='application/ld+json')
        events = []

        self.logger.info(f"Encontrados {len(scripts)} scripts JSON-LD")

        for script in scripts:
            try:
                data = json.loads(script.string)
                # Verifica se o script descreve um Evento
                if isinstance(data, list):
                    for item in data:
                        if item.get('@type') == 'Event':
                            event = self.extract_event_data(item)
                            if event:
                                events.append(event)
                elif data.get('@type') == 'Event':
                    event = self.extract_event_data(data)
                    if event:
                        events.append(event)
            except json.JSONDecodeError as e:
                self.logger.warning(f"Erro ao decodificar JSON-LD: {e}")
                continue
            except Exception as e:
                self.logger.error(f"Erro ao processar JSON-LD: {e}")
                continue

        self.logger.info(f"{len(events)} eventos extraídos dos scripts JSON-LD.")
        return events
    
    def extract_event_data(self, data):
        """
        Extrai informações relevantes de um objeto JSON-LD de tipo 'Event'.
        """
        try:
            name = data.get('name')
            event_type = data.get('@type')  # Corrigido para '@type'
            description = data.get('description')
            start_date = data.get('startDate')
            end_date = data.get('endDate')
            location = data.get('location', {}).get('name')
            address = data.get('location', {}).get('address')
            image = data.get('image')
            url = data.get('url')
            offers = data.get('offers', {})
            price = offers.get('price')
            price_currency = offers.get('priceCurrency')
            availability = offers.get('availability')

            # Validação dos campos obrigatórios
            if not all([name, event_type, start_date]):
                self.logger.warning(f"Evento incompleto: {data}")
                return None

            event = {
                'name': name,
                'type': event_type,
                'description': description,
                'start_date': start_date,
                'end_date': end_date,
                'location': location,
                'address': address,
                'image': image,
                'url': url,
                'price': price,
                'price_currency': price_currency,
                'availability': availability
            }
            self.logger.debug(f"Evento extraído: {event}")
            return event
        except Exception as e:
            self.logger.error(f"Erro ao extrair dados do evento: {e}")
            return None