from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")
MAIN_ADMIN = int(os.getenv("MAIN_ADMIN"))

user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")
host = os.getenv("host")
tablename = os.getenv("tablename")

DB_CONNECTION_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{tablename}"
"""
sudo docker run -d --name *имя контейнера* -e POSTGRES_PASSWORD=*пароль* -e POSTGRES_USER=*имя пользователя* -e POSTGRES_DB=*имя БД* -p 5432:5432 postgres
"""