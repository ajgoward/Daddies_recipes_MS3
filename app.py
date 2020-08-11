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


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
