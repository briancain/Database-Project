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

#
# MANUFACTURERS
#
#
# (id, name, address, phone, web, about, region_id)
  TallgrassBrewingCo = model.Manufacturer(1,"Tallgrass Brewing Co.", "8845 Quail Lane Manhattan, KS 66502", "http://www.tallgrassbeer.com/","(785) 537-1131", "Tallgrass Brewing Co. is a microbrewery based out of Manhattan, Kansas.", 1) #region 1 is kansas

  BoulevardBrewingCo = model.Manufacturer(2, "Boulevard Brewing Co.", "2501 Southwest Boulevard Kansas City, MO 64108",	"http://www.boulevard.com/",	"(816) 474-7095","Boulevard Brewing Co. is a microbrewery based out of Kansas City, Missouri.", 2) #region 2 is missouri

  KrackenRumCo = model.Manufacturer(3, "Kracken Rum Co.",	"333 Washington St. Jersey City, NJ 07302", "0000", "http://www.krakenrum.com/site.html","Kracken Rum Co. produces rum from a verity of different spices from Trinidad and Tobago.", 3)#region 3 is NJ

  JohnJamesonandSonsLimited = model.Manufacturer(4, "John Jameson & Sons Limited",	"777 Westchester Ave. West Harrison , NY 10604", "http://www.jamesonwhiskey.com/", "(914) 539-4500","John Jameson & Sons Limited produces Irish Whiskey that is triple distilled to create a more smother taste.", 4) #region 4 is NY

  AustinNicholsDistillingCo = model.Manufacturer(5, "Austin, Nichols Distilling Co.","1525 Tyrone Road Lawrenceburg, KY 40342","http://www.wildturkey.com/","(502) 839-2182","Austin, Nichols Distilling Co. produces bourbon under the name Wild Turkey and is based out of Kentucky.", 5) #region 5 is KY

  AnheuserBusch = model.Manufacturer(6, "Anheuser-Busch Companies, Inc.", "1127 Lynch Street & Lynch St  St. Louis, MO 63118", "http://www.anheuser-busch.com/", "(314) 577-2333", "Produces the United States most popular beer.", 2)

  FootHillsBrewing = model.Manufacturer(7, "Foothills Brewing Company", "638 W. 4th Street Winston-Salem, North Carolina United States", "(336) 777-3348", "http://www.foothillsbrewing.com/", "A small brewing company that produces a wide variety of beer", 7)

  MccormickDistillingCo = model.Manufacturer(8,"McCormick Distilling Co.", "1 Mc Cormick Ln, Weston, MO 66502", "http://www.mccormickdistilling.com/","(816) 640-2276", "McCormick Distilling, located in historic Weston, Missouri, is the oldest continuously operating distillery in the U.S.", 2)

  HobNobWineCo = model.Manufacturer(9,"HobNob Wine Company", "709 Westchester Ave., Suite 300, White Plains, NY 10604", "http://www.hobnobwines.com/","(914) 251-9463", "HobNob Wine Company offers fine French wines at California prices.", 4)

  WJDeutschSonsLtd = model.Manufacturer(10,"W.J. Deutsch & Sons Ltd.", "709 Westchester Ave., Suite 300, White Plains, NY 10604", "http://www.wjdeutsch.com/","(914) 251-9463", "W.J.Deutsch & Sons builds brands that offer approachable wine experiences which contribute to a premium lifestyle for the mainstream and wine enthusiast consumer.", 4)

  TheWineGroupInc = model.Manufacturer(11,"The Wine Group, Inc.", "315 Montgomery St., San Francisco, CA 94104", "http://www.thewinegroup.org/","(415) 986-8700", "The Wine Group, known for its Franzia wine in a box, the company was founded in 1981.", 6)

  BacardiUsaInc = model.Manufacturer(12,"Bacardi USA, Inc.", "2701 Le Jeune Rd., Coral Gables, FL 33134", "http://www.Barcardi.com/","(305) 573-8511", "Bacardi is a family-controlled spirits company, best known as a producer of rums.", 8)

  SchmittSohneInc = model.Manufacturer(13,"Schmitt Sohne, Inc.", "1111 Benfield Blvd., Suite 112, Millersville, MD 21108", "http://www.schmitt-soehne.com/","(410) 729-4083", "Schmitt Sohne is the leading importer of German Rieslings.", 9)

  ChateauMontelena = model.Manufacturer(14,"Chateau Montelena Winery", "1429 Tubbs Lane, Calistoga, CA 94515", "http://www.montelena.com/","(707) 942-5105", "Chateau Montelena is a Napa Valley winery, most famous for winning the white wine section of the historic Judgement of Paris wine competition.", 6)

  

  model.DBSession.add(TallgrassBrewingCo)
  model.DBSession.add(BoulevardBrewingCo)
  model.DBSession.add(KrackenRumCo)
  model.DBSession.add(JohnJamesonandSonsLimited)
  model.DBSession.add(AustinNicholsDistillingCo)
  model.DBSession.add(AnheuserBusch)
  model.DBSession.add(FootHillsBrewing)
  model.DBSession.add(MccormickDistillingCo)
  model.DBSession.add(HobNobWineCo)
  model.DBSession.add(WJDeutschSonsLtd)
  model.DBSession.add(TheWineGroupInc)
  model.DBSession.add(BacardiUsaInc)
  model.DBSession.add(SchmittSohneInc)
  model.DBSession.add(ChateauMontelena)

