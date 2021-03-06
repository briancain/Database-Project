"""Beer Form"""

from tw.api import WidgetsList
from tw.forms import TableForm, CalendarDatePicker, SingleSelectField, TextField, TextArea


class BeerForm(TableForm):

    class fields(WidgetsList):
        name = TextField()
        category = TextField()
        style = TextField()
        abv = TextField()
        color = TextField()
        brewer = TextField()
        region = TextField()


create_beer_form = BeerForm("create_beer_form", action='beerQ')
