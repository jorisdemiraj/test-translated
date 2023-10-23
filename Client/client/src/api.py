
from fastapi import APIRouter

from .endpoints.run import router as run_router


router = APIRouter()

router.include_router(run_router)

