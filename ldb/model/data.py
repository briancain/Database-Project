from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy.types import Integer, Unicode, Boolean

from ldb.model import DeclarativeBase, metadata, DBSession

__all__ = [ 'Beer', 'Manufacturer' ]

class Beer(DeclarativeBase):
  __tablename__ = 'beer'
  
  id = Column(Integer, primary_key=True)
  name = Column(Unicode, nullable=False)
  category = Column(Unicode, nullable=True)
  style = Column(Unicode, nullable=True)
  color = Column(Unicode, nullable=True)
  abv = Column(Integer, nullable=True)

  manf_id = Column(Integer,ForeignKey('Manufacturer.id'), nullable=True)
  manf = relation('Manufacturer',foreign_keys=manf_id )
  reviewed = Column(Boolean, nullable=False, default=False )

  def __init__(self, id, name, category, style, color, abv, manf_id):
    self.id = id
    self.name = name
    self.category = category
    self.style = style
    self.color = color
    self.abv = abv

    self.manf_id = manf_id

class Manufacturer(DeclarativeBase):
  __tablename__ = 'Manufacturer'

  id = Column(Integer,primary_key=True)
  name = Column(Unicode,nullable=False,unique=True)
  address = Column(Unicode, nullable=True)
  web = Column(Unicode, nullable=False)

  def __init__(self, id, name, address, web):
    self.id = id
    self.name = name
    self.address = address
    self.web = web
