from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models.user import *
from app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash


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


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(User.username == username)
    if user:
        return render_template("users/show.html", user=user)
    else:
        flash("User doesn't exist")
        return redirect(url_for('home'))


@users_blueprint.route('/', methods=["GET"])
def index():
    users = User.select()
    return render_template('users/user_list.html', users=users)


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    if current_user.id != int(id):
        return redirect(url_for('users.edit', id=current_user.id))
    else:
        user = User.get_or_none(User.id == id)
        if user:
            return render_template('users/edit.html', user=user)
        else:
            return redirect(url_for('users.edit', id=current_user.id))

@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    if current_user.id != int(id):
        return redirect(url_for('users.edit', id=current_user.id))
    else:
        user = User.get_by_id(id)
        if request.form['username']:
            user.username = request.form['username']    
            #if user.save(only=[User.username]):
            #    flash("Username editted.")
            #else:
            #    flash(user.errors)
        if request.form['name']:
            user.name = request.form['name']
            #if user.save(only=[User.name]):
            #    flash("Display name editted.")
            #else:
            #    flash(user.errors) 
        if request.form['email']:
            user.email = request.form['email']
            #if user.save(only=[User.email]):
            #    flash("Email editted.")
            #else:
            #    flash(user.errors) 
        if request.form['password'] and request.form['confirm_password']:
            user.password = request.form['password']
            user.confirm_password = request.form['confirm_password']
            #if user.save(only=[User.username]):
            #    flash("Username editted.")
            #else:
            #    flash(user.errors)
        if user.save():
            flash("Successfully editted.")
        else:
            flash(user.errors)
        return redirect(url_for('users.edit', id=current_user.id))
