"""Wine Form"""

from tw.api import WidgetsList
from tw.forms import TableForm, CalendarDatePicker, SingleSelectField, TextField, TextArea


class FoodForm(TableForm):

    class fields(WidgetsList):
        name = TextField()


create_food_form = FoodForm("create_food_form", action='foodQ')
