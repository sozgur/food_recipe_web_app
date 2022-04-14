from app.auth import auth
from flask import render_template, url_for, redirect, flash
from app.models import User, Category, db
from app.email import send_email
from flask_login import login_user, current_user, logout_user, login_required
from .auth_forms import RegisterForm, LoginForm, ForgotPasswordForm, CreateNewPasswordForm, UserEditForm
from .auth_utils import token_generator, token_get_user_id


@auth.context_processor
def inject_categories():
    """
    Get categories for using navbar
    """
    categories = Category.query.order_by('name').all()
    return dict(categories=categories)


@auth.route('/register', methods=["GET", "POST"])
def register():
    """
    Create a new user and add to DB. Redirect to user page

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form  = RegisterForm()

    if form.validate_on_submit():

        image_url = form.image_url.data if form.image_url.data else None
        
        new_user = User.register(form.username.data, form.email.data, form.first_name.data, 
            form.last_name.data, form.password.data, image_url)
        db.session.add(new_user)
        db.session.commit()

        flash('Successfully Created Your Account!', "success")
        return redirect("/login")

    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login exiting user and redirect to user page
    If form not valid, present form.
    """

    form = LoginForm()

    if current_user.is_authenticated:
        flash("Aldready login", 'info')
        return redirect("/")

    if form.validate_on_submit():
        # Login and validate the user.
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            login_user(user)
            flash('Logged in successfully.', "success")
            return redirect('/')

        else:
            flash("Invalid Username or Password", "warning")


    return render_template('auth/login.html', form=form)


@auth.route('/profile/edit', methods=["GET", "POST"])
def edit_profile():
    """Update profile for current user."""

    if not current_user.is_authenticated:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    form = UserEditForm(obj=current_user)

    if form.validate_on_submit():

        if User.authenticate(current_user.username, form.password.data):
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.image_url = form.image_url.data

            db.session.commit()
            return redirect(url_for('user.user_recipes', user_id=current_user.id))

        flash("Wrong password, please try again.", 'danger')

    return render_template('auth/edit.html', form=form, user_id=current_user.id)



@auth.route("/logout")
@login_required
def sign_out():
    logout_user()
    return redirect('/')


#### send message ####
@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password_form():
    """Show forgot password form and send a reset email
       Create and save token on user column
    """
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            reset_key = token_generator(user)
            user.auth_reset_password = reset_key
            db.session.commit()

            send_email(user.email, 'Reset Your Password', 'auth/email/reset', user=user,
                   reset_key=reset_key)

            flash(f"We send you email for reset your password to {user.email}. Please check your email.", "success")
            return redirect("/")

    return render_template("auth/forgot_password.html", form=form)


@auth.route("/reset/<reset_key>", methods=["GET", "POST"])
def reset_password(reset_key):
    """Reset password and delete a token"""

    form = CreateNewPasswordForm()
    user_id = token_get_user_id(reset_key)

    if user_id:
        user = User.query.get_or_404(user_id)

        if form.validate_on_submit():
            password = form.password.data
            user.reset_password(password)
            return redirect(url_for('auth.login'))

        if user:
            return render_template("auth/reset_password.html", form=form)


@auth.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""
    return render_template('404.html'), 404





