from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def home_page():
    return {'key': 'Hi bro!'}
