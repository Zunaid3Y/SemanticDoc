from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserPublic
from app.models import user as user_model
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserPublic)
async def register(payload: UserCreate):
    existing = await user_model.get_user_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_doc = {
        "email": payload.email,
        "hashed_password": hash_password(payload.password),
        "is_active": True,
        "is_admin": False,
    }
    user_doc = await user_model.create_user(user_doc)

    return UserPublic(
        id=str(user_doc["_id"]),
        email=user_doc["email"],
        is_admin=user_doc["is_admin"],
    )

@router.post("/login")
async def login(payload: UserCreate):  # reuse for simplicity: email + password
    user_doc = await user_model.get_user_by_email(payload.email)
    if not user_doc or not verify_password(payload.password, user_doc["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = create_access_token({"sub": str(user_doc["_id"])})
    return {"access_token": token, "token_type": "bearer"}
