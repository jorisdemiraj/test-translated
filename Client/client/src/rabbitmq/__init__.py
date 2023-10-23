import json
import logging
import asyncio
from pydantic.tools import lru_cache
import pika
from pika.adapters.blocking_connection import BlockingChannel
import time
from config.load_settings import RABBIT_MQ_HOST, TOPIC, QUEUE

  