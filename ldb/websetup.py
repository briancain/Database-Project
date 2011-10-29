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

  halc = model.Beer(1, "Halcyon", "Lager", "Wheat", "Gold", 5, 1)
  tallg = model.Manufacturer(1, "Tallgrass Brewing Co.", "8845 Quail Lane Manhattan, KS 66502", 
                                "http://tallgrassbeer.com/")

  model.DBSession.add(halc)
  model.DBSession.add(tallg)

  transaction.commit()
  print "Successfully setup"
