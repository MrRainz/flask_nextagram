from flask import Blueprint, render_template, flash, redirect, request, url_for
from werkzeug.security import generate_password_hash
import re
from models.user import *

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/sign_up', methods=['GET'])
def sign_up():
    return render_template('users/sign_up.html')


@users_blueprint.route('/create', methods=['POST'])
def create():
    valid_count = 0
    username = request.form['username']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if len(username) > 5 and len(username) < 21:
        valid_count += 1
    else:
        flash("Username must be 6-20 characters")
    if len(name) > 0 and len(name) < 51:
        valid_count += 1
    else:
        flash("Display name must be 1-50 characters")
    email_length = email.split("@")
    if len(email_length[0]) > 3 and len(email_length[0]) < 20:
        valid_count += 1
    else:
        flash("Email length needs to be 3-20 characters long")
    if re.search('[^a-zA-Z0-9]', password) and len(password) > 7 and len(password) < 20:
        valid_count += 1
    else:
        flash("Password needs to be 8-20 characters long and contains at least 1 special character.")
    if confirm_password == password:
        valid_count += 1
    else:
        flash("Passwords do not match.")
    if valid_count == 5:
        hash_password = generate_password_hash(password)
        user = User(username=username, name=name, email=email, password=hash_password)
        integrity_count = 0
        if not User.get_or_none(User.username==username):
            integrity_count += 1
        else:
            flash("Username taken!")
        if not User.get_or_none(User.email==email):
            integrity_count += 1
        else:
            flash("Email taken!")
        if integrity_count == 2:
            if user.save():
                flash("Registration successful!")
            else:
                flash("Registration failed.")
    return redirect(url_for('users.sign_up'))


@users_blueprint.route('/sign_in', methods["GET"])
def sign_in():
    pass


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return render_template('users/user_list.html')


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass

@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
