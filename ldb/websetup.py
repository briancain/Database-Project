import logging

import transaction
from tg import config

from ldb.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
  """Place any commands to setup the Database here"""
  load_environment(conf.global_conf, conf.local_conf)
  # Load the models
  from ldb import model
  print "Creating tables"
  model.metadata.create_all(bind=config['pylons.app_globals'].sa_engine)

  # Create the initial data
  print "Creating initial data"

  # (id, name, abv, manu_id, catbeer ID, catLiquor ID, catWine ID)
  # -1 if null....for now
  drinkb = model.Drink(1, "Halcyon", 5, 1, 1, -1, -1)
  drinkl = model.Drink(2, "The Kracken Black Spiced Rum", 40, 2, -1, 1, -1)
  drinkw = model.Drink(3, "Relax Riesling", 9.5, 3, -1, -1, 1)

  # (id, category, style, about, color)
  halc = model.Beer(1, "Lager", "Wheat", "About", "Gold")

  # (id, category, style, about, color, ingrediants)
  kr = model.Liquor(1, "Rum", "Spiced Rum", "About", "Black", "Sugar")

  # (id, category, style, about, color, grapes)
  relw = model.Wine(1, "White", "Riesling", "About Coming Soon", "Yellow", "Reisling")

  # (id, name, address, phone, web, about, region_id)
  tallg = model.Manufacturer(1, "Tallgrass Brewing Co.", "8845 Quail Lane Manhattan, KS 66502", 
                                "911", "http://tallgrassbeer.com/", "Hurray Beer", 1)
  krack = model.Manufacturer(2, "Kracken Rum Co.", "333 Washington St. Jersey City, NJ 07302",
                                "911", "http://krakenrum.com/site.html", "Kracken Rum Co. produces from a variety of different spices from Trinidad and Tobago", 2)

  relax = model.Manufacturer(3, "Relax", "Address goes here", "911", "http://web.com", "Wine About", 2)

  # (id, state, about)
  ks = model.Region(1, "Kansas", "It's flat")
  nj = model.Region(2, "East", "East cost")

  # (id, catbeer id, catwine id, name)
  # -1 if null...for now
  nomnom = model.Food(1, -1, 1, "Pasta w/ White Sauce")
  nomnom2 = model.Food(2, 1, -1, "Red Meat")


  model.DBSession.add(drinkb)
  model.DBSession.add(drinkl)
  model.DBSession.add(drinkw)

  model.DBSession.add(halc)
  model.DBSession.add(kr)
  model.DBSession.add(relw)

  model.DBSession.add(tallg)
  model.DBSession.add(krack)
  model.DBSession.add(relax)

  model.DBSession.add(ks)
  model.DBSession.add(nj)

  model.DBSession.add(nomnom)
  model.DBSession.add(nomnom2)

  transaction.commit()
  print "Successfully setup"
