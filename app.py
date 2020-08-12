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
@app.route('/login_page')
def login_page():
    return render_template("index.html")


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(
            request.form['password'].encode(
                'utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('home'))

    flash('invalid login details')
    return render_template('index.html')


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

    return render_template('signup.html')


# recipe pages with function to find the recipes #


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/breakfast')
def breakfast():
    return render_template(
        "breakfast.html", breakfasts=mongo.db.breakfasts.find())


@app.route('/lunch')
def lunch():
    return render_template("lunch.html", lunch=mongo.db.lunch.find())


@app.route('/dinner')
def dinner():
    return render_template("dinner.html", dinner=mongo.db.dinner.find())


@app.route('/dessert')
def dessert():
    return render_template("dessert.html", desserts=mongo.db.desserts.find())


# CRUD functionality for the Breakfast collection #


@app.route('/add_breakfast')
def add_breakfast():
    return render_template("addbreakfast.html")


@app.route('/insert_breakfast', methods=["POST"])
def insert_breakfast():
    breakfasts = mongo.db.breakfasts
    breakfasts.insert_one(request.form.to_dict())
    return redirect(url_for('breakfast'))


@app.route('/edit_breakfast/<breakfast_id>')
def edit_breakfast(breakfast_id):
    the_breakfast = mongo.db.breakfasts.find_one({
        "_id": ObjectId(breakfast_id)})
    return render_template('editbreakfast.html', breakfast=the_breakfast)


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


@app.route('/add_lunch')
def add_lunch():
    return render_template("addlunch.html")


@app.route('/insert_lunch', methods=["POST"])
def insert_lunch():
    lunch = mongo.db.lunch
    lunch.insert_one(request.form.to_dict())
    return redirect(url_for('lunch'))


@app.route('/edit_lun/<lun_id>')
def edit_lun(lun_id):
    the_lunch = mongo.db.lunch.find_one({"_id": ObjectId(lun_id)})
    return render_template('editlunch.html', lun=the_lunch)


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


@app.route('/add_dinner')
def add_dinner():
    return render_template("adddinner.html")


@app.route('/insert_dinner', methods=["POST"])
def insert_dinner():
    dinner = mongo.db.dinner
    dinner.insert_one(request.form.to_dict())
    return redirect(url_for('dinner'))


@app.route('/edit_dinners/<dinners_id>')
def edit_dinners(dinners_id):
    the_dinner = mongo.db.dinner.find_one({"_id": ObjectId(dinners_id)})
    return render_template('editdinner.html', dinners=the_dinner)


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


#

if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
