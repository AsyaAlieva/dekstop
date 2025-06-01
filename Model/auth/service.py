from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from Model.models.users import User
from Model.auth.utils import verify_password


class AuthService:
   def __init__(self, db_session: Session):
      self.db = db_session

   def authenticate_user(self, username: str, password: str):
      user = self.db.query(User).filter(User.username == username).first()
      if not user or not verify_password(password, user.password_hash):
         return None
      return user

   def create_user(self, username: str, password: str):
      if self.db.query(User).filter_by(username=username).count() > 0:
         raise ValueError(f"Пользователь {username} уже существует")

      user = User(username=username)
      if len(password) < 8:
         raise ValueError("Слишком короткий пароль!")
      user.set_password(password)

      try:
         self.db.add(user)
         self.db.commit()
      except IntegrityError as error:
         self.db.rollback()
         if "unique" in str(error).lower() or "duplicate" in str(error).lower():
            raise ValueError(f"Пользователь {username} уже существует") from error
         else:
            print(error)
            raise RuntimeError("Не удалось создать пользователя из-за ограничений базы данных")
      return user
