from fastapi import APIRouter


router = APIRouter(
    prefix="/users"
)

@router.get('/', tags=['Users'])
async def get_user():
    return "Christian Højsager"