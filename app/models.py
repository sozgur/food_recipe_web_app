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

    user_follower_id = db.Column(
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
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

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
        primaryjoin=(Follows.user_follower_id == id),
        secondaryjoin=(Follows.user_following_id == id)
    )

    following = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_following_id == id),
        secondaryjoin=(Follows.user_follower_id == id)
    )

    class Category(db.Model):
        """Categorty table for each recipe category"""

        __tablename__ = "categories"

        id = db.Column(db.Integer, primary_key=True, nullable=False)

        name = db.Column(db.String(50), nullable=False)


    class RecipeBook(db.Model):
        """Recipe books for user can create recipe list """

        __tablename__ = "recipebooks"

        id = db.Column(db.Integer, primary_key=True, nullable=False)

        name = db.Column(db.String(50), nullable=False)

        user_id = db.Column(
            db.Integer, 
            db.ForeignKey('users.id', ondelete="cascade"), 
            nullable=False
        )

        created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
        updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


    class Recipe(db.Model):

        __tablename__ = "recipes"

        id = db.Column(db.Integer, primary_key=True, nullable=False)
        title = db.Column(db.String(150), nullable=False)
        ingredient = db.Column(db.Text, nullable=False)
        description = db.Column(db.Text, nullable=False)
        category_id = db.Column(
            db.Integer, 
            db.ForeignKey('categories.id', ondelete='SET NULL'))
        total_rate = db.Column(db.Integer, nullable=True)
        average_rate = db.Column(db.Float, nullable=True)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
        updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())


    class RecipeBookEntity(db.Model):

        __tablename__ = "recipebookentities"

        book_id = db.Column(
            db.Integer, 
            db.ForeignKey('recipebooks.id', ondelete="cascade"), 
            primary_key=True
        )

        recipe_id = db.Column(
            db.Integer, 
            db.ForeignKey('recipes.id', ondelete="cascade"), 
            primary_key=True
        )



    class Rate(db.Model):

        __tablename__ = "rates"

        id = db.Column(db.Integer, primary_key=True, nullable=False)
        rate = db.Column(db.Integer, nullable=False)

        user_id = db.Column(
            db.Integer, 
            db.ForeignKey('users.id', ondelete="SET NULL")
        )

        recipe_id = db.Column(
            db.Integer, 
            db.ForeignKey('recipes.id', ondelete="cascade"), 
            nullable=False
        )























    