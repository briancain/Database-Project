"""Wine Form"""

from tw.api import WidgetsList
from tw.forms import TableForm, CalendarDatePicker, SingleSelectField, TextField, TextArea


class WineForm(TableForm):

    class fields(WidgetsList):
        name = TextField()
        category = TextField()
        style = TextField()
        abv = TextField()
        color = TextField()
        brewer = TextField()
        region = TextField()


create_wine_form = WineForm("create_wine_form", action='wineQ')
