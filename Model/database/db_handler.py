from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker # фабрика для создания сессий (сессия = "экземпляр работы с БД").
from sqlalchemy.orm import scoped_session # обеспечивает "глобальность" сессии для потока, т.е. удобно для многопоточности.
from sqlalchemy.orm.session import Session
from contextlib import contextmanager


def create_session(db_url: str, pool_size: int = 5, max_overflow: int = 10) -> sessionmaker:
   engine = create_engine(
      db_url,
      echo=False, # логирование sql-запросов выключено
      pool_pre_ping=True, # проверяет соединение перед использованием
      pool_size=pool_size, # размер пула соединений
      max_overflow=max_overflow # сколько доп соединений можно создавать свыше pool_size
   )

   session_factory = sessionmaker(
      autocommit=False,
      autoflush=False, # отключено автоматическое обновление изменений в БД перед запросом
      bind=engine
   )
   # возращает Объект (scoped_session_factory),
   # который можно вызывать как функцию для получения сессии (session = session_factory()).
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