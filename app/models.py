from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin

from datetime import datetime

bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

class Follows(db.Model):
    """Connection of a follower <-> followed_user."""

    __tablename__ = 'follows'

    user_being_followed_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

    user_following_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png"
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    recipes = db.relationship('Recipe', backref='user', cascade="all, delete-orphan")

    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_being_followed_id == id),
        secondaryjoin=(Follows.user_following_id == id)
    )

    following = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_following_id == id),
        secondaryjoin=(Follows.user_being_followed_id == id)
    )

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}" 


    @classmethod
    def register(cls, username, email, first_name, last_name, password):
        """Register user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user


    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct
           Return user if valid; else return False
        """

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user

        # if there is no valid user return False
        return False


    def reset_password(self, password):

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        self.password = hashed_utf8
        self.auth_reset_password = None

        db.session.commit()
        return self


    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_being_followed_id == id),
        secondaryjoin=(Follows.user_following_id == id)
    )

    following = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_following_id == id),
        secondaryjoin=(Follows.user_being_followed_id == id)
    )

    def is_followed_by(self, other_user):
        """Is this user followed by `other_user`?"""

        found_user_list = [user for user in self.followers if user == other_user]
        return len(found_user_list) == 1

    def is_following(self, other_user):
        """Is this user following `other_use`?"""

        found_user_list = [user for user in self.following if user == other_user]
        return len(found_user_list) == 1

class Category(db.Model):
    """Categorty table for each recipe category"""

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    name = db.Column(db.String(50), nullable=False)
    banner_img_url = db.Column(db.Text, nullable=True)

    recipes = db.relationship('Recipe', backref='category', cascade="all, delete-orphan")


# class RecipeBook(db.Model):
#     """Recipe books for user can create recipe list """

#     __tablename__ = "recipebooks"

#     id = db.Column(db.Integer, primary_key=True, nullable=False)

#     name = db.Column(db.String(50), nullable=False)

#     user_id = db.Column(
#         db.Integer, 
#         db.ForeignKey('users.id', ondelete="cascade"), 
#         nullable=False
#     )

#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
#     updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class Recipe(db.Model):

    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    directions = db.Column(db.Text, nullable=False)

    category_id = db.Column(
        db.Integer, 
        db.ForeignKey('categories.id', ondelete='SET NULL'))

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    image_url = db.Column(db.Text, nullable=True)
    approx_calories = db.Column(db.Float, nullable=True)
    serving = db.Column(db.Integer, nullable=False)
    prep = db.Column(db.String(30), nullable=False)
    cook = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    @property
    def img_url(self):

        if self.image_url: 
            return f"{self.image_url}"

        return "/static/images/default-recipe-img.png"


# class RecipeBookEntity(db.Model):

#     __tablename__ = "recipebookentities"

#     book_id = db.Column(
#         db.Integer, 
#         db.ForeignKey('recipebooks.id', ondelete="cascade"), 
#         primary_key=True
#     )

#     recipe_id = db.Column(
#         db.Integer, 
#         db.ForeignKey('recipes.id', ondelete="cascade"), 
#         primary_key=True
#     )























    