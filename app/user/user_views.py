from app.user import user
from flask import render_template, url_for, redirect, request, flash, jsonify
from app.models import User, Recipe, Category, db
from flask_login import login_user, current_user, logout_user, login_required




@user.route("/users/<int:user_id>/recipes")
def user_recipes(user_id):
    """Show list of recipes of this user"""
    user = User.query.get_or_404(user_id)
    recipes = Recipe.query.filter_by(user_id=user.id).order_by(Recipe.created_at.desc()).all()
    return render_template("user/profile.html", recipes=recipes, user=user)


@user.route('/users/<int:user_id>/followers')
def users_followers(user_id):
    """Show list of followers of this user."""

    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(user_id)
    return render_template('user/followers.html', user=user)


@user.route('/users/<int:user_id>/following')
def show_following(user_id):
    """Show list of people this user is following."""

    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(user_id)
    return render_template('user/following.html', user=user)


@user.route("/users/toggle_follow/<int:user_id>", methods=["POST"])
@login_required
def toggle_follow(user_id):
    """Follow or unfollow the user by current user"""

    user = User.query.get_or_404(user_id)

    if current_user.is_following(user):
        current_user.following.remove(user)
    else:
        current_user.following.append(user)
    db.session.commit()

    return jsonify({'followers': len(user.followers), 'following': len(user.following)})


@user.context_processor
def inject_categories():
    """
    Get categories for using navbar
    """
    categories = Category.query.order_by('name').all()
    return dict(categories=categories)
