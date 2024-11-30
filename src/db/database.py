import os
from playhouse.sqlite_ext import SqliteExtDatabase
from src.config import settings

db_url = settings.database_url
if db_url.startswith("sqlite:///"):
    db_path = settings.database_path
    db_dir = os.path.dirname(db_path)

    # Criar o diretório se não existir
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"Diretório para o banco de dados criado em: {db_dir}")

    # Usar SqliteExtDatabase para possíveis extensões
    database = SqliteExtDatabase(
        db_path,
        pragmas={
            'journal_mode': 'wal',
            'cache_size': -1024 * 64,  # 64MB
            'foreign_keys': 1,
            'ignore_check_constraints': 0,
            'synchronous': 'NORMAL'
        },
        timeout=30  
    )
    print(f"Banco de dados configurado em: {db_path}")
else:
    raise ValueError(f"Unsupported database URL: {db_url}")
