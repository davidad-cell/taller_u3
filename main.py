import csv
import os
from faker import Faker
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url
from dotenv import load_dotenv


def ensure_database(db_url: str) -> None:
    """Create the target MySQL database if it doesn't exist."""
    url = make_url(db_url)
    dbname = url.database
    if not dbname:
        return
    server_url = url.set(database=None)
    engine = create_engine(server_url, future=True)
    with engine.begin() as conn:
        print(f"Creating database {dbname}")
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
