import os
import bcrypt
from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env

# if os.path.exists("utils.py"):
 #   import utils

# Connection configuration
app = Flask(__name__)

# MongoDB config
app.config['MONGO_DBNAME'] = 'time_manager'
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

mongo = PyMongo(app)

# Setting up the app route
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login')
def login():
    hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
    user = mongo.db.users.find_one({'name': request.form['username'], 'password': hashpass})

    if user:
        session['username'] = request.form['username']
        return redirect(url_for('admin_dashboard'))

    return render_template("login.html")


@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template("admin_dashboard.html")
#    new_user = mongo.db.new_user
#    login_user = new_user.find_one({'name' : request.form['username']})

    # if login_user:
    #    if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
    #        session['username'] = request.form['username']
    #        return redirect(url_for('login'))
#    return 'Invalid username/password combination'


# users --> usernames and passwords and permissions e.g. is_employee, is_admin and employee = _id
# employees --> [employee_1(_id=...)]


@app.route('/view_employees')
def view_employees():
    return render_template("view_employees.html", employees=mongo.db.employees.find())

    # get the employees from MongoDB
    # employees = [employee_1, ..., employee_n]
    # employees[0]['postal_code']


@app.route('/profile/<employee_id>')
def profile(employee_id):
    the_employee = mongo.db.employees.find_one({"_id": ObjectId(employee_id)})
    employees = mongo.db.employees.find()
    return render_template("profile.html", employee=the_employee, employees=mongo.db.employees.find_one())


@app.route('/add_user')
def add_user():
    return render_template("add_user.html")


@app.route('/insert_user', methods=['POST'])
def insert_user():
    employees = mongo.db.employees
    employees.insert_one(request.form.to_dict())
    flash('New employee added')
    return redirect(url_for('admin_dashboard'))


@app.route('/edit_employee/<employee_id>')
def edit_employee(employee_id):
    the_employee = mongo.db.employees.find_one({"_id": ObjectId(employee_id)})
    employees = mongo.db.employees.find()
    return render_template('edit_employee.html', employee=the_employee, employees=mongo.db.employees.find_one())


@app.route('/update_employee/<employee_id>', methods=["POST"])
def update_employee(employee_id):
    employees = mongo.db.employees
    employees.replace_one( {'_id': ObjectId(employee_id)},
    {
        'name' : request.form.get('name'),
        'dob' : request.form.get('DOB'),
        'address' : request.form.get('address'),
        'postal_code' : request.form.get('postal_code'),
        'postal_address' : request.form.get('postal_address'),
        'phone' : request.form.get('phone'),
        'country_code' : request.form.get('country_code'),
        'email_id' : request.form.get('email_id'),
        'id' : request.form.get('id')
    })
    return redirect(url_for('view_employees'))


@app.route('/delete_employee/<employee_id>')
def delete_employee(employee_id):
    mongo.db.employees.remove({'_id': ObjectId(employee_id)})
    flash('Employee deleted!')
    return redirect(url_for('view_employees'))


if __name__ == '__main__':
    app.secret_key = os.getenv('SECRET_KEY')
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)
