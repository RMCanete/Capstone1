"""Model for Capstone1 app."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    user_password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<User #{self.user_id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, user_password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = Bcrypt.generate_password_hash(user_password).decode('UTF-8')

        user = User(username=username, email=email, user_password=hashed_pwd)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = Bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False



class Drink(db.Model):
    
    __tablename__ = 'drinks'

    drink_id = db.Column(db.Integer, primary_key=True)
    drink_ingredients_id = db.Column(db.Text, nullable=False)
    drink_image = db.Column(db.Text, nullable=True)
    drink_instructions = db.Column(db.Text, nullable=True)

class Drink_ingredient(db.Model):
    
    __tablename__ = 'drink_ingredients'

    drink_ingredient_id = db.Column(db.Integer, primary_key=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.drink_id', ondelete="cascade"),
        primary_key=True,)
    quantity = db.Column(db.Text, nullable=True)
    measurement_unit = db.Column(db.Text, nullable=True)

class Comment(db.Model):
    
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete="cascade"))
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.drink_id', ondelete="cascade"))
    created_at = db.Column(db.DateTime, nullable=False)

class Ingredient(db.Model):
    
    __tablename__ = 'ingredients'

    ingredient_id = db.Column(db.Integer, primary_key=True)
    drink_ingredient_id = db.Column(db.Integer, db.ForeignKey('Drink_ingredient.drink_ingredient_id', ondelete="cascade"))
    ingredient_name = db.Column(db.Text, nullable=False)

class Favorite(db.Model):
    
    __tablename__ = 'favorites'

    favorite_id = db.Column(db.Integer, primary_key=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.drink_id', ondelete="cascade"))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete="cascade"))


def connect_db(app):
    db.app = app
    db.init_app(app)
