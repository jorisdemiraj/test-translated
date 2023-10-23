import logging

from fastapi import APIRouter, Body, Depends, Path, Query, Response, File, UploadFile, Form, BackgroundTasks
from fastapi.responses import RedirectResponse

from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK,
    HTTP_202_ACCEPTED,
    HTTP_500_INTERNAL_SERVER_ERROR
)

from config.load_settings import APP_HOST, APP_PORT

from src.models.run import RunInResponseInComputing


from src.utils.utils import *
import asyncio

from src.rabbitmq.rabbitmq import message_broker
import hashlib
import json
router = APIRouter()
