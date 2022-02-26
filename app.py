import os
from xml.etree.ElementTree import Comment

from flask import Flask, render_template, flash, request, redirect, session, g
import requests
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import null
from sqlalchemy.exc import IntegrityError
from forms import UserAddForm, LoginForm
from models import db, connect_db, User, Drink

CURR_USER_KEY = "curr_user"

API_BASE_URL = "www.thecocktaildb.com/api/json/v1/1"

# You should keep your API key a secret (I'm keeping it here so you can run this app)
key = '1'

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///capstone_1'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

def serialize_drinks(id):
    """Serialize a cupcake SQLAlchemy obj to dictionary"""

    data = request.json
    return {
        "drink_id": drink.drink_id,
        "drink_ingredients_id": drink.drink_ingredients_id,
        "drink_instructions": drink.drink_instructions,
        "drink_image": drink.drink_image,
    }

def serialize_favorites(id):
    """Serialize a cupcake SQLAlchemy obj to dictionary"""

    data = request.json
    return {
        "favorite_id": favorite.favorite_id,
        "drink_id": favorite.drink_id,
        "user_id": favorite.user_id
    }

def view_favorites():

    data = request.json
    favorites = Favorite.query.all()

    return favorites



@app.route('/')
def homepage():

    return render_template('index.html')

@app.route('/drinks, methods=['GET'])
def get_drink_list():
    """Get information about cupcakes"""

    data = request.json
    drinks = Drink.query.all()
    serialized = [serialize_drinks(d) for d in drinks]

    return drinks=serialized


@app.route('/drinks/<int:id>', methods=['PATCH'])
def update_cupcake_data(id):
    """Update information about a specific cupcake"""

    data = request.json

    drink = Drink.query.get_or_404(id)

    drink.drink_id = request.json.get(‘drink_id’, drink.drink_id)
    drink.drink_ingredients_id = request.json.get(‘drink_ingredients_id’, drink.drink_ingredients_id)
    drink.drink_instructions = request.json.get(‘drink_instructions’, drink.drink_instructions)
    drink.drink_image = request.json.get('drink_image', drink.drink_image)

    db.session.add(drink)
    db.session.commit()

    return jsonify(drink=serialize_drinks(drink))





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


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """User add form; handle adding."""

    form = UserAddForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        flash(f"Added {username}!")
        return redirect("/signup")

    else:
        return render_template(
            "user_add_form.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")


#########################################################
"""Homepage"""

@app.route('/')
def homepage():
    """Show homepage"""
    
    return render_template('home.html')

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    output=[]
    for drink in drinks:
        drink_data = {'name': drink.name, 'description': drink.description}
        output.append(drink_data)



    res = requests.get(f"{API_BASE_URL}", params)
    data = res.json()

    for drink in data['drinks']:
        print(drink[strDrink])
        if drink['strInstructions'] == null:
            print(drink[strInstructions])
    return 
    

@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return drink



    import json
    db.session.add(Drink(name="Cherry", ))
    db.session.commit
    GET
    /drinks/<id>

    POST /Comment
    PUT /comment/<id>
    DELETE /comment/<id>

def get_random_drink():
    res = requests.get(f"{API_BASE_URL}/random.php")
    data = res.json()
    return data


get_drinks(strDrink)
def get_drinks():
    drinks = Drink.query.all()
    output=[]
    for drink in drinks:
        drink_data = {'name': drink.name, 'description': drink.description}
        output.append(drink_data)

get_drink(idDrink)
get_drink_instructions(strInstructions)
get_drink_picture(strDrinkThumb)
get_drink_ingredient(strIngredient1)
get_drink_measurement(strMeasure)
add_comment(user_id, drink_id)


class Get_Drinks
    def __init__()