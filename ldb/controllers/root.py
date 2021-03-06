# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect, validate
from tw.forms.validators import Int, NotEmpty, DateConverter
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from catwalk.tg2 import Catwalk
from repoze.what import predicates
import pylons

from ldb.lib.base import BaseController
from ldb.model import *
from ldb.controllers.error import ErrorController
from ldb import model
from ldb.controllers.secure import SecureController
from tw.jquery import FlexiGrid
from tw.api import js_callback, Resource

from tg import tmpl_context
from ldb.widgets.beer_form import create_beer_form
from ldb.widgets.liquor_form import create_liquor_form
from ldb.widgets.wine_form import create_wine_form
from ldb.widgets.food_form import create_food_form

from sqlalchemy import distinct

from ldb.model.data import Beer

from tw.forms import DataGrid

__all__ = ['RootController']

class RootController(BaseController):
    """
    The root controller for the liquorDatabase application.
    
    All the other controllers and WSGI applications should be mounted on this
    controller. For example::
    
        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()
    
    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.
    
    """
    secc = SecureController()
    
    admin = Catwalk(model, DBSession)
    
    error = ErrorController()

    @expose('ldb.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('ldb.templates.contact')
    def contact(self):
        """Handle the contact page"""
        return dict(page='contact')

    @expose('ldb.templates.region')
    def region(self):
        """Handle the front-page."""
        return dict(page='region')

    @expose('ldb.templates.map_iframe')
    def map_iframe(self):
        """Handle the front-page."""
        return dict(page='map_iframe')

    #@expose('ldb.templates.page')
    #def page(self):
    #   page = DBSession.query(Beer).order_by("id").all()
    #   return dict(beerpage=page)

    @expose('ldb.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    # @expose('ldb.templates.derp')
    #def derp(self):
    #   """Handle the 'derp' page."""
    #  return dict(page='derp')

    @expose('ldb.templates.authentication')
    def auth(self):
        """Display some information about auth* on this application."""
        return dict(page='auth')
    @expose('ldb.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('ldb.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('ldb.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)
    
    @expose()
    def post_login(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.
        
        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect(url('/login', came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.
        
        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)

    @expose('ldb.templates.derp')
    def derp(self):
        return dict(page = 'derp', )

        
    @expose('ldb.templates.wine')
    def wine(self, **kw):
        wine_grid = DataGrid(fields=[('Name','Drink.name'), ('Category', 'Wine.category'), ('Style', 'Wine.style'), ('ABV', 'Drink.abv'), ('Color', 'Wine.color'), ('Brewer', 'Manufacturer.name'), ('Region', 'Region.state')])
        tmpl_context.form = create_wine_form
        
        wineQueryString = 'query(Wine, Drink, Manufacturer, Region).filter(Wine.id == Drink.catW_id).filter(Drink.manu_id == Manufacturer.id).filter(Manufacturer.reg_id == Region.id)'
        if kw:
            name = kw['name']
            if name:
                wineQueryString = wineQueryString + '.filter(Drink.name == \''+ name + '\')'
            category = kw['category']
            if category:
                wineQueryString = wineQueryString + '.filter(Wine.category == \''+ category + '\')'        
            style = kw['style']
            if style:
                wineQueryString = wineQueryString + '.filter(Wine.style == \''+ style + '\')'        
            abv = kw['abv']
            if abv:
                wineQueryString = wineQueryString + '.filter(Drink.abv == \''+ abv + '\')' #may need to be converted to a double!!!
            color = kw['color']
            if color:
                wineQueryString = wineQueryString + '.filter(Wine.color == \''+ color + '\')'
            brewer = kw['brewer']
            if brewer:
                wineQueryString = wineQueryString + '.filter(Manufacturer.name == \''+ brewer + '\')'    
            region = kw['region']
            if region:
                wineQueryString = wineQueryString + '.filter(Region.state == \''+ region + '\')'
        wines = eval('DBSession.' + wineQueryString)
        return dict(page = 'wine', grid = wine_grid, wines = wines, modelname = 'Wine', value = kw )
    
    @expose('ldb.templates.beer')
    def beer(self, **kw):
        """Controller method for the beer page"""
        
        tmpl_context.form = create_beer_form #creates the search form for beers, see widgets/beer_form.py
        # beer_grid is the table which displays all of our data.
        beer_grid = DataGrid(fields=[('Name','Drink.name'),
                                     ('Category', 'Beer.category'),
                                     ('Style', 'Beer.style'),
                                     ('ABV', 'Drink.abv'),
                                     ('Color', 'Beer.color'),
                                     ('Brewer', 'Manufacturer.name'),
                                     ('Region', 'Region.state')])

        """ Search Queries for beer, wine, and liquor work in the following way:
        
               1. The user inputs data into the beer_form displayed on the beer page
               2. When the "submit" button is pressed on the beer_form,
                  RootController.beerQ(see below) is called with the search parameters entered by the user.
               3. beerQ parses out the search parameters, and reloads the beer page with the parameters appended to the URL,
                  the beer method(this one) then builds a database query from these parameters.
               4. The query is executed, and the results are displayed within the beer_grid table.
        """
        
        beerQueryString = 'query(Beer, Drink, Manufacturer, Region)'
                         + '.filter(Beer.id == Drink.catB_id)'
                         + '.filter(Drink.manu_id == Manufacturer.id)'
                         + '.filter(Manufacturer.reg_id == Region.id)'
        if kw:
            name = kw['name']
            if name:
                beerQueryString = beerQueryString + '.filter(Drink.name == \''+ name + '\')'
            category = kw['category']
            if category:
                beerQueryString = beerQueryString + '.filter(Beer.category == \''+ category + '\')'        
            style = kw['style']
            if style:
                beerQueryString = beerQueryString + '.filter(Beer.style == \''+ style + '\')'        
            abv = kw['abv']
            if abv:
                beerQueryString = beerQueryString + '.filter(Drink.abv == \''+ abv + '\')' #may need to be converted to a double!!!
            color = kw['color']
            if color:
                beerQueryString = beerQueryString + '.filter(Beer.color == \''+ color + '\')'
            brewer = kw['brewer']
            if brewer:
                beerQueryString = beerQueryString + '.filter(Manufacturer.name == \''+ brewer + '\')'    
            region = kw['region']
            if region:
                beerQueryString = beerQueryString + '.filter(Region.state == \''+ region + '\')'
        beers = eval('DBSession.' + beerQueryString)
        return dict(page = 'beer', grid = beer_grid, beers = beers, modelname = 'Beer', value = kw )

      
    @expose('ldb.templates.liquor')
    def liquor(self, **kw):
        liquor_grid = DataGrid(fields=[('Name','Drink.name'), ('Category', 'Liquor.category'), ('Style', 'Liquor.style'), ('ABV', 'Drink.abv'), ('Color', 'Liquor.color'), ('Brewer', 'Manufacturer.name'), ('Region', 'Region.state')])
        tmpl_context.form = create_liquor_form
        
        liquorQueryString = 'query(Liquor, Drink, Manufacturer, Region).filter(Liquor.id == Drink.catL_id).filter(Drink.manu_id == Manufacturer.id).filter(Manufacturer.reg_id == Region.id)'
        if kw:
            name = kw['name']
            if name:
                liquorQueryString = liquorQueryString + '.filter(Drink.name == \''+ name + '\')'
            category = kw['category']
            if category:
                liquorQueryString = liquorQueryString + '.filter(Liquor.category == \''+ category + '\')'        
            style = kw['style']
            if style:
                liquorQueryString = liquorQueryString + '.filter(Liquor.style == \''+ style + '\')'        
            abv = kw['abv']
            if abv:
                liquorQueryString = liquorQueryString + '.filter(Drink.abv == \''+ abv + '\')' #may need to be converted to a double!!!
            color = kw['color']
            if color:
                liquorQueryString = liquorQueryString + '.filter(Liquor.color == \''+ color + '\')'
            brewer = kw['brewer']
            if brewer:
                liquorQueryString = liquorQueryString + '.filter(Manufacturer.name == \''+ brewer + '\')'    
            region = kw['region']
            if region:
                liquorQueryString = liquorQueryString + '.filter(Region.state == \''+ region + '\')'
        liquors = eval('DBSession.' + liquorQueryString)
        return dict(page = 'liquor', grid = liquor_grid, liquors = liquors, modelname = 'Liquor', value = kw )


    @expose('ldb.templates.food')
    def food(self, **kw):
        food_wine_grid = DataGrid(fields=[('Wine Name', 'Drink.name'), ('Category', 'Wine.category'), ('ABV', 'Drink.abv'),
          ('Grapes', 'Wine.grapes'), ('Food Name', 'Food.name')])
        food_beer_grid = DataGrid(fields=[('Beer Name','Drink.name'), ('Category', 'Beer.category'), ('Style', 'Beer.style'), ('ABV', 'Drink.abv'), ('Food Name', 'Food.name')])
        tmpl_context.form = create_food_form
        
        wineQueryString = 'query(Food, Drink, Wine).filter(Wine.id == Drink.catW_id).filter(Food.catW_id == Drink.catW_id)'
        beerQueryString = 'query(Food, Drink, Beer).filter(Beer.id == Drink.catB_id).filter(Food.catB_id == Drink.catB_id)'

        if kw:
            name = kw['name']
            if name == '0':
              name = 'Pasta With White Sauce'
            elif name == '1':
              name = 'Pasta With Red Sauce'
            elif name == '2':
              name = 'Red Meat'
            elif name == '3':
              name = 'Poultry'

            if name:
                wineQueryString = wineQueryString + '.filter(Food.name == \''+ name + '\')'
                beerQueryString = beerQueryString + '.filter(Food.name == \''+ name + '\')'

        wines = eval('DBSession.' + wineQueryString)
        beers = eval('DBSession.' + beerQueryString)
        return dict(page = 'food', grid = food_wine_grid, gridbeer = food_beer_grid, wines = wines, beers = beers, modelname = 'Food', value = kw )

    @expose()
    def foodQ(self, **kw):
        """Query from the from on the food page"""
        name = kw['name']
        redirect('./food?name='+name)

    @expose()
    def beerQ(self, **kw):
        """Query from the form on the beer page"""
        #set up parameters
        name = kw['name']
        category = kw['category']
        style = kw['style']
        abv = kw['abv']
        color = kw['color']
        brewer = kw['brewer']
        region = kw['region']
        redirect('./beer?name='+name+'&category='+category+'&style='+style+'&abv='+abv+'&color='+color+'&brewer='+brewer+'&region='+region)

    @expose()
    def liquorQ(self, **kw):
        """Query from the form on the liquor page"""
        #set up parameters
        name = kw['name']
        category = kw['category']
        style = kw['style']
        abv = kw['abv']
        color = kw['color']
        brewer = kw['brewer']
        region = kw['region']
        redirect('./liquor?name='+name+'&category='+category+'&style='+style+'&abv='+abv+'&color='+color+'&brewer='+brewer+'&region='+region)

        
    @expose()
    def wineQ(self, **kw):
        """Query from the form on the wine page"""
        #set up parameters
        name = kw['name']
        category = kw['category']
        style = kw['style']
        abv = kw['abv']
        color = kw['color']
        brewer = kw['brewer']
        region = kw['region']
        redirect('./wine?name='+name+'&category='+category+'&style='+style+'&abv='+abv+'&color='+color+'&brewer='+brewer+'&region='+region)
  
