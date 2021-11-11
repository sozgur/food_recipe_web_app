from app.category import category
from flask import render_template
from app.models import Category
from flask_login import login_user, current_user, logout_user, login_required


@category.context_processor
def inject_categories():
    categories = Category.query.order_by('name').all()
    return dict(categories=categories)

@category.route("/categories/<int:category_id>/recipes")
def recipe_list(category_id):
    category = Category.query.get_or_404(category_id)
    recipes = category.recipes
    return render_template("category/recipe_list.html", category=category, recipes = recipes)
