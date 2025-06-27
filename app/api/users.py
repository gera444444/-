from fastapi import APIRouter, Depends
from app.db.models import User
from app.core.security import get_current_user
from app.schemas.users import UserOut
from app.repositories.users import UserRepository
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
async def read_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = UserRepository(User, db)
    return repo.get(current_user.id)