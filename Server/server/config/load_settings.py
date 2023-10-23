import os
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), './.env')
load_dotenv(dotenv_path)


LOGS_PATH = os.environ.get("PATH_LOGS")
RABBIT_MQ_HOST = os.environ.get("RABBIT_MQ_HOST")
TOPIC = os.environ.get("TOPIC")
QUEUE = os.environ.get("QUEUE")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_DB = os.environ.get("REDIS_DB")
URL_PATH = os.environ.get("URL_PATH")
