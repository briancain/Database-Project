"""Beer Form"""

from tw.api import WidgetsList
from tw.forms import TableForm, CalendarDatePicker, SingleSelectField, TextField, TextArea


class BeerForm(TableForm):

    class fields(WidgetsList):
        category = TextField()
        style = TextField()
        color = TextField()


create_beer_form = BeerForm("create_beer_form")
