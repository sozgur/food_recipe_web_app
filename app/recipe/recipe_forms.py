from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets
from app.models import Recipe

times = ["5 mins", "10 mins", "15 mins", "20 mins", "25 mins", "30 mins",
         "35 mins", "40 mins", "45 mins", "50 mins", "55 mins", 
         "1 hour", "1 hour 15 mins", "1 hour 30 mins", "1 hour 45mins", 
         "2 hours", "2 hours 15 mins", "2 hours 30 mins", "2 hours 45mins", 
         "3 hours", "3 hours 15 mins", "3 hours 30 mins", "3 hours 45mins",
         "4 hours", "more than 4 hours"]

prep_times = ["Choose"]
cook_times = ["Choose", "0"]

prep_times.extend(times)
cook_times.extend(times)

class AddRecipeForm(FlaskForm):
    """Form for adding recipe."""

    title = StringField("Title", validators = [DataRequired()])

    ingredients = TextAreaField('Ingredients', validators = [DataRequired()])

    directions = TextAreaField("Directions", validators = [DataRequired()])

    category = SelectField('Category', coerce=int)

    image_url = StringField('(Optional) Image URL')

    calories = HiddenField("Calories")

    prep = SelectField('Prep Time', choices=[(tm, tm) for tm in prep_times], validators = [DataRequired()])

    cook = SelectField('Cook Time', choices=[(tm, tm) for tm in cook_times], validators = [DataRequired()])

    servings = h5fields.IntegerField("Servings", widget=h5widgets.NumberInput(min=1, max=16))

    
class EditRecipeForm(FlaskForm):
    """Form for editing recipe."""

    title = StringField("Title", validators = [DataRequired()])

    ingredients = TextAreaField('Ingredients', validators = [DataRequired()])

    directions = TextAreaField("Directions", validators = [DataRequired()])

    category = SelectField('Category', coerce=int)

    image_url = StringField('(Optional) Image URL')

    calories = HiddenField("Calories")

    prep = SelectField('Prep Time', choices=[(tm, tm) for tm in prep_times], validators = [DataRequired()])

    cook = SelectField('Cook Time', choices=[(tm, tm) for tm in cook_times], validators = [DataRequired()])

    servings = h5fields.IntegerField("Servings", widget=h5widgets.NumberInput(min=1, max=16))