#
# REGIONS
#
# (id, state, about)
  KS = model.Region(1,"Kansas","It's flat with wheat")
  MO = model.Region(2, "Missouri", "NA")
  NJ = model.Region(3,"New Jersey", "most toxic waste sites in the U.S.")
  NY = model.Region(4, "New York", "something about an apple")
  KY = model.Region(5, "Kentucky", "makers of fine bourbon")
  CA = model.Region(6, "California", "beer, wine, cheese, and movies")
  NC = model.Region(7, "North Carolina", "This is a state located in the southeastern US")
  FL = model.Region(8, "Florida", "Florida is a state in the southeastern United States, located on the nation's Atlantic and Gulf coasts.")
  MD = model.Region(9, "Maryland", "Maryland is a state located in the Mid Atlantic region of the United States, bordering Virginia, West Virginia, and the District of Columbia to its south and west; Pennsylvania to its north; and Delaware to its east.")
  

  model.DBSession.add(KS)
  model.DBSession.add(MO)
  model.DBSession.add(NJ)
  model.DBSession.add(NY)
  model.DBSession.add(KY)
  model.DBSession.add(CA)
  model.DBSession.add(NC)
  model.DBSession.add(FL)
  model.DBSession.add(MD)

#
# FOOD
#
# (id, catbeer id, catwine id, name)
# -1 if null...for now
  Pasta = model.Food(1,-1,1, "Pasta with White Sauce")
  RedMeat = model.Food(2,1,-1, "Red Meat")
  Poultry = model.Food(3,2,-1, "Poultry")
  Fish = model.Food(4,1,-1, "Fish")
  Pork = model.Food(5,2,1, "Pork")

  model.DBSession.add(Pasta)
  model.DBSession.add(RedMeat)
  model.DBSession.add(Poultry)
  model.DBSession.add(Fish)
  model.DBSession.add(Pork)

#
# WINE CATEGORIES
#
# (id, category, style, about, color, grapes)
  Riesling = model.Wine(1,"White", "Riesling", "NA", "Yellow", "Reisling")
  Chardonnay = model.Wine(2,"White", "Chardonnay", "NA", "White", "Chardonnay")
  PinotNoir = model.Wine(3,"Red", "Pinot Noir", "NA", "Red", "Pinot Noir")
  Merlot = model.Wine(4, "Red", "Merlot", "NA", "Red", "Merlot")
  CabernetSauvignon = model.Wine(5, "Red", "Cabernet Sauvignon", "NA", "Red", "NA")

  model.DBSession.add(Riesling)
  model.DBSession.add(Chardonnay)
  model.DBSession.add(PinotNoir)
  model.DBSession.add(Merlot)
  model.DBSession.add(CabernetSauvignon)

#
# LIQUOR CATEGORIES
#
# (id, category, style, about, color, ingredients)
  SpicedRum = model.Liquor(1, "Rum", "Spiced", "caribbean historically", "white-dark brown", "sugar cane")
  Rum = model.Liquor(2,"Rum", "plain", "caribean historicaly", "white-dark brown", "sugar cane")
  Bourbon = model.Liquor(3,"Whiskey", "Bourbon", "Southern U.S.", "amber", "corn")
  Rye = model.Liquor(4, "Whiskey", "Rye", "NA", "amber", "rye")
  Scotch = model.Liquor(5, "Whiskey", "Scotch", "Scotland", "amber", "barley")
  Irish = model.Liquor(6, "Whiskey", "Irish", "Ireland", "amber", "barley")
  Vodka = model.Liquor(7, "Vodka", "Vodka", "Russia", "clear", "potatoes")

  model.DBSession.add(SpicedRum)
  model.DBSession.add(Rum)
  model.DBSession.add(Bourbon)
  model.DBSession.add(Rye)
  model.DBSession.add(Scotch)
  model.DBSession.add(Irish)
  model.DBSession.add(Vodka)

