from flask import Blueprint

category = Blueprint('category', __name__)

from . import category_views