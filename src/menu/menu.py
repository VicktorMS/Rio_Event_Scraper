# src/menu/menu.py

from abc import ABC, abstractmethod
from typing import List, Optional
import logging
import sys
from src.scraper import scraper  # Importa a função scraper
from src.queries.database_queries import (
    get_all_events,
    get_upcoming_events,
    get_events_in_rio,
    get_outdoor_events,
    get_metadata_per_event
)

class MenuOption(ABC):
    """
    Classe abstrata que define a interface para opções de menu.
    """

    @abstractmethod
    def display_name(self) -> str:
        """
        Retorna o nome da opção que será exibido no menu.
        """
        pass

    @abstractmethod
    def execute(self):
        """
        Executa a ação associada à opção.
        """
        pass

class ScraperOption(MenuOption):
    """
    Opção de menu para executar o scraper.
    """

    def display_name(self) -> str:
        return "Executar Scraper"

    def execute(self):
        logging.info("Opção selecionada: Executar Scraper")
        scraper()
        logging.info("Scraping concluído. Retornando ao menu principal.")

class ShowAllEventsOption(MenuOption):
    """
    Opção de menu para mostrar todos os eventos com suas datas, localização e tipo de evento.
    """

    def display_name(self) -> str:
        return "(QUERY) Mostrar Todos os Eventos"

    def execute(self):
        logging.info("Opção selecionada: Mostrar Todos os Eventos")
        events = get_all_events()
        if events:
            print("\n--- Todos os Eventos ---")
            for event in events:
                print(f"Nome: {event['Nome']}")
                print(f"Tipo: {event['Tipo']}")
                print(f"Descrição: {event['Descrição']}")
                print(f"Data: {event['Data']}")
                print(f"Localização: {event['Localização']}")
                print("---------------------------")
        else:
            print("Nenhum evento encontrado.")
        logging.info("Consulta 'Mostrar Todos os Eventos' concluída.")

class ShowUpcomingEventsOption(MenuOption):
    """
    Opção de menu para mostrar os 2 eventos mais próximos de iniciar.
    """

    def display_name(self) -> str:
        return "(QUERY) Mostrar os 2 Eventos Mais Próximos de Iniciar"

    def execute(self):
        logging.info("Opção selecionada: Mostrar os 2 Eventos Mais Próximos de Iniciar")
        events = get_upcoming_events(limit=2)
        if events:
            print("\n--- 2 Eventos Mais Próximos de Iniciar ---")
            for event in events:
                print(f"Nome: {event['Nome']}")
                print(f"Tipo: {event['Tipo']}")
                print(f"Descrição: {event['Descrição']}")
                print(f"Data: {event['Data']}")
                print(f"Localização: {event['Localização']}")
                print("---------------------------")
        else:
            print("Nenhum evento próximo encontrado.")
        logging.info("Consulta 'Mostrar os 2 Eventos Mais Próximos de Iniciar' concluída.")

class ShowEventsInRioOption(MenuOption):
    """
    Opção de menu para mostrar os eventos que acontecem no Rio de Janeiro.
    """

    def display_name(self) -> str:
        return "(QUERY) Mostrar Eventos no Rio de Janeiro"

    def execute(self):
        logging.info("Opção selecionada: Mostrar Eventos no Rio de Janeiro")
        events = get_events_in_rio()
        if events:
            print("\n--- Eventos no Rio de Janeiro ---")
            for event in events:
                print(f"Nome: {event['Nome']}")
                print(f"Tipo: {event['Tipo']}")
                print(f"Descrição: {event['Descrição']}")
                print(f"Data: {event['Data']}")
                print(f"Localização: {event['Localização']}")
                print("---------------------------")
        else:
            print("Nenhum evento encontrado no Rio de Janeiro.")
        logging.info("Consulta 'Mostrar Eventos no Rio de Janeiro' concluída.")

