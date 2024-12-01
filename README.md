# Event Scraper

O **Event Scraper** é uma aplicação console desenvolvida em Python que coleta, armazena e permite a consulta de eventos culturais do Rio de Janeiro. Utilizando técnicas de scraping e uma interface de menu interativa, o projeto visa fornecer uma ferramenta eficiente para explorar eventos, suas datas, locais e outros metadados relevantes.

---

## 🚀 Funcionalidades

- **Scraping de Dados**: Coleta informações de eventos diretamente de uma fonte online.
- **Armazenamento de Dados**: Utiliza SQLite para armazenar dados de eventos e seus metadados.
- **Interface de Menu**: Oferece uma interface interativa para executar scraping e realizar consultas.
- **Consultas Avançadas**:
  - Exibir todos os eventos.
  - Mostrar os dois eventos mais próximos de iniciar.
  - Listar eventos que ocorrem no Rio de Janeiro.
  - Exibir eventos ao ar livre.
  - Mostrar metadados por evento.
- **Logs Detalhados**: Registra todas as operações para facilitar a depuração e monitoramento.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem de Programação**: Python 3.12
- **ORM**: Peewee
- **Banco de Dados**: SQLite
- **Bibliotecas de Scraping**: `requests`, `urlib`,`beautifulsoup4`
- **Gerenciamento de Logs**: `logging`
- **Ambiente Virtual**: `venv`

---

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de ter instalado as seguintes ferramentas em seu sistema:

- **Python 3.12** ou superior
- **Git** (para clonagem do repositório)
- **Ambiente Virtual** (opcional, mas recomendado)

---

## 🔧 Instalação

### 1. Clone o Repositório

Abra o terminal e execute o seguinte comando para clonar o repositório:

```bash
git clone https://github.com/VicktorMS/Rio_Event_Scraper.git
cd Rio_Event_Scraper
```

### 2. Crie um Ambiente Virtual

É recomendado utilizar um ambiente virtual para isolar as dependências do projeto.

```bash
python3 -m venv venv
```

### 3. Ative o Ambiente Virtual

- **No Linux/macOS:**

  ```bash
  source venv/bin/activate
  ```

- **No Windows:**

  ```bash
  venv\Scripts\activate
  ```

### 4. Instale as Dependências

Com o ambiente virtual ativado, instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

---

## 📋 Estrutura do Projeto

A seguir, uma visão geral da estrutura de diretórios e arquivos do projeto:

```
Rio_Event_Scraper/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── scraper/
│   │   └── scraper.py
│   ├── db/
│   │   ├── database.py
│   │   └── models/
│   │       ├── event.py
│   │       ├── event_data.py
│   │       └── metadata.py
│   ├── queries/
│   │   └── database_queries.py
│   └── menu/
│       └── menu.py
├── logs/
│   └── scraper.log
├── requirements.txt
└── README.md
```

