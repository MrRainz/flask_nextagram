from flask import Blueprint, render_template, flash, redirect, request, url_for

from models.user import *

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/sign_up', methods=['GET'])
def sign_up():
    return render_template('users/sign_up.html')


@users_blueprint.route('/sign_up', methods=['POST'])
def create():
    username = request.form['username']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    user = User(username=username, name=name, email=email, password=password, confirm_password=confirm_password)
    if user.save():
        flash("Registration successful!")
        return redirect(url_for('home'))
    else:
        flash(user.errors)
        return redirect(url_for('users.sign_up'))


@users_blueprint.route('/sign_in', methods=["GET"])
def sign_in():
    return render_template('users/sign_in.html')


@users_blueprint.route('/sign_in', methods=["POST"])
def login():
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
