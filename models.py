"""Model for Capstone1 app."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
# from flask.ext.bcrypt import Bcrypt

bcrypt=Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    fav_drinks = db.relationship(
            "Drink",
            secondary="favorites",
            backref="users"
        )
    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username, email=email, password=hashed_pwd)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False



class Drink(db.Model):
    __tablename__ = 'drinks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text, nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    ingredients = db.relationship(
        "Ingredient",
        secondary="drink_ingredients",
        backref="drinks"
    )

    def serialize(self):
        return {
            "id": self.id,
            "ingredients": [{"name":ing.name, "quantity":ing.quantity, "measument_unit":ing.measurment_unit} for ing in self.ingredients],
            "instructions": self.instructions,
            "image": self.image,
            "name": self.name,
        }

class DrinkIngredient(db.Model):
    
    __tablename__ = 'drink_ingredients'

    id = db.Column(db.Integer, primary_key=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('drinks.id', ondelete="cascade"))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id', ondelete="cascade"))
    quantity = db.Column(db.Text, nullable=True)
    measurement_unit = db.Column(db.Text, nullable=True)

class Comment(db.Model):
    
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))
    drink_id = db.Column(db.Integer, db.ForeignKey('drinks.id', ondelete="cascade"))
    created_at = db.Column(db.DateTime, nullable=False)

class Ingredient(db.Model):
    
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

class Favorite(db.Model):
    
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('drinks.id', ondelete="cascade"))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))

    def serialize(self):
        return {
            "id": self.id,
            "drink_id": self.drink_id,
            "user_id": self.user_id
        }

def connect_db(app):
    db.app = app
    db.init_app(app)
