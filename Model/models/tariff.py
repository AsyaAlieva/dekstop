from sqlalchemy import Column, Integer, String, Float, Numeric
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Tariff(Base):
   __tablename__ = "tariff"

   id = Column(Integer, primary_key=True)
   price = Column(Numeric(10, 2), nullable=False)
   distance = Column(Numeric(10, 2), nullable=False)
   city = Column(String(50), nullable=False)
   warehouse = Column(String(80), nullable=False)