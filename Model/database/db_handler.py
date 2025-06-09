from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from contextlib import contextmanager


def create_session(
      db_url: str, pool_size: int = 5, max_overflow: int = 10
   ) -> sessionmaker:
   engine = create_engine(
      db_url,
      echo=False,
      pool_pre_ping=True,
      pool_size=pool_size,
      max_overflow=max_overflow
   )

   session_factory = sessionmaker(
      autocommit=False,
      autoflush=False,
      bind=engine
   )
   scoped_session_factory = scoped_session(session_factory)
   return scoped_session_factory


@contextmanager
def session_scope(session_factory: sessionmaker):
   """ Контекстный менеджер для работы с БД """
   session = session_factory()
   try:
      yield session
      session.commit()
   except Exception as e:
      print(e)
      session.rollback()
      raise
   finally:
      session.close()