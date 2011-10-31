import logging

import transaction
from tg import config

from ldb.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
  """Place any commands to setup Movies here"""
  load_environment(conf.global_conf, conf.local_conf)
  # Load the models
  from ldb import model
  print "Creating tables"
  model.metadata.create_all(bind=config['pylons.app_globals'].sa_engine)

  # Create the initial data
  print "Creating initial data"

  drinkh = model.Drink(1, "Halcyon", 5, 1, 1, -1)
  drinkw = model.Drink(2, "The Kracken Black Spiced Rum", 9.5, 2, -1, 1)

  halc = model.Beer(1, "Lager", "Wheat", "About", "Gold")

  kr = model.Liquor(1, "Rum", "Spiced Rum", "About", "Black", "Sugar")

  tallg = model.Manufacturer(1, "Tallgrass Brewing Co.", "8845 Quail Lane Manhattan, KS 66502", 
                                "911", "http://tallgrassbeer.com/", "Hurray Beer", 1)
  krack = model.Manufacturer(2, "Kracken Rum Co.", "333 Washington St. Jersey City, NJ 07302",
                                "911", "http://krakenrum.com/site.html", "Kracken Rum Co. produces from a variety of different spices from Trinidad and Tobago", 2)

  ks = model.Region(1, "Kansas", "It's flat")
  nj = model.Region(2, "East", "East cost")

  model.DBSession.add(drinkh)
  model.DBSession.add(drinkw)
  model.DBSession.add(halc)
  model.DBSession.add(kr)
  model.DBSession.add(tallg)
  model.DBSession.add(krack)
  model.DBSession.add(ks)
  model.DBSession.add(nj)

  transaction.commit()
  print "Successfully setup"
