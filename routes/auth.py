from fastapi import APIRouter
from schemas.user_schema import User
from services.auth_service import register_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: User):
    return register_user(user.dict())