#
# BEER CATEGORIES
#
# (id, category, style, about, color)
  Wheat = model.Beer(1, "Lager" , "Wheat", "made with wheat, sometimes in addition to barley and sometimes entirely of wheat. Often unfiltered", "semi-opaque gold")
  DoubleESB = model.Beer(2, "Ale", "DoubleESB", "extra strong/special bitter", "predominantly dark beers")
  AmberAle = model.Beer(3, "Ale", "Amber Ale", "NA", "amber")
  PaleAle = model.Beer(4, "Ale", "Pale Ale", "NA", "light amber, gold")
  IPA = model.Beer(5, "Ale", "IPA", "Heavily hopped beer", "NA")
  Stout = model.Beer(6, "Ale", "Stout", "lightly hopped and heavily malted beers with well roasted malt", "Dark brown/black")
  AmericanBrownAle = model.Beer(7,"Ale", "American Brown Ale", "often a mix of european malts to create a uniquely American brew", "brown")
  Pilsner = model.Beer(8, "Lager", "Pilsner", "Most produced beer in the world. Examples include Budweiser and Coors", "light gold")
  Porter = model.Beer(9, "Ale", "Porter", "An English beer popular among the working class, the porter is often ligther than the stout with moderate bitterness", "Dark brown to black")

  model.DBSession.add(Wheat)
  model.DBSession.add(DoubleESB)
  model.DBSession.add(AmberAle)
  model.DBSession.add(PaleAle)
  model.DBSession.add(IPA)
  model.DBSession.add(Stout)
  model.DBSession.add(AmericanBrownAle)
  model.DBSession.add(Pilsner)
  model.DBSession.add(Porter)

# Check both constraints

  #error1 = model.Drink(id, "Fail Drink", 200, 1, 10, 10, 10)

  #model.DBSession.add(error1)

#
# DRINKS
#
# (id, name, abv, manu_id, catbeer ID, catLiquor ID, catWine ID)
# -1 if null....for now

  # Beer
  TallgrassHalcyon = model.Drink(1,"Halcyon", 5, 1,1,-1,-1)
  TallgrassAle = model.Drink(2,"Tallgrass Ale", 4.4, 1,7,-1,-1)
  TallgrassOasis = model.Drink(3, "Oasis", 7.2, 1, 2, -1,-1)
  BoulevardAmberAle = model.Drink(4, "Amber Ale", 5.1, 2,3,-1,-1)
  BoulevardPaleAle = model.Drink(5,"Pale Ale", 5.4, 2, 4, -1,-1)

  # Liquor
  TheKrackenBlackSpicedRum = model.Drink(6, "The Kracken Black Spiced Rum", 47, 3,-1,1,-1)
  JamesonIrishWhiskey = model.Drink(7, "Jameson Irish Whiskey", 40, 5,-1,6,-1)
  WildTurkeyBourbon = model.Drink(8, "Wild Turkey", 50.5, 5, -1,3,-1 )
  BacardiSuperior = model.Drink(9, "Bacardi Superior", 40, 12, -1,2,-1)
  McCormickVodka = model.Drink(10, "McCormick Vodka", 40, 8, -1, 7, -1)

  # Wine
  RelaxRiesling = model.Drink(11, "Relax Riesling", 9.5, 13, -1,-1, 1)
  HobnobPinotNoir = model.Drink(12, "Hobnob Pinot Noir", 13, 9, -1,-1,3)
  YellowTailChardonnay = model.Drink(13, "Yellow Tail Chardonnay", 13.5, 10, -1,-1,2)
  FranziaMerlot = model.Drink(14, "Franzia Merlot", 8.8, 11, -1,-1,4)
  MontelenaEstateCabernetSauvignon = model.Drink(15, "Montelena Estate Cabernet Sauvignon", 14.3, -1, -1, -1 , 5)

  Budweiser = model.Drink(16, "Budweiser", 5.5, 6, 8, -1, -1)
  Foothills = model.Drink(17, "Foothills Baltic Porter", 9, 7, 9, -1, -1)

  # beer
  model.DBSession.add(TallgrassHalcyon)
  model.DBSession.add(TallgrassAle)
  model.DBSession.add(TallgrassOasis)
  model.DBSession.add(BoulevardAmberAle)
  model.DBSession.add(BoulevardPaleAle)

  model.DBSession.add(Budweiser)
  model.DBSession.add(Foothills)

  # liquor
  model.DBSession.add(TheKrackenBlackSpicedRum)
  model.DBSession.add(JamesonIrishWhiskey)
  model.DBSession.add(WildTurkeyBourbon)
  model.DBSession.add(BacardiSuperior)
  model.DBSession.add(McCormickVodka)

  # wine
  model.DBSession.add(RelaxRiesling)
  model.DBSession.add(HobnobPinotNoir)
  model.DBSession.add(YellowTailChardonnay)
  model.DBSession.add(FranziaMerlot)
  model.DBSession.add(MontelenaEstateCabernetSauvignon)

  transaction.commit()
  print "successfully setup"
