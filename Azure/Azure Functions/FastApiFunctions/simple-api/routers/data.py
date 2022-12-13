import logging
from fastapi import APIRouter, Request, Response

router = APIRouter()

@router.post("/{data}")
async def get_data(request: Request):
    logging.info("get_data")
    return Response(content="get_data")