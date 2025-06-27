from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.schemas.users import Token, UserCreate, UserOut
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.repositories.users import UserRepository
from app.db.models import User
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password
)

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=UserOut)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(User, db)
    if user_repo.get_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    db_user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(User, db)
    user = user_repo.get_by_email(form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}