from flask import Blueprint

recipe = Blueprint('recipe', __name__)

from . import recipe_forms, recipe_views, recipe_utils