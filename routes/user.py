from fastapi import APIRouter

router = APIRouter(
    prefix='/user',
    tags=['user'],
    include_in_schema=True
)

