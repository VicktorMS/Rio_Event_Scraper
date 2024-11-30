import requests
from urllib.parse import urljoin
from src.config import settings
import logging

class EventCrawler:
    def __init__(self, base_url=settings.target_url):
        self.base_url = base_url
        self.ajax_endpoint = "/wp-admin/admin-ajax.php"
        self.session = requests.Session()
        self.headers = {
            'User-Agent': f'{settings.app_name}-{settings.environment}/1.0 (+https://google.com)'
        }
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.__class__.__name__)

    def fetch_initial_page(self):
        """
        Busca por dados iniciais da página, extrai eventos de destaque diréto da página
        """
        url = self.base_url
        try:
            self.logger.info(f"Buscando a página: {url}")
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            self.logger.info(f"Página obtida com sucesso: {url}")
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"Erro ao buscar a página {url}: {e}")
            return None
        
    def fetch_events_ajax(self, action: str, start_date: str, offset: int):
        """
        Faz a simulação de uma requisição Ajax para pegar os eventos do site.
        """
        ajax_url = urljoin(self.base_url, self.ajax_endpoint)
        payload = {
            'action': action,
            'mec_start_date': start_date,
            'mec_offset': offset
        }
        
        try:
            self.logger.info(f"Enviando requisição AJAX para offset {offset}...")
            
            response = self.session.post(ajax_url, data=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            self.logger.info(f"Requisição AJAX para offset {offset} bem-sucedida.")
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Erro na requisição AJAX para offset {offset}: {e}")
            return None

    def close(self):
        self.session.close()