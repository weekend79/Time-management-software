import os
import bcrypt
from flask import Flask, render_template, url_for, redirect, request, session
from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env

# Connection configuration
app = Flask(__name__)

# MongoDB config
app.config['MONGO_DBNAME'] = 'timeManagement'
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


mongo = PyMongo(app)

# Setting up the app route
@app.route('/')
def get_index():
    return render_template("index.html")

@app.route('/login')
def login():
    if 'username' in session:
        return redirect(url_for('admin_dashboard'))

    return render_template("login.html")

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        new_user = mongo.db.new_user
        existing_user = new_user.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            new_user.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('login'))
        
        return 'The username already exists!'

    return render_template('register.html')

@app.route('/add_user')
def add_user():
    return render_template("add_user.html")

if __name__ == '__main__':
    app.secret_key = os.getenv('SECRET_KEY')
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)


