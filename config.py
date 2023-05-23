import os
from dotenv import load_dotenv
from pathlib import Path
# from sqlalchemy import URL
import logging


LOG_LEVEL = logging.DEBUG

# initiate StateStorage and bot
BASE_DIR = Path(__file__).parent.resolve()
load_dotenv(os.path.join(BASE_DIR, '.env'))
TOKEN = os.getenv("TOKEN")

DB_STRING = 'sqlite:///test.db'
#     URL.create(
#     "postgresql+psycopg2",
#     username=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),  # plain (unescaped) text
#     host=os.getenv("DB_HOST"),
#     port=os.getenv("DB_PORT"),
#     database=os.getenv("DB_NAME"),
# )

PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")  # @BotFather -> Bot Settings -> Payments