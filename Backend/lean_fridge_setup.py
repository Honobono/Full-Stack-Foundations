import os
import sys
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key = True)
    name = Column(String(20), nullable = False)
    total = Column(Integer, primary_key = True)


class ItemProperty(Base):
    __tablename__ = 'itemProperty'
    id = Column(Integer, primary_key = True)
    name = Column(String(20), nullable = False)
    purchased_on = Column(DateTime, default = datetime.date.today)
    count = Column(Integer)
    category = Column(String(20), nullable = False)
    description = Column(String(50))
    stock_id = Column(Integer, ForeignKey('stock.id'))
    stock = relationship(Stock)


engine = create_engine('sqlite:///lean_fridge.db')

Base.metadata.create_all(engine)