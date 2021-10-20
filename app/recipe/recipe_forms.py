from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length
from app.models import Recipe


class AddRecipeForm(FlaskForm):
    """Form for adding recipe."""

    title = StringField("Title", validators = [DataRequired(), Length(min=5, max=100)])

    ingredients = TextAreaField('Ingredients', validators = [DataRequired()])

    description = TextAreaField("Description", validators = [DataRequired()])

    category = SelectField('Category', coerce=int)

    image_url = StringField('(Optional) Image URL')

    calories = HiddenField("Calories")

    
class EditRecipeForm(FlaskForm):
    """Form for editing recipe."""

    title = StringField("Title", validators = [DataRequired(), Length(min=5, max=100)])

    ingredients = TextAreaField('Ingredients', validators = [DataRequired()])

    description = TextAreaField("Description", validators = [DataRequired()])

    category = SelectField('Category', coerce=int)

    image_url = StringField('(Optional) Image URL')

    calories = HiddenField("Calories")
