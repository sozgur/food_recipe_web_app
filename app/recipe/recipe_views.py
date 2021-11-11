import os, requests
from app.recipe import recipe
from flask import render_template, url_for, redirect, request, flash, jsonify
from app.models import Recipe, Category, db
from flask_login import login_user, current_user, logout_user, login_required

from .recipe_forms import AddRecipeForm, EditRecipeForm
# from .auth_utils import token_generator, token_get_user_id


@recipe.route("/")
def home_page():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template("index.html", recipes=recipes)



@recipe.route("/add-recipe", methods=["GET", "POST"])
def add_recipe():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    form = AddRecipeForm()

    categories = [(c.id, c.name) for c in Category.query.order_by('name')]
    form.category.choices=categories

    if form.validate_on_submit():

        image_url = form.image_url.data if form.image_url.data else None
        calories = form.calories.data if form.calories.data else None

        recipe = Recipe(title=form.title.data, ingredients=form.ingredients.data, 
            directions = form.directions.data, category_id = form.category.data,
            image_url=image_url, approx_calories=calories, prep=form.prep.data,
            cook=form.cook.data, serving=form.servings.data, user_id = current_user.id)

        db.session.add(recipe)
        db.session.commit()

        return redirect(url_for("recipe.detail", recipe_id=recipe.id))


    return render_template("recipe/create.html", form=form)


@recipe.route("/recipe/<int:recipe_id>/edit", methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    
    recipe = Recipe.query.get_or_404(recipe_id)

    form = EditRecipeForm(obj=recipe)

    categories = [(c.id, c.name) for c in Category.query.order_by('name')]
    form.category.choices=categories

    # form.category.default = recipe.category_id
    # form.servings.default = recipe.serving 
    # form.title.default = recipe.title 
    # form.ingredients.default = recipe.ingredients
    # form.directions.default = recipe.directions 
    # form.image_url.default = recipe.image_url
    # form.calories.default = recipe.approx_calories
    # form.prep.default = recipe.prep
    # form.cook.default = recipe.cook
    # form.process()


    if form.validate_on_submit():

        image_url = form.image_url.data if form.image_url.data else None
        calories = form.calories.data if form.calories.data else None

        recipe.title = form.title.data
        recipe.ingredients = form.ingredients.data
        recipe.directions = form.directions.data
        recipe.category_id = form.category.data
        recipe.image_url=image_url
        recipe.approx_calories=calories
        recipe.prep=form.prep.data
        recipe.cook=form.cook.data
        recipe.serving=form.servings.data

        db.session.commit()

        flash(f"{recipe.title} Updated!", "success")
        return redirect(url_for("recipe.detail", recipe_id=recipe.id))

    return render_template("recipe/edit.html", form=form, recipe = recipe)


@recipe.route("/recipe/<int:recipe_id>/delete", methods=["POST"])
@login_required
def delete_recipe(recipe_id):

    recipe = Recipe.query.get_or_404(recipe_id)

    user_id = recipe.user.id

    db.session.delete(recipe)
    db.session.commit()

    return redirect(url_for('user.user_recipes', user_id=user_id))


@recipe.route("/detail/<int:recipe_id>", methods=["GET"])
def detail(recipe_id):

    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.approx_calories:
        per_serving = recipe.approx_calories // recipe.serving 
    else:
        per_serving = "Can't calculated"

    return render_template("recipe/detail.html", recipe = recipe, per_serving = per_serving )



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


@recipe.context_processor
def inject_categories():
    categories = Category.query.order_by('name').all()
    return dict(categories=categories)