from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    auth_reset_password = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}" 


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






    