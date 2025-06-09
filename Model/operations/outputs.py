import os
from typing import Type, TypeVar, List, Optional
from Model.database.db_handler import session_scope
from Model.models.warehouse_balance import WarehouseBalance
from Model.operations.abstract_class import BaseOperations
from Model.database.data_service import SessionFactory


T = TypeVar('T')


class WarehouseBalanceOperations(BaseOperations):
   def __init__(self, session_factory):
      self.session_factory = session_factory

   def add(self, **kwargs: dict):
      with session_scope(SessionFactory) as session:
         record = WarehouseBalance(
            product_name=kwargs['product_name'],
            warehouse_product_amount=kwargs['warehouse_product_amount'],
            unit=kwargs['unit'],
            checking_date=kwargs['checking_date'],
         )
         session.add(record)
         session.flush()
         return record

   def read(self, id: int):
      self.session.query(self.model).get(id)

   def update(self, id: int, **kwargs: dict):
      pass

   def delete(self):
      pass
