import logging.handlers
import os
from fastapi import FastAPI
from src.api import router as api_router
from src.rabbitmq.rabbitmq import message_broker
from config.load_settings import (
    LOGS_PATH,
    VERSION
)

# define the debug format for logging
debug_format = '[%(asctime)s] [%(levelname)s] [%(threadName)s] [%(filename)s %(lineno)d]: %(message)s'

# define the filename for logging
filename = os.path.join(LOGS_PATH, f"{__name__}.log")

# configure basic logging settings
logging.basicConfig(
    format=debug_format,
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)

# get a logger instance
LOGGER = logging.getLogger(__name__)

# create a FastAPI instance
app = FastAPI(title="Translated-Test-App", version=VERSION)

# define allowed hosts
ALLOWED_HOSTS = ["*"]

# define startup event handler
@app.on_event("startup")
async def startup():
    # start the message broker on startup
    message_broker.start()

# define shutdown event handler
@app.on_event("shutdown")
async def shutdown():
    # print "stop" on shutdown
    print("stop")

# include the api router in the app
app.include_router(api_router)
