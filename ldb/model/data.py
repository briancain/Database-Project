from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy.types import Integer, Unicode, Boolean

from ldb.model import DeclarativeBase, metadata, DBSession

__all__ = [ 'Beer', 'Manufacturer', 'Region' ]

class Beer(DeclarativeBase):
  __tablename__ = 'Beer'
  
  id = Column(Integer, primary_key=True)
  category = Column(Unicode, nullable=True)
  style = Column(Unicode, nullable=True)
  about = Column(Unicode, nullable=True)
  color = Column(Unicode, nullable=True)

  def __init__(self, id, category, style, about, color):
    self.id = id
    self.category = category
    self.style = style
    self.about = about
    self.color = color

class Manufacturer(DeclarativeBase):
  __tablename__ = 'Manufacturer'

  id = Column(Integer,primary_key=True)
  name = Column(Unicode,nullable=False,unique=True)
  address = Column(Unicode, nullable=True)
  web = Column(Unicode, nullable=True)
  phone = Column(Integer, nullable = True)
  about = Column(Unicode, nullable=True)

  reg_id = Column(Integer, ForeignKey('Region.id'), nullable=True)
  reg = relation('Region', foreign_keys=reg_id)

  def __init__(self, id, name, address, phone, web, about, reg_id):
    self.id = id
    self.name = name
    self.address = address
    self.web = web
    self.phone = phone
    self.about = about

    self.reg_id = reg_id

class Region(DeclarativeBase):
  __tablename__ = 'Region'

  id = Column(Integer, primary_key=True)
  state = Column(Unicode, nullable = False)
  about = Column(Unicode, nullable =  True)

  def __init__(self, id, state, about):
    self.id = id
    self.state = state
    self.about = about
