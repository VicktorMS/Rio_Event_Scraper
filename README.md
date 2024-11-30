# Event Scraper


## Visão Geral

O **Event Scraper** é um aplicativo automatizado desenvolvido para extrair informações sobre eventos culturais do site [Agenda Cultural Rio de Janeiro](https://agendaculturalriodejaneiro.com). Este scraper coleta dados estruturados sobre eventos e os armazena em um banco de dados SQLite para posterior análise e consulta.

---

## Características

- **Extração de Eventos Iniciais**: Captura eventos diretamente da página inicial do site.
- **Requisições AJAX**: Realiza requisições AJAX para obter eventos adicionais em três datas diferentes, com intervalos de uma semana.
- **Armazenamento Estruturado**: Organiza os dados em três tabelas distintas no banco de dados:
  - **Event**: Informações básicas do evento.
  - **EventData**: Detalhes específicos de cada ocorrência do evento (data e localização).
  - **Metadata**: Informações adicionais como preço, disponibilidade, imagem e URL.
- **Logging Detalhado**: Registra todas as operações e erros em arquivos de log para monitoramento e depuração.
- **Mecanismos de Concurrency Control**: Implementa técnicas para evitar bloqueios no banco de dados durante operações de escrita.


## Arquitetura

### Componentes

1. **Crawler (`EventCrawler`)**: Responsável por realizar as requisições HTTP e simular interações com o site para obter o conteúdo das páginas e requisições AJAX.
2. **Parser (`EventParser`)**: Analisa o conteúdo HTML obtido pelo crawler e extrai os dados dos eventos utilizando scripts JSON-LD.
3. **Pipeline (`DatabasePipeline`)**: Processa os dados extraídos e os insere nas tabelas apropriadas do banco de dados.
4. **Banco de Dados (`SQLite`)**: Armazena os dados estruturados em três tabelas distintas.
5. **Logging**: Monitora e registra as operações do scraper para facilitar a análise e depuração.

### Fluxo de Trabalho

1. **Inicialização**:
   - Configuração do ambiente de logging.
   - Inicialização do banco de dados e criação das tabelas, se necessário.
2. **Extração de Eventos Iniciais**:
   - O crawler acessa a página inicial do site.
   - O parser extrai os eventos presentes na página inicial.
   - Os eventos são enviados para a pipeline para armazenamento.
3. **Requisições AJAX**:
   - O scraper determina três datas diferentes (hoje e as próximas duas semanas).
   - Para cada data, o crawler realiza requisições AJAX para obter mais eventos.
   - O parser extrai os eventos retornados nas respostas AJAX.
   - Os eventos são enviados para a pipeline para armazenamento.
4. **Finalização**:
   - Todas as conexões são fechadas adequadamente.
   - Logs são finalizados com sucesso.


## Instalação

### Pré-requisitos

- **Python 3.7+**
- **pip** (Gerenciador de Pacotes do Python)
- **virtualenv** (Opcional, mas recomendado)

### Clone o Repositório

```bash
git clone https://github.com/seu-usuario/event-scraper.git
cd event-scraper
```

### Configuração do Ambiente Virtual

Recomenda-se o uso de um ambiente virtual para isolar as dependências do projeto.

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### Instalação das Dependências

Instale todas as dependências necessárias listadas no `requirements.txt`.

```bash
pip install -r requirements.txt
```

---

## Configuração

### Arquivo de Configuração

O scraper utiliza um arquivo de configuração para definir parâmetros como a URL alvo e o caminho do banco de dados.

**`src/config.py`**

```python
# src/config.py
from datetime import datetime

class Settings:
    target_url = "https://agendaculturalriodejaneiro.com"
    database_path = "src/data/tp5_data.db"

settings = Settings()
```

- **`target_url`**: URL do site de onde os eventos serão extraídos.
- **`database_path`**: Caminho para o arquivo do banco de dados SQLite.

---

## Uso

### Executando o Scraper

Para iniciar o scraper, execute o seguinte comando na raiz do projeto:

```bash
python3 -m src.main
```

### Monitoramento dos Logs

O scraper gera logs detalhados tanto no console quanto no arquivo `scraper.log`. Esses logs são essenciais para monitorar o progresso do scraper e identificar possíveis erros.

**Exemplo de Comando para Verificar Logs em Tempo Real:**

```bash
tail -f scraper.log
```

---

## Banco de Dados

O scraper utiliza o **SQLite** como banco de dados para armazenar os dados extraídos. O banco de dados é composto por três tabelas principais: `Event`, `EventData` e `Metadata`.

### Estrutura das Tabelas

1. **`Event`**

   - **Descrição**: Armazena informações básicas sobre cada evento.
   - **Campos**:
     - `id`: Identificador único do evento.
     - `name`: Nome do evento (único).
     - `type`: Tipo do evento.
     - `description`: Descrição do evento.
     - `created_at`: Data e hora de criação do registro.

2. **`EventData`**

   - **Descrição**: Contém detalhes específicos de cada ocorrência do evento, como data e localização.
   - **Campos**:
     - `id`: Identificador único.
     - `event_id`: Chave estrangeira referenciando a tabela `Event`.
     - `date`: Data do evento.
     - `location`: Localização detalhada do evento.
   - **Índices**:
     - Combinação única de `event_id` e `date` para evitar duplicatas.

3. **`Metadata`**

   - **Descrição**: Armazena informações adicionais sobre os eventos, como preço, disponibilidade, imagem e URL.
   - **Campos**:
     - `id`: Identificador único.
     - `event_id`: Chave estrangeira referenciando a tabela `Event`.
     - `key`: Chave da metadata (ex: `price`).
     - `value`: Valor da metadata (ex: `50`).
     - `updated_at`: Data e hora da última atualização do registro.
   - **Índices**:
     - Combinação única de `event_id` e `key` para evitar duplicatas.

### Acessando o Banco de Dados

Você pode utilizar ferramentas como **DBeaver** para visualizar e gerenciar o banco de dados SQLite.

1. **Abrir o DBeaver**.
2. **Adicionar uma Nova Conexão**:
   - Selecione **SQLite** como tipo de banco de dados.
   - Navegue até o arquivo `tp5_data.db` localizado em `src/data/`.
3. **Conectar e Explorar**:
   - Após conectar, você poderá visualizar as tabelas `event`, `event_data` e `metadata`.
   - Execute consultas SQL para analisar os dados conforme necessário.

**Nota**: Certifique-se de que o scraper não está em execução enquanto tenta acessar o banco de dados com o DBeaver para evitar conflitos de acesso.

---

## Resolução de Problemas

### Erro: Database Locked

**Descrição**: Ocorre quando o scraper tenta acessar o banco de dados enquanto outra conexão (como o DBeaver) está mantendo uma transação aberta, resultando em bloqueios.

**Causas Comuns**:

- Acesso simultâneo de múltiplas conexões ao banco de dados.
- Transações não finalizadas ou conexões não fechadas adequadamente.
- Alta concorrência em operações de leitura e escrita.

**Soluções**:

1. **Configure o SQLite para Modo WAL (Write-Ahead Logging)**:
   
   Isso permite leituras simultâneas enquanto escritas estão ocorrendo.

   **Como Configurar**:
   
   No seu arquivo de inicialização do banco de dados (`src/db/init_db.py`), adicione as seguintes linhas após conectar ao banco de dados:

   ```python
   database.connect()
   database.execute_sql('PRAGMA journal_mode = WAL;')
   database.execute_sql('PRAGMA synchronous = NORMAL;')  # Opcional: melhora a performance com menor segurança
   ```

2. **Aumente o Timeout da Conexão do SQLite**:
   
   Define quanto tempo o SQLite espera antes de lançar um erro de bloqueio.

   **Como Configurar**:

   No seu arquivo de configuração do banco de dados (`src/db/database.py`), ajuste o parâmetro `timeout`:

   ```python
   from peewee import SqliteDatabase
   from src.config import settings

   database = SqliteDatabase(
       settings.database_path,
       pragmas={
           'journal_mode': 'wal',
           'cache_size': -1024 * 64,  # 64MB
           'foreign_keys': 1,
           'ignore_check_constraints': 0,
           'synchronous': 'NORMAL'
       },
       timeout=30  # Timeout de 30 segundos
   )
   ```

3. **Evite Acessar o Banco de Dados Enquanto o Scraper Está Executando**:
   
   Ferramentas como o DBeaver mantêm conexões abertas que podem interferir com o scraper. Considere:

   - Fechar o DBeaver enquanto o scraper está executando.
   - Utilizar uma cópia do banco de dados para consultas.

   **Como Criar uma Cópia do Banco de Dados**:

   ```bash
   cp src/data/tp5_data.db src/data/tp5_data_copy.db
   ```

   Use o arquivo `tp5_data_copy.db` no DBeaver para evitar conflitos.

4. **Assegure-se de Fechar Conexões Corretamente**:
   
   No seu script Python, garanta que todas as conexões com o banco de dados são fechadas após as operações.

   **Exemplo no `main.py`**:

   ```python
   finally:
       # Fechar o crawler
       crawler.close()
       # Fechar a conexão com o banco de dados se ainda estiver aberta
       if not database.is_closed():
           database.close()
           logger.info("Conexão com o banco de dados fechada.")
   ```

### Outros Problemas Comuns

1. **Falha na Extração de Dados**:
   
   - **Causa**: Alterações na estrutura do site alvo.
   - **Solução**: Atualize os seletores no `EventParser` para refletir as mudanças no site.

2. **Problemas de Rede**:
   
   - **Causa**: Conexões instáveis ou timeout.
   - **Solução**: Verifique a conexão com a internet e considere aumentar o timeout nas requisições HTTP.

3. **Erros de Parsing**:
   
   - **Causa**: Dados inesperados ou malformados nos scripts JSON-LD.
   - **Solução**: Adicione verificações e tratamentos de exceções no `EventParser` para lidar com dados inconsistentes.

---

## Considerações Finais

O **Event Scraper** é uma ferramenta eficiente para coletar e organizar dados sobre eventos culturais, facilitando análises posteriores e a geração de insights. A modularização do código e a estrutura robusta do banco de dados garantem que o scraper seja fácil de manter e escalar conforme as necessidades do projeto evoluem.

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
