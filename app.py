import os
import bcrypt
from flask import (
    Flask, render_template, redirect, request, url_for, session, flash)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# home page
# I recievd the login functionality from a youtube
# tutorial you can fiind it here
# https://www.youtube.com/watch?v=vVx1737auSE#


@app.route('/')
@app.route('/home')
def home():
    return render_template("homepages/home.html")


@app.route('/login_page')
def login_page():
    return render_template("homepages/index.html")


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(
            request.form['password'].encode(
                'utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('profile'))

    flash('invalid login details')
    return render_template('homepages/index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        exsiting_user = mongo.db.users.find_one(
            {'username': request.form.get['username'].lower()})

        if exsiting_user:
            flash('That username already exists!')
            return redirect(url_for('register'))
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()

    return render_template('homepages/home.html')


@app.route('/log_out')
def log_out():
    flash("log out successful")
    session.pop("username")
    return redirect(url_for('home'))


@app.route('/profile')
def profile():
    return render_template(
        "homepages/profile.html", recipes=mongo.db.recipes.find())

# recipe pages with function to find the recipes #


@app.route('/breakfast')
def breakfast():
    return render_template(
        "recipes/breakfast.html", recipes=mongo.db.recipes.find(
            {"type": "breakfast"}))


@app.route('/lunch')
def lunch():
    return render_template("recipes/lunch.html", recipes=mongo.db.recipes.find(
        {"type": "lunch"}))


@app.route('/dinner')
def dinner():
    return render_template(
        "recipes/dinner.html", recipes=mongo.db.recipes.find(
            {"type": "dinner"}))


@app.route('/dessert')
def dessert():
    return render_template(
        "recipes/dessert.html", recipes=mongo.db.recipes.find(
            {"type": "dessert"}))


# CRUD functionality for the Breakfast collection #


@app.route('/add_recipe')
def add_recipe():
    return render_template("recipes/addrecipe.html")


@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('profile'))


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({
        "_id": ObjectId(recipe_id)})
    return render_template('recipes/editrecipe.html', recipe=the_recipe)


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipe = mongo.db.recipes
    recipe.update({'_id': ObjectId(recipe_id)}, {
        'type': request.form.get('type'),
        'image': request.form.get('image'),
        'recipe_name': request.form.get('recipe_name'),
        'time_to_make': request.form.get('time_to_make'),
        'ingredients': request.form.get('ingredients'),
        'method': request.form.get('method'),
        'posted_by': request.form.get('posted_by')
    })
    return redirect(url_for('profile'))


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
        mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
        return redirect(url_for('profile'))


@app.route('/products')
def products():
    return render_template("products.html")


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
