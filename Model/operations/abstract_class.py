from abc import abstractmethod, ABC
from typing import TypeVar, Generic, Optional, List
from datetime import date


T = TypeVar('T')

class BaseOperations(ABC, Generic[T]):
   @abstractmethod
   def add(self, **kwargs: dict):
      pass

   @abstractmethod
   def read(self, id: int):
      pass

   @abstractmethod
   def delete(self, id: int):
      pass

   @abstractmethod
   def update(self, id: int, **kwargs: dict):
      pass
