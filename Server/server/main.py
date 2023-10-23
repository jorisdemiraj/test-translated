from src.rabbitmq.rabbitmq import MessageConsumer
import time
import redis
import logging
from pydantic.tools import lru_cache
from config.load_settings import (
    RABBIT_MQ_HOST,
    TOPIC,
    QUEUE,REDIS_HOST,REDIS_PORT,REDIS_DB
)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# this is the main initializer for the RabbitMQ Consumer
@lru_cache()
def get_broker():
    # return a new instance of MessageConsumer with the specified host, topic, and queue
    return MessageConsumer(RABBIT_MQ_HOST,TOPIC, QUEUE)

# main function that runs the whole Server side app.
def main():
    # create a new redis connection with the specified host, port, and db
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    # get a broker instance
    while True:
        try:
            LOGGER.info(f"Connecting to RabbitMQ")
            server = get_broker()
        except:
            LOGGER.info(f"Retry in 5...")
            time.sleep(5)
        else:
            break;
    # start the server with the redis connection
    server.start(r)
    # start consuming messages from the queue
    server.start_consume()
    LOGGER.info(f"Application started")
# check if this module is being run directly
if __name__ == "__main__":
    main()
