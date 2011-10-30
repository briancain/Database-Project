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

  halc = model.Beer(1, "Lager", "Wheat", "About", "Gold")
  tallg = model.Manufacturer(1, "Tallgrass Brewing Co.", "8845 Quail Lane Manhattan, KS 66502", 
                                "911", "http://tallgrassbeer.com/", "Hurray Beer", 1)
  ks = model.Region(1, "Kansas", "It's flat")

  model.DBSession.add(halc)
  model.DBSession.add(tallg)
  model.DBSession.add(ks)

  transaction.commit()
  print "Successfully setup"
