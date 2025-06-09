from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from Model.auth.utils import get_password_hash
from Model.auth.utils import verify_password


Base = declarative_base()


class User(Base):
   __tablename__ = 'users'

   id = Column(Integer, primary_key=True)
   username = Column(String(50), unique=True, nullable=False)
   password_hash = Column(String(128), nullable=False)

   def set_password(self, password: str):
      self.password_hash = get_password_hash(password)

   def check_password(self, password: str) -> bool:
      return verify_password(password, self.password_hash)
