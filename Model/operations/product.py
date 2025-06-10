import os
from typing import Type, TypeVar, List, Optional
from Model.database.db_handler import session_scope
from Model.models.outputs import WarehouseBalance
from Model.operations.abstract_class import BaseOperations
from Model.database.data_service import SessionFactory


T = TypeVar('T')

class Product(BaseOperations):
   def __init__(self):
      super().__init__()