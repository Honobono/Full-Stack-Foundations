import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Stock(Base):
    sqlite_autoincrement=True
    __tablename__ = 'stock'
    ids = Column(Integer, primary_key = True)
    names = Column(String(20), nullable = False)
    total = Column(Integer, primary_key = True)


class ItemProperty(Base):
    __tablename__ = 'itemProperty'
    ids = Column(Integer, primary_key = True)
    names = Column(String(20), nullable = False)
    dates = Column(datetime())
    counts = Column(Integer, primary_key = True)
    categories = Column(String(20), nullable = False)
    notes = Column(String(50))
    stock_ids = Column(Integer, ForeignKey('stock.id'))
    stock = relationship(Stock)

engine = create_engine('sqlite:///lean_fridge_app.db')

Base.metadata.create_all(engine)