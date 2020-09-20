import os
from flask import (
    Flask, render_template, redirect, request, url_for, session, flash)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# I received the login and register functionality
# from the code institute tutor support called "Tim"


@app.route('/')
@app.route('/home')
def home():
    """Renders home page"""
    return render_template("homepages/home.html")


@app.route('/login', methods=['POST', "GET"])
def login():
    if request.method == 'POST':
        """check if username exsits in the database"""
        existing_user = mongo.db.users.find_one(
            {'username': request.form.get('username').lower()})

        """check if the password matches using check_hashword_pass"""

        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    return redirect(url_for('profile'))

                    """invalid login details"""

            else:
                flash("Incorrect login details")
        else:
            flash("Incorrect login details")
            return redirect(url_for("login"))

    return render_template('homepages/login.html')


@app.route('/register', methods=['POST', "GET"])
def register():
    if request.method == 'POST':
        """check if username exsits in the database"""
        exsiting_user = mongo.db.users.find_one(
            {'username': request.form.get('username').lower()})

        if exsiting_user:

            """if username exsits display message"""

            flash('That username already exists!')
            return redirect(url_for('register'))
        """
        if username doesnt exsit create dictionary
        and store the information within
        """
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        return redirect(url_for(
            'profile'))
    return render_template('homepages/signup.html')


@app.route('/log_out')
def log_out():
    """remove session cookies"""
    flash("log out successful")
    session.pop("user")
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
        """Renders Profile page and finds all recipes"""
        return render_template(
            "homepages/profile.html", recipes=mongo.db.recipes.find())


# recipe pages with function to find the recipes


@app.route('/breakfast')
def breakfast():
    """Renders breakfast recipe page and finds all breakfast"""
    return render_template(
        "recipes/breakfast.html", recipes=mongo.db.recipes.find(
            {"type": "breakfast"}))


@app.route('/lunch')
def lunch():
    """Renders lunch recipe page and finds all lunch"""
    return render_template("recipes/lunch.html", recipes=mongo.db.recipes.find(
        {"type": "lunch"}))


@app.route('/dinner')
def dinner():
    """Renders dinner recipe page and finds all dinner"""
    return render_template(
        "recipes/dinner.html", recipes=mongo.db.recipes.find(
            {"type": "dinner"}))


@app.route('/dessert')
def dessert():
    """Renders dessert recipe page and finds all desserts"""
    return render_template(
        "recipes/dessert.html", recipes=mongo.db.recipes.find(
            {"type": "dessert"}))


# CRUD functionality for the Breakfast collection #


@app.route('/add_recipe')
def add_recipe():
    """Renders the add recipe page"""
    return render_template("recipes/addrecipe.html")


@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
        """Create the recipe in the database."""
        recipe = {
            "type": request.form.get("type"),
            "image": request.form.get("image"),
            "recipe_name": request.form.get("recipe_name"),
            "time_to_make": request.form.get("time_to_make"),
            "ingredients": request.form.get("ingredients"),
            "method": request.form.get("method"),
            "posted_by": session["user"],
            "credit": request.form.get("credit")
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Added , Thank you!")
        return redirect(url_for('profile'))


@app.route('/edit_recipe/<recipe_id>', methods=["GET", "POST"])
def edit_recipe(recipe_id):
    """request the information of the recipe from the database
     and display it for editing and then updating the database"""
    if request.method == "POST":
        recipe = {
            "type": request.form.get("type"),
            "image": request.form.get("image"),
            "recipe_name": request.form.get("recipe_name"),
            "time_to_make": request.form.get("time_to_make"),
            "ingredients": request.form.get("ingredients"),
            "method": request.form.get("method"),
            "posted_by": session["user"],
            "credit": request.form.get("credit")
        }
        mongo.db.recipes.update({'_id': ObjectId(recipe_id)}, recipe)
        flash("Recipe Edited , Thank you!")
        return redirect(url_for('profile'))
    the_recipe = mongo.db.recipes.find_one({
        "_id": ObjectId(recipe_id)})
    return render_template('recipes/editrecipe.html', recipe=the_recipe)


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
        """Remove the recipe from the database"""
        mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
        return redirect(url_for('profile'))


@app.route('/search',  methods=['GET', 'POST'])
def search():
    """search the database using the query key i have set see readme.md"""
    query = request.form.get("query")
    recipes = mongo.db.recipes.find({"$text": {"$search": query}})
    return render_template(
            "recipes/searchpage.html", recipes=recipes)


# 404 event handler i recieved this from the flask documentation


@app.errorhandler(404)
def page_not_found(e):
    """if the page is not found show this page"""
    return render_template('homepages/404.html'), 404


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
