import os, requests
from app.recipe import recipe
from flask import render_template, url_for, redirect, request, flash, jsonify
from app.models import Recipe, Category, db
from flask_login import login_user, current_user, logout_user, login_required

from .recipe_forms import AddRecipeForm, EditRecipeForm
# from .auth_utils import token_generator, token_get_user_id


#TODO:Remove it
@recipe.route("/")
def home_page():
    """Home page for test"""
    return render_template("index.html")


@login_required
@recipe.route("/add-recipe", methods=["GET", "POST"])
def add_recipe():

    form = AddRecipeForm()

    categories = [(c.id, c.name) for c in Category.query.order_by('name')]
    form.category.choices=categories

    if form.validate_on_submit():

        image_url = form.image_url.data if form.image_url.data else None
        calories = form.calories.data if form.calories.data else None

        recipe = Recipe(title=form.title.data, ingredients=form.ingredients.data, 
            description = form.description.data, category_id = form.category.data,
            image_url=image_url, approx_calories=calories)

        db.session.add(recipe)
        db.session.commit()

        return redirect(url_for("recipe.detail", recipe_id=recipe.id))


    return render_template("recipe/create.html", form=form)


@login_required
@recipe.route("/detail/<int:recipe_id>", methods=["GET"])
def detail(recipe_id):
    return render_template("recipe/detail.html")


@recipe.route("/calculate-calories/json", methods=["POST"])
def calculate_calories():

    ingredients = request.json["ingredients"]
   
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(ingredients)
    response = requests.get(api_url, headers={'X-Api-Key': os.environ.get('API_KEY')})

    if response.status_code == requests.codes.ok:
        incredients = response.json()
        total_calories = 0
        for ing in incredients:
            total_calories += ing["calories"]

        return jsonify({'calories': round(total_calories, 2)})

    else:
        return jsonify({'error': "Can't calculate calories"}), 204