- **src/**: Contém todo o código fonte do projeto.
  - **main.py**: Ponto de entrada da aplicação.
  - **config.py**: Configurações do projeto, como caminhos de arquivos e URLs.
  - **scraper/**: Módulo responsável por coletar dados de eventos.
    - **scraper.py**: Implementação do scraper.
  - **db/**: Configuração do banco de dados e modelos.
    - **database.py**: Configuração da conexão com o banco de dados.
    - **models/**: Definição dos modelos ORM.
      - **event.py**: Modelo do Evento.
      - **event_data.py**: Modelo dos Dados do Evento.
      - **metadata.py**: Modelo de Metadados.
  - **queries/**: Módulo contendo funções para consultas SQL.
    - **database_queries.py**: Implementação das consultas.
  - **menu/**: Implementação da interface de menu.
    - **menu.py**: Classes e funções relacionadas ao menu interativo.
- **logs/**: Diretório onde os logs da aplicação são armazenados.
  - **scraper.log**: Arquivo de log principal.
- **requirements.txt**: Lista de dependências do projeto.
- **README.md**: Este arquivo de documentação.

---

## 🎯 Como Utilizar

### 1. Ative o Ambiente Virtual

Caso ainda não tenha ativado o ambiente virtual, faça-o agora:

- **No Linux/macOS:**

  ```bash
  source venv/bin/activate
  ```

- **No Windows:**

  ```bash
  venv\Scripts\activate
  ```

### 2. Execute a Aplicação

Com o ambiente virtual ativo, inicie a aplicação executando o módulo `main.py`:

```bash
python3 -m src.main
```

### 3. Interaja com o Menu

Ao iniciar, você verá o seguinte menu no console:

```
=== Menu Principal ===
1. Executar Scraper
2. Mostrar Todos os Eventos
3. Mostrar os 2 Eventos Mais Próximos de Iniciar
4. Mostrar Eventos no Rio de Janeiro
5. Mostrar Eventos ao Ar Livre
6. Mostrar Metadados por Evento
7. Ver Logs
8. Sair
=======================
Selecione uma opção:
```

#### 3.1. Executando o Scraper

**Opção 1: Executar Scraper**

Esta opção coleta dados de eventos a partir da fonte especificada e os armazena no banco de dados.

**Exemplo de Uso:**

```
Selecione uma opção: 1
```

**Saída Esperada:**

```
Iniciando scraping...
Scraping concluído. Retornando ao menu principal.
```

#### 3.2. Mostrar Todos os Eventos

**Opção 2: Mostrar Todos os Eventos**

Exibe uma lista completa de todos os eventos armazenados, incluindo datas, localizações e tipos.

**Exemplo de Uso:**

```
Selecione uma opção: 2
```

**Saída Esperada:**

```
--- Todos os Eventos ---
Nome: Festival de Música
Tipo: Música
Descrição: Festival anual de música ao vivo.
Data: 2024-12-20
Localização: Parque Central
---------------------------
Nome: Exposição de Arte Moderna
Tipo: Arte
Descrição: Exposição de obras contemporâneas.
Data: 2024-12-25
Localização: Museu de Arte do Rio
---------------------------
...
```

#### 3.3. Mostrar os 2 Eventos Mais Próximos de Iniciar

**Opção 3: Mostrar os 2 Eventos Mais Próximos de Iniciar**

Exibe os dois eventos que estão mais próximos de ocorrer, com base na data atual.

**Exemplo de Uso:**

```
Selecione uma opção: 3
```

**Saída Esperada:**

```
--- 2 Eventos Mais Próximos de Iniciar ---
Nome: Festival de Música
Tipo: Música
Descrição: Festival anual de música ao vivo.
Data: 2024-12-20
Localização: Parque Central
---------------------------
Nome: Concerto de Jazz
Tipo: Música
Descrição: Concerto de jazz ao ar livre.
Data: 2024-12-22
Localização: Praça Mauá
---------------------------
```

#### 3.4. Mostrar Eventos no Rio de Janeiro

**Opção 4: Mostrar Eventos no Rio de Janeiro**

Lista todos os eventos que ocorrem no Rio de Janeiro.

**Exemplo de Uso:**

```
Selecione uma opção: 4
```

**Saída Esperada:**

```
--- Eventos no Rio de Janeiro ---
Nome: Exposição de Arte Moderna
Tipo: Arte
Descrição: Exposição de obras contemporâneas.
Data: 2024-12-25
Localização: Museu de Arte do Rio
---------------------------
Nome: Concerto de Jazz
Tipo: Música
Descrição: Concerto de jazz ao ar livre.
Data: 2024-12-22
Localização: Praça Mauá, Rio de Janeiro
---------------------------
...
```

#### 3.5. Mostrar Eventos ao Ar Livre

**Opção 5: Mostrar Eventos ao Ar Livre**

Exibe todos os eventos que são realizados ao ar livre.

**Exemplo de Uso:**

```
Selecione uma opção: 5
```

**Saída Esperada:**

```
--- Eventos ao Ar Livre ---
Nome: Festival de Música
Tipo: Música
Descrição: Festival anual de música ao vivo.
Data: 2024-12-20
Localização: Parque Central
Tipo de Evento: Ao ar livre
---------------------------
Nome: Concerto de Jazz
Tipo: Música
Descrição: Concerto de jazz ao ar livre.
Data: 2024-12-22
Localização: Praça Mauá, Rio de Janeiro
Tipo de Evento: Ao ar livre
---------------------------
...
```

#### 3.6. Mostrar Metadados por Evento

**Opção 6: Mostrar Metadados por Evento**

Apresenta todos os metadados associados a cada evento, organizados por nome do evento.

**Exemplo de Uso:**

```
Selecione uma opção: 6
```

**Saída Esperada:**

```
--- Metadados por Evento ---
Evento: Festival de Música
  event_type: Ao ar livre
  organizer: XYZ Eventos
  sponsors: ABC Corp
---------------------------
Evento: Exposição de Arte Moderna
  event_type: Indoor
  organizer: ArteRio
  sponsors: ArteCorp
---------------------------
...
```

#### 3.7. Ver Logs

**Opção 7: Ver Logs**

Exibe o conteúdo do arquivo de log para monitorar as operações da aplicação.

**Exemplo de Uso:**

```
Selecione uma opção: 7
```

**Saída Esperada:**

```
--- Logs do Scraper ---
2024-12-01 10:15:30,123 - INFO - main - Iniciando o aplicativo...
2024-12-01 10:15:30,124 - INFO - menu - Opção selecionada: Mostrar Todos os Eventos
2024-12-01 10:15:30,125 - INFO - queries.database_queries - Total de eventos: 2
2024-12-01 10:15:30,126 - INFO - queries.database_queries - Total de dados de eventos: 2
2024-12-01 10:15:30,127 - INFO - menu - Consulta 'Mostrar Todos os Eventos' concluída.
...
--- Fim dos Logs ---
```

#### 3.8. Sair

**Opção 8: Sair**

Encerra a aplicação.

**Exemplo de Uso:**

```
Selecione uma opção: 8
```

**Saída Esperada:**

```
Encerrando o aplicativo. Até logo!
```

---

## 📂 Estrutura do Banco de Dados

O banco de dados utilizado é o **SQLite**, organizado em duas principais tabelas: `event` e `event_data`. Além disso, há uma tabela de `metadata` para armazenar informações adicionais sobre os eventos.

### 1. Tabela `event`

Armazena informações básicas sobre cada evento.

| Campo        | Tipo           | Descrição                            |
|--------------|----------------|--------------------------------------|
| `id`         | AutoField      | Identificador único do evento.       |
| `name`       | CharField      | Nome do evento.                       |
| `type`       | TextField      | Tipo do evento (e.g., Música, Arte). |
| `description`| CharField (Null)| Descrição do evento.                  |
| `created_at` | DateTimeField  | Data e hora de criação do registro.   |

### 2. Tabela `event_data`

Armazena informações específicas de cada ocorrência de um evento.

| Campo      | Tipo          | Descrição                                   |
|------------|---------------|---------------------------------------------|
| `id`       | AutoField     | Identificador único dos dados do evento.    |
| `event_id` | ForeignKeyField | Referência ao `id` da tabela `event`.      |
| `date`     | DateTimeField | Data e hora do evento.                      |
| `location` | TextField     | Localização do evento.                      |

### 3. Tabela `metadata`

Armazena metadados adicionais para cada evento.

| Campo      | Tipo          | Descrição                        |
|------------|---------------|----------------------------------|
| `id`       | AutoField     | Identificador único do metadado. |
| `event_id` | ForeignKeyField | Referência ao `id` da tabela `event`. |
| `key`      | CharField     | Chave do metadado (e.g., `event_type`). |
| `value`    | TextField     | Valor do metadado (e.g., `Ao ar livre`). |

---

## 📝 Consultas Disponíveis

### 1. Mostrar Todos os Eventos

**Descrição**: Exibe uma lista completa de todos os eventos armazenados, incluindo suas datas, localizações e tipos.

**Função**: `get_all_events()`

### 2. Mostrar os 2 Eventos Mais Próximos de Iniciar

**Descrição**: Exibe os dois eventos que estão mais próximos de ocorrer, com base na data atual.

**Função**: `get_upcoming_events(limit=2)`

### 3. Mostrar Eventos no Rio de Janeiro

**Descrição**: Lista todos os eventos que ocorrem no Rio de Janeiro.

**Função**: `get_events_in_rio()`

### 4. Mostrar Eventos ao Ar Livre

**Descrição**: Exibe todos os eventos que são realizados ao ar livre.

**Função**: `get_outdoor_events()`

### 5. Mostrar Metadados por Evento

**Descrição**: Apresenta todos os metadados associados a cada evento, organizados por nome do evento.

**Função**: `get_metadata_per_event()`

---

## 📈 Logs

A aplicação utiliza a biblioteca `logging` para registrar informações importantes sobre a execução do scraper e das consultas. Os logs são armazenados no arquivo `src/logs/scraper.log`.

**Tipos de Logs:**

- **INFO**: Informações gerais sobre a execução.
- **WARNING**: Avisos sobre condições inesperadas que não impedem a execução.
- **ERROR**: Erros que impedem a conclusão de uma operação.
- **DEBUG**: Informações detalhadas para depuração (opcional, dependendo da configuração).

**Exemplo de Entrada de Log:**

```
2024-12-01 10:15:30,123 - INFO - main - Iniciando o aplicativo...
2024-12-01 10:15:30,124 - INFO - menu - Opção selecionada: Mostrar Todos os Eventos
2024-12-01 10:15:30,125 - INFO - queries.database_queries - Total de eventos: 2
2024-12-01 10:15:30,126 - INFO - queries.database_queries - Total de dados de eventos: 2
2024-12-01 10:15:30,127 - INFO - menu - Consulta 'Mostrar Todos os Eventos' concluída.
...
```

---

## 🔍 Depuração

Em caso de problemas durante a execução das consultas ou do scraper, os logs fornecem informações detalhadas que podem auxiliar na identificação e resolução de erros.

### Passos para Depuração:

1. **Verifique os Logs:**

   Abra o arquivo de log para identificar mensagens de erro ou avisos.

   ```bash
   cat src/logs/scraper.log
   ```

2. **Analise as Mensagens de Erro:**

   As mensagens de erro geralmente incluem o tipo de erro e a linha do código onde ocorreu, facilitando a localização do problema.

3. **Verifique a Estrutura do Banco de Dados:**

   Assegure-se de que as tabelas e os relacionamentos estão corretamente configurados.

4. **Teste Individualmente as Funções:**

   Execute as funções de consulta individualmente para isolar o problema.

5. **Revisite as Definições dos Modelos:**

   Garanta que os modelos ORM (`Event`, `EventData`, `Metadata`) estão corretamente definidos com os relacionamentos adequados.


## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---