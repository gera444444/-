from app.db.models import User
from app.schemas.users import UserCreate, UserUpdate
from .base import BaseRepository

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()