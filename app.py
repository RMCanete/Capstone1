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

# You should keep your API key a secret (I'm keeping it here so you can run this app)
key = '1'

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql://postgres:2118@localhost/capstone_1'))

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
        return render_template('new_home.html', searchForm=form)

    form = LoginForm()    
    return redirect('/login')

@app.route('/cocktail/random')
def cocktail_random():
    """Show random cocktail page"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/signup")

    random_cocktail=get_random_cocktail()

    form = CommentForm()

    return render_template('random_cocktail.html',cocktail=parse_drink(random_cocktail), form=form)


@app.route('/cocktail')
def cocktail():
    """Show cocktail"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/signup")

    # drink_name=request.args.get('search',None)
    # if drink_name:
    #     cocktails=get_drinks_by_name(drink_name)
    #     if cocktails:
    #         return render_template('cocktail.html',cocktails=cocktails)
    #     return redirect("/")
        
    drinks = Drink.query.all()
    
    return render_template('cocktail.html',cocktails=drinks)

    # return redirect("/")

@app.route('/cocktail/<id>')
def show_cocktail(id):
    """Show random cocktail page"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/signup")

    cocktail = Drink.query.get_or_404(id)
    drink_ingredients = DrinkIngredient.query.all()
    ingredients = Ingredient.query.all()

    # add_drink(cocktail)

    return render_template('show_cocktail.html',cocktail=cocktail, drink_ingredients=drink_ingredients, ingredients=ingredients)



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
    return redirect("/")

@app.route('/drinks/<id>/favorites/delete', methods=["POST"])
def fav_drink_delete(id):
    """Show favorites"""

    if not g.user:
        flash("Access unauthorized!", "danger")
        return redirect("/")

    user=g.user
    if id in [drink.id for drink in user.fav_drinks]:
        user.fav_drinks=[drink for drink in user.fav_drinks if drink.id != id]
        db.session.delete(id)
        db.session.commit()
    return redirect("/favorites")


@app.route('/favorites', methods=["GET"])
def fav():
    """Show favorites"""

    if not g.user:
        flash("Access unauthorized!", "danger")
        return redirect("/")
    
    user = g.user
    return render_template('show_favorites_v2.html', drinks=user.fav_drinks)


@app.route('/favorite/<int:id>')
def favId(id):
    """Show favorite drink"""

    if not g.user:
        flash("Access unauthorized!", "danger")
        return redirect("/")
    drink = Drink.query.get_or_404(id)

    return render_template('view_favorite_drink.html', cocktail=drink)

@app.route('/comment/new', methods=["GET", "POST"])
def commentNew():
    """New comment"""
    
    if not g.user:
        flash("Access unauthorized!", "danger")
        return redirect("/")
    user = g.user
    form = CommentForm(obj=user)

    if form.validate_on_submit():
        comment = form.comment.data
        print(comment)
        # db.session.add(comment)
        db.session.commit()
        flash(f"Added {comment}!")
        return redirect(f"/users/{g.user.id}")

    else:
        return render_template(
            "new_comment.html", form=form)


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
    comment  = Comment(text=newComment,user_id=g.user.id,drink_id=id,created_at=datetime.datetime.now())
    db.session.add(comment)
    db.session.commit()
    
    return redirect("/comments")

    # if id not in [drink.id for drink in user.fav_drinks]:



@app.route('/comment/<int:id>', methods=["GET", "PUT", "PATCH"])
def commentId(id):
    """Show comment"""
    
    comment = Comment.query.get_or_404(id)
    cocktail = Drink.query.get_or_404(comment.drink_id)

    return render_template('view_comment.html', cocktail=cocktail)

@app.route('/comments', methods=["GET", "POST", "PUT", "PATCH"])
def view_all_comments():
    """Show comments"""
    
    comments = Comment.query.all()

    return render_template('view_all_comments.html', comments=comments)

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show user profile"""

    if not g.user:
        flash("Access unauthorized!", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    comments = (Comment.query.filter(Comment.user_id == user_id))

    return render_template('show_user.html', user = user, comments = comments)



@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404