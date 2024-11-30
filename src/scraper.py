from datetime import datetime, timedelta
from src.db.init_db import initialize_db
from src.crawlers.event_crawler import EventCrawler
from src.db.database import database
from src.config import settings
import logging
from src.parsers.event_parser import EventParser
from src.pipelines.database_pipeline import DatabasePipeline


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Formato dos logs
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # Handler para console
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Handler para arquivo
    fh = logging.FileHandler(settings.scraper_log)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def scraper():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Inicializando o banco de dados...")
        initialize_db()
        
        crawler = EventCrawler(settings.target_url)
        parser = EventParser()
        pipeline = DatabasePipeline()
        
        logger.info(f"Buscando a página inicial: {settings.target_url}")
        initial_html = crawler.fetch_initial_page()
        if not initial_html:
            logger.error("Falha ao obter a página inicial. Encerrando scraping.")
            return

        initial_events = parser.parse_events_from_html(initial_html)
        if initial_events:
            logger.info(f"{len(initial_events)} eventos encontrados na página inicial. Enviando para o pipeline.")
            pipeline.process_events(initial_events)
        else:
            logger.info("Nenhum evento encontrado na página inicial.")
        

        # Determinar três datas com intervalo de semanas
        today = datetime.today()
        date_list = [today + timedelta(weeks=i) for i in range(3)]
        date_str_list = [date.strftime('%Y-%m-%d') for date in date_list]

        for idx, date_str in enumerate(date_str_list, start=1):
            logger.info(f"Iniciando requisição AJAX para data {idx}: {date_str}")
            action = 'mec_grid_load_more'
            offset = 0
            
            response_json = crawler.fetch_events_ajax(
                action=action,
                start_date=date_str,
                offset=offset,
            )
            
            if not response_json:
                logger.error(f"Falha ao obter dados via AJAX para data {date_str}. Pulando para a próxima data.")
                continue
            
            html_content = response_json.get('html', '')
            if not html_content.strip():
                logger.info(f"Nenhum conteúdo HTML retornado para data {date_str}. Pulando para a próxima data.")
                continue

            logger.info(f"Processando eventos retornados para data {date_str}")
            events = parser.parse_events_from_html(html_content)
            
            if events:
                logger.info(f"{len(events)} eventos encontrados para data {date_str}. Enviando para o pipeline.")
                pipeline.process_events(events)
            else:
                logger.info(f"Nenhum evento encontrado para data {date_str}.")


        logger.info("Scraping concluído com sucesso.")
        
    except Exception as e:
        logger.exception(f"Ocorreu um erro durante a execução do scraper: {e}")
    finally:
        crawler.close()
        if not database.is_closed():
            database.close()
            logger.info("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    scraper()