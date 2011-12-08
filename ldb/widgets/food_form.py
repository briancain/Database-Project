"""Wine Form"""

from tw.api import WidgetsList
from tw.forms import TableForm, CalendarDatePicker, SingleSelectField, TextField, TextArea


class FoodForm(TableForm):

    class fields(WidgetsList):
        name_options = [x for x in enumerate(('Pasta With White Sauce', 
                  'Pasta With Red Sauce', 'Red Meat', 'Poultry'))]
        name = SingleSelectField(options=name_options)


create_food_form = FoodForm("create_food_form", action='foodQ')
