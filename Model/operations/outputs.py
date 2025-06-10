import os
from typing import Type, TypeVar, List, Optional
from Model.database.db_handler import session_scope
from Model.models.outputs import WarehouseBalance
from Model.operations.abstract_class import BaseOperations
from Model.database.data_service import SessionFactory
from Model.models.tariff import Tariff as TariffModel
from decimal import Decimal

T = TypeVar('T')


class Tariff:
   def __init__(self, session_factory):
      self.session_factory = session_factory

   def read_all(self):
      with session_scope(SessionFactory) as session:
         result = session.query(TariffModel).all()
         for row in result:
            new_fields = list()
            fields = [row.price, row.distance, row.city, row.warehouse]
            for field_value in fields:
               new_fields.append(str(field_value))
            yield new_fields


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


class TransportationPlanOperations(BaseOperations):
   def __init__(self, session_factory):
      self.session_factory = session_factory


class ProductDeliveryPlanOperations(BaseOperations):
   def __init__(self, session_factory):
      self.session_factory = session_factory


class DeliveryReportOperations(BaseOperations):
   def __init__(self, session_factory):
      self.session_factory = session_factory
