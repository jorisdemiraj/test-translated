import os
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), './.env')
load_dotenv(dotenv_path)

LOGS_PATH = os.environ.get("PATH_LOGS")
DATA_PATH = os.environ.get("PATH_DATA")
APP_HOST = os.environ.get("APP_HOST")
APP_NAME = os.environ.get("APP_NAME")
APP_PORT = os.environ.get("APP_PORT")
WORKERS = os.environ.get("WORKERS")
VERSION = os.environ.get("VERSION")

RABBIT_MQ_HOST = os.environ.get("RABBIT_MQ_HOST")
TOPIC = os.environ.get("TOPIC")
QUEUE= os.environ.get("QUEUE")
