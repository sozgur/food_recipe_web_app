from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User


class RegisterForm(FlaskForm):
    """Form for adding users."""

    username = StringField("Username", validators = [DataRequired(), Length(min=4, max=30)])

    email = StringField('Email Address', validators = [DataRequired(), Email()])

    first_name = StringField("First Name", validators = [DataRequired()])

    last_name = StringField("Last Name", validators = [DataRequired()])

    password = PasswordField('Password', validators=[DataRequired(), 
        Length(min=6, message="Password must be at least 6 characters long.")])

    confirm  = PasswordField('Confirm Password', validators=[DataRequired(), 
        EqualTo('password', message='Passwords must be match.')])


    def validate_username(self, username):
        # check if the username data exists in the form
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username Already Exists')

    def validate_email(self, email):
        # check if the email data exist in the form
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email Already Exists')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])

    password = PasswordField('Password', validators=[Length(min=6)])



class ForgotPasswordForm(FlaskForm):

    email = StringField('Email Address', validators = [DataRequired(), 
    Email(message="Please enter a valid email"), Length(min=6, max=35)])

    def validate_email(self, email):
        # check if the email data exist in the form
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError("Your email doesn't exits in our database.")


class CreateNewPasswordForm(FlaskForm):

    password = PasswordField('New Password', validators=[DataRequired(), 
        EqualTo('confirm', message='Passwords must be match')])
    confirm  = PasswordField('Repeat Password')
