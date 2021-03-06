from sqlalchemy import *
from sqlalchemy import Column
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy.types import Integer, Unicode, Boolean, Text

from ldb.model import DeclarativeBase, metadata, DBSession

__all__ = [ 'Beer', 'Manufacturer', 'Region', 'Drink', 'Liquor', 'Wine', 'Food' ]

class Drink(DeclarativeBase):
  __tablename__ = 'Drink'
  __table_args__ = (CheckConstraint('abv > 0', 'abv < 100'), CheckConstraint('(catB_id > 0 AND catL_id < 0 AND catW_id < 0) OR (catB_id < 0 AND catL_id > 0 AND catW_id < 0) OR (catB_id < 0 AND catL_id < 0 AND catW_id > 0)'))

  id = Column(Integer, primary_key=True)
  name = Column(Unicode, nullable=False)
  abv = Column(Integer, nullable=True)

  manu_id = Column(Integer, ForeignKey('Manufacturer.id'), nullable=True)
  man = relation('Manufacturer', foreign_keys=manu_id)

  catB_id = Column(Integer, ForeignKey('Beer.id'), nullable=True)
  catB = relation('Beer', foreign_keys=catB_id)

  catL_id = Column(Integer, ForeignKey('Liquor.id'), nullable=True)
  catL = relation('Liquor', foreign_keys=catL_id)

  catW_id = Column(Integer, ForeignKey('Wine.id'), nullable=True)
  catW = relation('Wine', foreign_keys=catW_id)

  def __init__(self, id, name, abv, manu_id, catB_id, catL_id, catW_id):
    self.id = id
    self.name = name
    self.abv = abv
    
    self.manu_id = manu_id
    self.catB_id = catB_id
    self.catL_id = catL_id
    self.catW_id = catW_id

class Food(DeclarativeBase):
  __tablename__ = 'Food'

  id = Column(Integer, primary_key=True)
  name = Column(Unicode, nullable=False)

  catB_id = Column(Integer, ForeignKey('Beer.id'), nullable=True)
  catB = relation('Beer', foreign_keys=catB_id)

  catW_id = Column(Integer, ForeignKey('Wine.id'), nullable=True)
  catW = relation('Wine', foreign_keys=catW_id)

  def __init__(self, id, catB_id, catW_id, name):
    self.id = id
    self.catB_id = catB_id
    self.catW_id = catW_id
    self.name = name

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

class Liquor(DeclarativeBase):
  __tablename__ = 'Liquor'

  id = Column(Integer, primary_key=True)
  category = Column(Unicode, nullable=True)
  style = Column(Unicode, nullable=True)
  about = Column(Unicode, nullable=True)
  color = Column(Unicode, nullable=True)
  ingred = Column(Unicode, nullable=True)

  def __init__(self, id, category, style, about, color, ingred):
    self.id = id
    self.category = category
    self.style = style
    self.about = about
    self.color = color
    self.ingred = ingred

class Wine(DeclarativeBase):
  __tablename__ = 'Wine'

  id = Column(Integer, primary_key=True)
  category = Column(Unicode, nullable=True)
  style = Column(Unicode, nullable=True)
  about = Column(Unicode, nullable=True)
  color = Column(Unicode, nullable=True)
  grapes = Column(Unicode, nullable=True)

  def __init__(self, id, category, style, about, color, grapes):
    self.id = id
    self.category = category
    self.about = about
    self.style = style
    self.color = color
    self.grapes = grapes

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
