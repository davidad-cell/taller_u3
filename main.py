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


def main() -> None:
    fake = Faker('es_ES')

    
    rows = [{
        "nombre": fake.name(),
        "email": fake.email(),
        "direccion": fake.address().replace("\n", ", "),
        "telefono": fake.phone_number(),
        "fecha_nacimiento": fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d"),
        "ciudad": fake.city(),
        "transporte": fake.random_element(elements=["Carro", "Moto", "Bicicleta", "Bus", "Metro", "Camión"])
    } for _ in range(100000)]

    
    with open("personas_david.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["nombre", "email", "direccion", "telefono", "fecha_nacimiento", "ciudad", "transporte"])
        w.writeheader()
        w.writerows(rows)

    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL no está definida. Se omite la ingesta.")
        return

    ensure_database(db_url)
    engine = create_engine(db_url, future=True)