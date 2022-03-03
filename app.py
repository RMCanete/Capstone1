import os

from flask import Flask, render_template, flash, redirect, session, g
import requests
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserAddForm, LoginForm, CommentForm
from models import db, connect_db, User, Drink, DrinkIngredient, Comment, Ingredient, Favorite

CURR_USER_KEY = "curr_user"

API_BASE_URL = "www.thecocktaildb.com/api/json/v1/1"

# You should keep your API key a secret (I'm keeping it here so you can run this app)
key = '1'

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///capstone_1'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

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
        username = form.username.data
        user_password = form.password.data
        email = form.email.data

        user = User(username=username, user_password=user_password, email=email)
        db.session.add(user)
        db.session.commit()
        flash(f"Added {username}!")

        return redirect("/login")

    else:
        return render_template(
            "user_add_form.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

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


######

"""Homepage"""

@app.route('/')
def homepage():
    """Show homepage"""
    res = requests.get(f"{API_BASE_URL}/random.php", params={"key": 1,})

    data = res.json()
    output = []

    for drink in data['drinks']:

        name = (drink['strDrink'])
        instructions = (drink['strInstructions'])
        image = (drink['strDrinkThumb'])
        ingredient = []
        measurement = []
        for i in range(1,5):
            ingredient.append(drink[f"strIngredient{i}"])
            measurement.append(drink[f"strMeasure{i}"])

        drink = {'name':name, 'instructions':instructions, 'image':image, 'ingredient': ingredient, 'measurement': measurement}
        output.append(drink)

    return render_template('home.html', output=output)

@app.route('/drinks')
def get_drinks():
    """"Call API"""
    # drinks = Drink.query.all()
    
    

@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)

    render_template('view_drink.html', drink=drink)

# @app.route('/drinks/<int:id>', methods=['PATCH'])
# def update_drink_data(id):
#     """Update information about a specific drink"""

#     data = request.json

#     drink = Drink.query.get_or_404(id)

#     drink.drink_id = request.json.get(‘id’, drink.id)
#     drink.drink_ingredients_id = request.json.get(‘drink_ingredients_id’, drink.drink_ingredients_id)
#     drink.drink_instructions = request.json.get(‘drink_instructions’, drink.drink_instructions)
#     drink.drink_image = request.json.get('drink_image', drink.drink_image)

#     db.session.add(drink)
#     db.session.commit()

#     return jsonify(drink=serialize_drinks(drink))


@app.route('/favorites')
def fav():
    """Show favorites"""
    
    return render_template('show_favorites.html')

@app.route('/favorite/<int:id>')
def favId():
    """Show favorite drink"""
    
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

    user = User.query.get_or_404(user_id)

    comments = (Comment.query.filter(Comment.user_id == user_id))

    return render_template('show_user.html', user = user, comments = comments)

