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

    @expose('json')
    #@validate(validators={"page":validators.Int(), "rp":validators.Int()})
    def fetch(self, page=1, rp=25, sortname='id', sortorder='asc', qtype=None, query=None): 
        try: 
            offset = (int(page)-1) * int(rp) 
        except: 
            page = 1 
            rp=25 
            offset = (int(page)-1) * int(rp)
        if (query):
            #d = {qtype:query}
            beers = DBSession.query(Beer)
        else:
            beers = DBSession.query(Beer)
        total = beers.count()
        column = getattr(Beer, sortname)
        #beers = beers.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
        rows = [{'id'  : beer.id,
                 'cell': [beer.id, beer.category, beer.style, beer.about, beer.color]} for beer in beers]
        return dict(page=page, total=total, rows=rows)