class ShowOutdoorEventsOption(MenuOption):
    """
    Opção de menu para mostrar todos os eventos que são ao ar livre.
    """

    def display_name(self) -> str:
        return "(QUERY) Mostrar Eventos ao Ar Livre"

    def execute(self):
        logging.info("Opção selecionada: Mostrar Eventos ao Ar Livre")
        events = get_outdoor_events()
        if events:
            print("\n--- Eventos ao Ar Livre ---")
            for event in events:
                print(f"Nome: {event['Nome']}")
                print(f"Tipo: {event['Tipo']}")
                print(f"Descrição: {event['Descrição']}")
                print(f"Data: {event['Data']}")
                print(f"Localização: {event['Localização']}")
                print(f"Tipo de Evento: {event['Tipo de Evento']}")
                print("---------------------------")
        else:
            print("Nenhum evento ao ar livre encontrado.")
        logging.info("Consulta 'Mostrar Eventos ao Ar Livre' concluída.")

class ShowMetadataPerEventOption(MenuOption):
    """
    Opção de menu para mostrar todos os Metadados por evento.
    """

    def display_name(self) -> str:
        return "(QUERY) Mostrar Metadados por Evento"

    def execute(self):
        logging.info("Opção selecionada: Mostrar Metadados por Evento")
        metadata = get_metadata_per_event()
        if metadata:
            print("\n--- Metadados por Evento ---")
            for event_name, metas in metadata.items():
                print(f"Evento: {event_name}")
                for key, value in metas.items():
                    print(f"  {key}: {value}")
                print("---------------------------")
        else:
            print("Nenhum metadado encontrado.")
        logging.info("Consulta 'Mostrar Metadados por Evento' concluída.")

class PlaceholderOption(MenuOption):
    """
    Opção de menu sem funcionalidade implementada.
    """

    def __init__(self, name: str):
        self._name = name

    def display_name(self) -> str:
        return self._name

    def execute(self):
        logging.info(f"Opção selecionada: {self._name}")
        print(f"A opção '{self._name}' ainda não está implementada.")
        logging.info("Retornando ao menu principal.")

class ExitOption(MenuOption):
    """
    Opção de menu para sair do aplicativo.
    """

    def display_name(self) -> str:
        return "Sair"

    def execute(self):
        logging.info("Opção selecionada: Sair")
        print("Encerrando o aplicativo. Até logo!")
        sys.exit(0)

class Menu:
    """
    Classe que representa o menu de console.
    """

    def __init__(self, options: Optional[List[MenuOption]] = None):
        self.options: List[MenuOption] = options if options else []
        self.logger = logging.getLogger(self.__class__.__name__)

    def add_option(self, option: MenuOption):
        """
        Adiciona uma opção ao menu.
        """
        self.options.append(option)
        self.logger.debug(f"Opção adicionada: {option.display_name()}")

    def display(self):
        """
        Exibe o menu e processa a seleção do usuário.
        """
        while True:
            print("\n=== Menu Principal ===")
            for idx, option in enumerate(self.options, start=1):
                print(f"{idx}. {option.display_name()}")
            print("======================")

            try:
                choice = int(input("Selecione uma opção: "))
                if 1 <= choice <= len(self.options):
                    selected_option = self.options[choice - 1]
                    selected_option.execute()
                else:
                    print("Opção inválida. Por favor, tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número correspondente às opções.")
            except Exception as e:
                logging.exception("Ocorreu um erro inesperado no menu.")
                print("Ocorreu um erro inesperado. Por favor, tente novamente.")

def create_menu() -> Menu:
    """
    Função para criar e configurar o menu com suas opções.
    """
    menu = Menu()
    menu.add_option(ScraperOption())
    menu.add_option(ShowAllEventsOption())
    menu.add_option(ShowUpcomingEventsOption())
    menu.add_option(ShowEventsInRioOption())
    menu.add_option(ShowOutdoorEventsOption())
    menu.add_option(ShowMetadataPerEventOption())
    menu.add_option(PlaceholderOption("Ver Logs"))  # Exemplo de opção sem implementação
    menu.add_option(ExitOption())
    return menu
