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
from tw.api import js_callback

from tg import tmpl_context
from ldb.widgets.beer_form import create_beer_form

from ldb.model.data import Beer

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
        colModel = [
            {'display':'ID', 'name':'id', 'width':20, 'align':'center'},
            {'display':'Category', 'name':'category', 'width':140, 'align':'left'},
            {'display':'Style', 'name':'style', 'width':140, 'align':'left'},
            {'display':'About', 'name':'about', 'width':220, 'align':'center'},
            {'display':'Color', 'name':'color', 'width':120, 'align':'center'}
        ]
        searchitems = [
            {'display':'ID', 'name':'id', 'isdefault':True},
            {'display':'Category', 'name':'category'},
            {'display':'Style', 'name':'style'}
        ]
        grid = FlexiGrid(id='flex', fetchURL='fetch', title='Beer',
            colModel=colModel, useRp=True, rp=10,
            sortname='id', sortorder='asc', usepager=True,
            searchitems=searchitems,
            showTableToggleButton=True,
       #    buttons=buttons,
            width=700,
            height=200
        )
        pylons.tmpl_context.grid = grid
        beers = DBSession.query( Beer ).order_by( Beer.id )
        return dict(page = 'derp',
                    beers = beers, )


    @expose('ldb.templates.wine')
    def wine(self):
        colModel = [
            {'display':'Name', 'name':'name', 'width':180, 'align':'center'},
            {'display':'Category', 'name':'category', 'width':60, 'align':'left'},
            {'display':'Style', 'name':'style', 'width':140, 'align':'left'},
            {'display':'ABV', 'name':'about', 'width':40, 'align':'center'},
            {'display':'Color', 'name':'color', 'width':120, 'align':'center'},
            {'display':'Brewer', 'name':'brewer', 'width':120, 'align':'center'},
            {'display':'Region', 'name':'region', 'width':120, 'align':'center'}
        ]
        searchitems = [
            {'display':'ID', 'name':'id', 'isdefault':True},
            {'display':'Category', 'name':'category'},
            {'display':'Style', 'name':'style'}
        ]
        grid = FlexiGrid(id='flex', fetchURL='fetchW', title='Wine',
            colModel=colModel, useRp=True, rp=10,
            sortname='id', sortorder='asc', usepager=True,
            searchitems=searchitems,
            showTableToggleButton=True,
       #    buttons=buttons,
            width=881,
            height=200
        )
        pylons.tmpl_context.grid = grid
        wines = DBSession.query( Wine ).order_by( Wine.id )
        return dict(page = 'wine',
                    wines = wines, )


    @expose('ldb.templates.beer')
    def beer(self, **kw):
        colModel = [
            {'display':'Name', 'name':'name', 'width':180, 'align':'center'},
            {'display':'Category', 'name':'category', 'width':60, 'align':'left'},
            {'display':'Style', 'name':'style', 'width':140, 'align':'left'},
            {'display':'ABV', 'name':'about', 'width':40, 'align':'center'},
            {'display':'Color', 'name':'color', 'width':120, 'align':'center'},
            {'display':'Brewer', 'name':'brewer', 'width':120, 'align':'center'},
            {'display':'Region', 'name':'region', 'width':120, 'align':'center'}
        ]
        searchitems = [
            {'display':'ID', 'name':'id', 'isdefault':True},
            {'display':'Category', 'name':'category'},
            {'display':'Style', 'name':'style'}
        ]
        grid = FlexiGrid(id='flex', fetchURL='fetchB', title='Beer',
            colModel=colModel, useRp=True, rp=10,
            sortname='id', sortorder='asc', usepager=True,
            searchitems=searchitems,
            showTableToggleButton=True,
       #    buttons=buttons,
            width=881,
            height=200
        )
        pylons.tmpl_context.grid = grid
        tmpl_context.form = create_beer_form
        #beers = DBSession.query( Beer ).order_by( Beer.id )
        return dict(page = 'beer', modelname='Beer', value=kw, )

    
    @expose('ldb.templates.liquor')
    def liquor(self):
        colModel = [
            {'display':'Name', 'name':'name', 'width':180, 'align':'center'},
            {'display':'Category', 'name':'category', 'width':60, 'align':'left'},
            {'display':'Style', 'name':'style', 'width':140, 'align':'left'},
            {'display':'ABV', 'name':'about', 'width':40, 'align':'center'},
            {'display':'Color', 'name':'color', 'width':120, 'align':'center'},
            {'display':'Brewer', 'name':'brewer', 'width':120, 'align':'center'},
            {'display':'Region', 'name':'region', 'width':120, 'align':'center'}
        ]
        searchitems = [
            {'display':'ID', 'name':'id', 'isdefault':True},
            {'display':'Category', 'name':'category'},
            {'display':'Style', 'name':'style'}
        ]
        grid = FlexiGrid(id='flex', fetchURL='fetchL', title='Liquor',
            colModel=colModel, useRp=True, rp=10,
            sortname='id', sortorder='asc', usepager=True,
            searchitems=searchitems,
            showTableToggleButton=True,
       #    buttons=buttons,
            width=881,
            height=200
        )
        pylons.tmpl_context.grid = grid
        liquors = DBSession.query( Liquor ).order_by( Liquor.id )
        return dict(page = 'liquor',
                    liquors = liquors, )
    @expose('json')
    #@validate(validators={"page":validators.Int(), "rp":validators.Int()})
    def fetchB(self, page=1, rp=25, sortname='id', sortorder='asc', qtype=None, query=None): 
        try: 
            offset = (int(page)-1) * int(rp) 
        except: 
            page = 1 
            rp=25 
            offset = (int(page)-1) * int(rp)
        if (query):
            #d = {qtype:query}
            beers = DBSession.query(Beer, Drink, Manufacturer, Region).filter(Beer.id == Drink.catB_id).filter(Drink.manu_id == Manufacturer.id).filter(Manufacturer.reg_id == Region.id)
        else:
            beers = DBSession.query(Beer, Drink, Manufacturer, Region).filter(Beer.id == Drink.catB_id).filter(Drink.manu_id == Manufacturer.id).filter(Manufacturer.reg_id == Region.id)
        total = beers.count()
        #column = getattr(Beer, sortname)
        #beers = beers.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
        rows = [{'id'  : beer.Beer.id, 'cell': [beer.Drink.name, beer.Beer.category, beer.Beer.style, beer.Drink.abv, beer.Beer.color, beer.Manufacturer.name, beer.Region.state]} for beer in beers]
        return dict(page=page, total=total, rows=rows)

    @expose('json')
    #@validate(validators={"page":validators.Int(), "rp":validators.Int()})
    def fetchW(self, page=1, rp=25, sortname='id', sortorder='asc', qtype=None, query=None): 
        try: 
            offset = (int(page)-1) * int(rp) 
        except: 
            page = 1 
            rp=25 
            offset = (int(page)-1) * int(rp)
        if (query):
            #d = {qtype:query}
            wines = DBSession.query(Wine, Drink, Manufacturer, Region).filter(Wine.id == Drink.catW_id).filter(Drink.manu_id == Manufacturer.id).filter(Manufacturer.reg_id == Region.id)
        else:
            wines = DBSession.query(Wine, Drink, Manufacturer, Region).filter(Wine.id == Drink.catW_id).filter(Drink.manu_id == Manufacturer.id).filter(Manufacturer.reg_id == Region.id)

        total = wines.count()
        rows = [{'id'  : wine.Wine.id,
                 'cell': [wine.Drink.name, wine.Wine.category, wine.Wine.style, wine.Drink.abv, wine.Wine.color, wine.Manufacturer.name, wine.Region.state]} for wine in wines]
        return dict(page=page, total=total, rows=rows)


    @expose('json')
    #@validate(validators={"page":validators.Int(), "rp":validators.Int()})
    def fetchL(self, page=1, rp=25, sortname='id', sortorder='asc', qtype=None, query=None): 
        try: 
            offset = (int(page)-1) * int(rp) 
        except: 
            page = 1 
            rp=25 
            offset = (int(page)-1) * int(rp)
        if (query):
            #d = {qtype:query}
            liquors = DBSession.query(Liquor, Drink, Manufacturer, Region).filter(Liquor.id == Drink.catL_id).filter(Drink.manu_id == Manufacturer.id).filter(Manufacturer.reg_id == Region.id)
        else:
            liquors = DBSession.query(Liquor, Drink, Manufacturer, Region).filter(Liquor.id == Drink.catL_id).filter(Drink.manu_id == Manufacturer.id).filter(Manufacturer.reg_id == Region.id)
        total = liquors.count()
        column = getattr(Liquor, sortname)
        #beers = beers.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
        rows = [{'id'  : liquor.Liquor.id,
                 'cell': [liquor.Drink.name, liquor.Liquor.category, liquor.Liquor.style, liquor.Drink.abv, liquor.Liquor.color, liquor.Manufacturer.name, liquor.Region.state]} for liquor in liquors]
        return dict(page=page, total=total, rows=rows)

    @expose('ldb.templates.beer_form')
    def beerF(self, **kw):
        """Show form to add new movie data record."""
        tmpl_context.form = create_beer_form
        return dict(modelname='Beer', value=kw)

    @expose()
    def beerQ(self, **kw):
        """Query from the form on the beer page"""
        #set up parameters
        beer = Beer()
        beer.color = kw['color']
        beer.id = kw['id']
        beer.style = kw['style']
        beer.category = kw['category']

        #query the DB session
        #DBSession.query( Beer )


    @expose('ldb.templates.food')
    def food(self):
        """Handle the food-page."""
        return dict(page='food')
