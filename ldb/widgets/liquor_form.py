"""Liquor Form"""

from tw.api import WidgetsList
from tw.forms import TableForm, CalendarDatePicker, SingleSelectField, TextField, TextArea


class LiquorForm(TableForm):

    class fields(WidgetsList):
        name = TextField()
        category = TextField()
        style = TextField()
        abv = TextField()
        color = TextField()
        brewer = TextField()
        region = TextField()


create_liquor_form = LiquorForm("create_liquor_form", action='liquorQ')
