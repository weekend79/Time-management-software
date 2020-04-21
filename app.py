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


@app.route('/timer')
def timer():
    return render_template('timer.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


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
    """
    1. Add generic and frequently used functions to utils.py

    if is_user_logged_in(request):
        employees = mongo.db.employees
        employees.insert_one(request.form.to_dict())
        flash('New employee added')
        return redirect(url_for('admin_dashboard'))
    else:
        flash(...)
        ....
    """
    employees = mongo.db.employees
    employees.insert_one(request.form.to_dict())
    flash('New employee added')
    return redirect(url_for('admin_dashboard'))


@app.route('/edit_employee/<employee_id>')
def edit_employee(employee_id):
    """
    2. Exception Handling

    try:
        the_employee = mongo.db.employees.find_one({"_id": ObjectId(employee_id)})
    except bson.errors.InvalidId:
        flash('Employee doesn\'t exist')
        ...

    flash('Employee updated')
    return render_template('edit_employee.html', employee=the_employee)
    """
    the_employee = mongo.db.employees.find_one({"_id": ObjectId(employee_id)})
    flash('Employee updated')
    return render_template('edit_employee.html', employee=the_employee)
#     employees.insert_one(request.form.to_dict())


@app.route('/update_employee/<employee_id>', methods=["POST"])
def update_employee(employee_id):
    """
    3. Improve forms by defining in the backend, presenting to the template, and validating on submit.
    """
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


@app.route('/projects')
def projects():
    return render_template("projects.html", projects=mongo.db.projects.find())


@app.route('/see_project/<project_id>')
def see_project(project_id):
    the_project = mongo.db.projects.find_one({"_id": ObjectId(project_id)})
    projects = mongo.db.projects.find()
    return render_template("see_project.html", project=the_project, projects=mongo.db.projects.find_one())


@app.route('/new_project')
def new_project():
    return render_template("new_project.html")


@app.route('/insert_project', methods=['POST'])
def insert_project():
    projects = mongo.db.projects
    projects.insert_one(request.form.to_dict())
    flash('New project added')
    return redirect(url_for('projects'))


@app.route('/edit_project/<project_id>')
def edit_project(project_id):
    the_project = mongo.db.projects.find_one({"_id": ObjectId(project_id)})
    projects = mongo.db.projects.find()
    return render_template('edit_project.html', project=the_project, projects=mongo.db.projects.find_one())


@app.route('/update_project/<project_id>', methods=["POST"])
def update_project(project_id):
    projects = mongo.db.projects
    projects.replace_one( {'_id': ObjectId(project_id)},
    {
        'project_id' : request.form.get('project_id'),
        'project_name' : request.form.get('project_name'),
        'project_manager' : request.form.get('project_manager')
    })
    return redirect(url_for('projects'))


@app.route('/delete_project/<project_id>')
def delete_project(project_id):
    mongo.db.projects.remove({'_id': ObjectId(project_id)})
    flash('Project deleted!')
    return redirect(url_for('projects'))


@app.route('/time_manager')
def time_manager():
    return render_template('time_manager.html', projects=mongo.db.projects.find())


@app.route('/timestamp', methods=['POST'])
def timestamp():
    timestamp = mongo.db.timestamps
    timestamp.insert_one(request.form.to_dict())
    flash('New Time Record Added')
    return redirect(url_for('admin_dashboard'))


@app.route('/history')
def history():
    return render_template("history.html", timestamps=mongo.db.timestamps.find())


@app.route('/project_profile')
def project_profile():
    return render_template('project_profile.html', timestamps=mongo.db.timestamps.find_one())


if __name__ == '__main__':
    app.secret_key = os.getenv('SECRET_KEY')
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)
