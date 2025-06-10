from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class WarehouseBalance(Base):
   __tablename__ = "warehouse_balance"

   id = Column(Integer, primary_key=True)
   product_name = Column(String(80), unique=True, nullable=False)
   warehouse_product_amount = Column(Integer, nullable=False)
   unit = Column(String(10), nullable=False)
   checking_date = Column(Date)


class TransportationPlan(Base):
   __tablename__ = "transportation_plan"
   id = Column(Integer, primary_key=True)


class ProductDeliveryPlan(Base):
   __tablename__ = "product_delivery_plan"
   id = Column(Integer, primary_key=True)


class DeliveryReport(Base):
   __tablename__ = "delivery_report"
   id = Column(Integer, primary_key=True)