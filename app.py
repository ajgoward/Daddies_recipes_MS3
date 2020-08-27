import os
import bcrypt
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        users = mongo.db.users
        exsiting_user = users.find_one({'name': request.form['username']})

        if exsiting_user is None:
            hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert(
                {'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('login_page'))

        flash('That username already exists!')

    return render_template('homepages/signup.html')


@app.route('/profile' )
def profile():
    return render_template("homepages/profile.html")

# recipe pages with function to find the recipes #


@app.route('/breakfast')
def breakfast():
    return render_template(
        "recipes/breakfast.html", recipes=mongo.db.recipes.find({"type":"breakfast"}))


@app.route('/lunch')
def lunch():
    return render_template("recipes/lunch.html", recipes=mongo.db.recipes.find({"type":"lunch"}))


@app.route('/dinner')
def dinner():
    return render_template("recipes/dinner.html", recipes=mongo.db.recipes.find({"type":"dinner"}))


@app.route('/dessert')
def dessert():
    return render_template("recipes/dessert.html", recipes=mongo.db.recipes.find({"type":"dessert"}))


# CRUD functionality for the Breakfast collection #


@app.route('/add_recipe')
def add_recipe():
    return render_template("recipes/addrecipe.html")


@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('breakfast'))


@app.route('/edit_breakfast/<breakfast_id>')
def edit_breakfast(breakfast_id):
    the_breakfast = mongo.db.breakfasts.find_one({
        "_id": ObjectId(breakfast_id)})
    return render_template('editrecipe/editbreakfast.html', breakfast=the_breakfast)


@app.route('/update_breakfast/<breakfast_id>', methods=["POST"])
def update_breakfast(breakfast_id):
    breakfasts = mongo.db.breakfasts
    breakfasts.update({'_id': ObjectId(breakfast_id)},
    {
        'image': request.form.get('image'),
        'recipe_name': request.form.get('recipe_name'),
        'time_to_make': request.form.get('time_to_make'),
        'ingredients': request.form.get('ingredients'),
        'method': request.form.get('method')
    })
    return redirect(url_for('breakfast'))


@app.route('/delete_breakfast/<breakfast_id>')
def delete_breakfast(breakfast_id):
    mongo.db.breakfasts.remove({'_id': ObjectId(breakfast_id)})
    return redirect(url_for('breakfast'))


# CRUD functionality for the Lunch collection #





@app.route('/edit_lun/<lun_id>')
def edit_lun(lun_id):
    the_lunch = mongo.db.lunch.find_one({"_id": ObjectId(lun_id)})
    return render_template('editrecipe/editlunch.html', lun=the_lunch)


@app.route('/update_lun/<lun_id>', methods=["POST"])
def update_lun(lun_id):
    lun = mongo.db.lunch
    lun.update({'_id': ObjectId(lun_id)},
    {
        'image': request.form.get('image'),
        'recipe_name': request.form.get('recipe_name'),
        'time_to_make': request.form.get('time_to_make'),
        'ingredients': request.form.get('ingredients'),
        'method': request.form.get('method')
    })
    return redirect(url_for('lunch'))


@app.route('/delete_lun/<lun_id>')
def delete_lun(lun_id):
    mongo.db.lunch.remove({'_id': ObjectId(lun_id)})
    return redirect(url_for('lunch'))


# CRUD functionality for the Dinner collection #





@app.route('/edit_dinners/<dinners_id>')
def edit_dinners(dinners_id):
    the_dinner = mongo.db.dinner.find_one({"_id": ObjectId(dinners_id)})
    return render_template('editrecipe/editdinner.html', dinners=the_dinner)


@app.route('/update_dinners/<dinners_id>', methods=["POST"])
def update_dinners(dinners_id):
    dinner = mongo.db.dinner
    dinner.update({'_id': ObjectId(dinners_id)},
    {
        'image': request.form.get('image'),
        'recipe_name': request.form.get('recipe_name'),
        'time_to_make': request.form.get('time_to_make'),
        'ingredients': request.form.get('ingredients'),
        'method': request.form.get('method')
    })
    return redirect(url_for('dinner'))


@app.route('/delete_dinners/<dinners_id>')
def delete_dinners(dinners_id):
    mongo.db.dinner.remove({'_id': ObjectId(dinners_id)})
    return redirect(url_for('dinner'))


# CRUD functionality for the Desserts collection #




@app.route('/edit_dessert/<dessert_id>')
def edit_dessert(dessert_id):
    the_desserts = mongo.db.desserts.find_one({"_id": ObjectId(dessert_id)})
    return render_template('editrecipe/editdessert.html', dessert=the_desserts)


@app.route('/update_dessert/<dessert_id>', methods=["POST"])
def update_dessert(dessert_id):
    desserts = mongo.db.desserts
    desserts.update({'_id': ObjectId(dessert_id)},
    {
        'image': request.form.get('image'),
        'recipe_name': request.form.get('recipe_name'),
        'time_to_make': request.form.get('time_to_make'),
        'ingredients': request.form.get('ingredients'),
        'method': request.form.get('method')
    })
    return redirect(url_for('dessert'))


@app.route('/delete_dessert/<dessert_id>')
def delete_dessert(dessert_id):
    mongo.db.desserts.remove({'_id': ObjectId(dessert_id)})
    return redirect(url_for('dessert'))


# product page #


@app.route('/products')
def products():
    return render_template("products.html")


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
