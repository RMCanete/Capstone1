import os
from sqlite3 import IntegrityError
import datetime
# from sqlalchemy.exc import IntegrityError
from flask import Flask, render_template, flash, redirect, request, session, g, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from forms import UserAddForm, LoginForm, CommentForm,CocktailSearch
from models import db, connect_db, User, Drink, DrinkIngredient, Comment, Ingredient, Favorite
from helper import add_drink, check_for_ingredient,parse_drink,check_for_drink
from api import get_drink_by_id,get_drinks_by_name,get_random_cocktail
CURR_USER_KEY = "curr_user"
# FLASK_DEBUG=True

#### Per Heroku, to us SQLAlchemy:

import re

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

# You should keep your API key a secret (I'm keeping it here so you can run this app)
key = '1'

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (uri)
    # os.environ.get('DATABASE_URL', 'postgresql://postgres:2118@localhost/capstone_1'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
#toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

##############################################33
"""User Signup/login/logout"""

@app.before_request
def add_user_to_g():
    """If logged in, add current user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else: g.user = None

def doLogin(user):
    session[CURR_USER_KEY] = user.id

def doLogout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

#### USER ACTIONS ####

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """User add form; handle adding."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(username=form.username.data, password=form.password.data, email=form.email.data)
            db.session.commit()
            flash(f"Added {user.username}!")
        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        doLogin(user)

        return redirect("/")

    else:
        return render_template(
            "signup.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        db.session.commit()

        if user:
            doLogin(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    doLogout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")


######

"""Homepage"""

@app.route('/')
def homepage():
    """Show homepage"""

    if g.user:

        form = CocktailSearch()
        return render_template('home.html', searchForm=form)

    form = LoginForm()    
    return redirect('/login')

@app.route('/drinks/random')
def cocktail_random():
    """Show random cocktail page"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/signup")

    random_cocktail=get_random_cocktail()
    add_drink(random_cocktail)
    print(random_cocktail["idDrink"])
    return redirect(f'/drinks/{random_cocktail["idDrink"]}')


@app.route('/drinks')
def cocktail():
    """Show cocktail"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/signup")

    drink_name=request.args.get('search',None)
    if drink_name:
        cocktails=get_drinks_by_name(drink_name)
        if cocktails:
            for cocktail in cocktails:
                add_drink(cocktail)
            return render_template('cocktail.html',cocktails=cocktails)
        return redirect("/")
        
    drinks = Drink.query.all()
    
    return render_template('cocktail.html',cocktails=drinks)

    # return redirect("/")

@app.route('/drinks/<id>')
def show_cocktail(id):
    """Show random cocktail page"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/signup")

    cocktail = Drink.query.get_or_404(id)
    drink_ingredients = DrinkIngredient.query.filter_by(drink_id=id)
    # add_drink(cocktail)

    return render_template('show_cocktail.html',cocktail=cocktail,drink_ingredients=drink_ingredients)



@app.route('/drinks/<id>/favorites', methods=["POST"])
def fav_drink(id):
    """Show favorites"""

    if not g.user:
        flash("Access unauthorized!", "danger")
        return redirect("/")
    
    drink=check_for_drink(id)
    if not drink:
        cocktail=get_drink_by_id(id)
        add_drink(cocktail)
        drink= Drink.query.get_or_404(id)
    
    user=g.user
    if id not in [drink.id for drink in user.fav_drinks]:
        user.fav_drinks.append(drink)
        db.session.add(user)
        db.session.commit()
    return redirect("/favorites")

@app.route('/drinks/<id>/favorites/delete', methods=["POST"])
def fav_drink_delete(id):
    """Show favorites"""

    if not g.user:
        flash("Access unauthorized!", "danger")
        return redirect("/")

    drink = Drink.query.get_or_404(id)
    db.session.delete(drink)
    db.session.commit()

    return redirect("/favorites")


@app.route('/favorites', methods=["GET"])
def fav():
    """Show favorites"""

    if not g.user:
        flash("Access unauthorized!", "danger")
        return redirect("/")
    
    user = g.user
    comments = Comment.query.all()
    # comments = (Comment.query.filter(user.fav_drinks))

    return render_template('show_favorites.html', drinks=user.fav_drinks, comments=comments)

@app.route('/favorite/<int:id>')
def favId(id):
    """Show favorite drink"""

    if not g.user:
        flash("Access unauthorized!", "danger")
        return redirect("/")
    drink = Drink.query.get_or_404(id)
    comments = Comment.query.all()

    return render_template('view_favorite_drink.html', cocktail=drink, comments=comments)

@app.route('/drinks/<id>/comments', methods=["POST"])
def drink_comment(id):
    """Show favorites"""

    if not g.user:
        flash("Access unauthorized!", "danger")
        return redirect("/")


    drink=check_for_drink(id)
    if not drink:
        cocktail=get_drink_by_id(id)
        add_drink(cocktail)
        drink= Drink.query.get_or_404(id)
    
    user=g.user
    newComment = request.form.get("new_comment")
    comment  = Comment(text=newComment,user_id=user.id,drink_id=id,created_at=datetime.datetime.now())
    db.session.add(comment)
    db.session.commit()
    
    return redirect(f"/drinks/{id}")

@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404