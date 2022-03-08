import os
from sqlite3 import IntegrityError

from flask import Flask, render_template, flash, redirect, session, g, jsonify
import requests
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserAddForm, LoginForm, CommentForm
from models import db, connect_db, User, Drink, DrinkIngredient, Comment, Ingredient, Favorite
from helper import add_drink, check_for_ingredient

CURR_USER_KEY = "curr_user"

base_url="https://www.thecocktaildb.com/api/json/v1/1"


# You should keep your API key a secret (I'm keeping it here so you can run this app)
key = '1'

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql://postgres:2118@localhost/capstone_1'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

"""API CALLS"""

def get_drinks_by_name(name):
    res = requests.get(f"{base_url}/search.php", params={"s": name})
    return res.json()["drinks"][0]

def get_drink_by_id(id):
    res = requests.get(f"{base_url}/lookup.php", params={"i": id})
    return res.json()["drinks"][0]

def get_random_cocktail():
    res = requests.get(f"{base_url}/random.php")
    return res.json()["drinks"][0]

##############################################33
"""User Signup/login/logout"""

@app.before_request
def add_user_to_g():
    """If logged in, add current user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else: g.user = None

def login(user):
    session[CURR_USER_KEY] = user.id

def logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

#### USER ACTIONS ####

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """User add form; handle adding."""

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(username=form.username.data, password=form.password.data, email=form.email.data)
            db.session.commit()
            flash(f"Added {user.username}!")
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('user_add_form.html', form=form)

        login(user)

        return redirect("/favorites")

    else:
        return render_template(
            "login.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            # login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/favorites")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")


######

"""Homepage"""

@app.route('/')
def homepage():
    """Show homepage"""

    random = get_random_cocktail()
    add_drink(random)
    print(random)

    drink = random

    return render_template('home.html', random=random, drink=drink)

@app.route('/drinks')
def get_drinks():
    """"Call API"""

    drinks = Drink.query.all()
    serialized = [drinks.serialize() for d in drinks]

    # jsonify(drinks = serialized)
    return render_template('view_drink.html', drink=serialized)

@app.route('/drinks/<id>')
def get_drink(id):

    ingredient = []
    drink = Drink.query.get_or_404(id)
    drinkIngredient = DrinkIngredient.query.all()
    ingredients = Ingredient.query.all()
    for ingredient in ingredients:
        if check_for_ingredient(ingredient):
            return ingredient.name

    return render_template('view_drink.html', drink=drink, ingredient=ingredient, drinkIngredient=drinkIngredient)


@app.route('/favorites')
def fav():
    """Show favorites"""

    if not g.user:
        flash("Access unauthorized!", "danger")
        return redirect("/")

    favorite = Favorite.query.all()

    return render_template('show_favorites.html', favorite=favorite)

@app.route('/favorite/<int:id>')
def favId():
    """Show favorite drink"""

    if not g.user:
        flash("Access unauthorized!", "danger")
        return redirect("/")

    return render_template('view_favorite_drink.html')

@app.route('/comment/new', methods=["GET", "POST"])
def commentNew():
    """New comment"""
    
    if not g.user:
        flash("Access unauthorized!", "danger")
        return redirect("/")

    form = CommentForm()

    if form.validate_on_submit():
        comment = form.comment.data
        g.user.comments.append(comment)
        db.session.add(comment)
        db.session.commit()
        flash(f"Added {comment}!")

        return redirect(f"/users/{g.user.id}")

    else:
        return render_template(
            "new_comment.html", form=form)

@app.route('/comment/<int:id>', methods=["GET", "PUT", "PATCH"])
def commentId():
    """Show comment"""
    
    comment = Comment.query.get_or_404(id)

    return render_template('view_comment.html', comment=comment)


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show user profile"""

    if not g.user:
        flash("Access unauthorized!", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    comments = (Comment.query.filter(Comment.user_id == user_id))

    return render_template('show_user.html', user = user, comments = comments)