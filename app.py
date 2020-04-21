"""
Imports from Os, Flask, BSON and PyMongo,  

"""
import os
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Import env file
if os.path.exists("env.py"):
    import env

# Connection configuration
app = Flask(__name__)

# MongoDB config
app.config['MONGO_DBNAME'] = 'time_manager'
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# PyMongo connection
mongo = PyMongo(app)


# Setting up the app route for Index
@app.route('/')
def index():
    return render_template("index.html")


# Setting up the app route for Time Manager static site
@app.route('/timer')
def timer():
    return render_template('timer.html')


# Setting up the app route for the FAQ page
@app.route('/faq')
def faq():
    return render_template('faq.html')


# Setting up the app route for contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Setting up the app route for admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template("admin_dashboard.html")


# Setting up the app route for View Employees
@app.route('/view_employees')
def view_employees():
    return render_template("view_employees.html", employees=mongo.db.employees.find())


# Setting up the app route for finding one employees profile
@app.route('/profile/<employee_id>')
def profile(employee_id):
    the_employee = mongo.db.employees.find_one({"_id": ObjectId(employee_id)})
    employees = mongo.db.employees.find()
    return render_template("profile.html", employee=the_employee, employees=mongo.db.employees.find_one())


# App route to add a new employee
@app.route('/add_user')
def add_user():
    return render_template("add_user.html")


# App route for inserting a user in the database
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

# App route for editing a employee
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


# App route for updating the database from the edit employee form
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


# App route for deleting a employee from the database
@app.route('/delete_employee/<employee_id>')
def delete_employee(employee_id):
    mongo.db.employees.remove({'_id': ObjectId(employee_id)})
    flash('Employee deleted!')
    return redirect(url_for('view_employees'))


# App route to see a list of all projects
@app.route('/projects')
def projects():
    return render_template("projects.html", projects=mongo.db.projects.find())


# App route to find a project and to display the project data
@app.route('/see_project/<project_id>')
def see_project(project_id):
    the_project = mongo.db.projects.find_one({"_id": ObjectId(project_id)})
    projects = mongo.db.projects.find()
    return render_template("see_project.html", project=the_project, projects=mongo.db.projects.find_one())


# App route for adding a new project to the database
@app.route('/new_project')
def new_project():
    return render_template("new_project.html")


# App route for inserting a new project to the database
@app.route('/insert_project', methods=['POST'])
def insert_project():
    projects = mongo.db.projects
    projects.insert_one(request.form.to_dict())
    flash('New project added')
    return redirect(url_for('projects'))


# App route for editing a project
@app.route('/edit_project/<project_id>')
def edit_project(project_id):
    the_project = mongo.db.projects.find_one({"_id": ObjectId(project_id)})
    projects = mongo.db.projects.find()
    return render_template('edit_project.html', project=the_project, projects=mongo.db.projects.find_one())


# App route for updating the project data in the database
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


# App route for deleting a project
@app.route('/delete_project/<project_id>')
def delete_project(project_id):
    mongo.db.projects.remove({'_id': ObjectId(project_id)})
    flash('Project deleted!')
    return redirect(url_for('projects'))


# App route to open the Time manager
@app.route('/time_manager')
def time_manager():
    return render_template('time_manager.html', projects=mongo.db.projects.find())


# App route for inserting a timestamp in the database
@app.route('/timestamp', methods=['POST'])
def timestamp():
    timestamp = mongo.db.timestamps
    timestamp.insert_one(request.form.to_dict())
    flash('New Time Record Added')
    return redirect(url_for('admin_dashboard'))


# App route to timestamp history
@app.route('/history')
def history():
    return render_template("history.html", timestamps=mongo.db.timestamps.find())


# App route to see the project data
@app.route('/project_profile')
def project_profile():
    return render_template('project_profile.html', timestamps=mongo.db.timestamps.find_one())


# App run
if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)
