from fastapi import APIRouter

router = APIRouter(
    prefix='/items'
)

@router.get("/", tags=['Items'])
async def get_items():
    return "A book"