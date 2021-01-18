from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models.user import *
from app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
import boto3, botocore
import os

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ['AWS_KEY'],
    aws_secret_access_key=os.environ['AWS_SECRET']
)


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


@users_blueprint.route('/<id>', methods=["GET"])
def show(id):
    user = User.get_or_none(User.id == id)
    if user:
        return render_template("users/show.html", user=user)
    else:
        flash("User doesn't exist")
        return redirect(url_for('home'))


@users_blueprint.route('/<id>/profile', methods=["GET"])
@login_required
def profile(id):
    user = User.get_or_none(User.id == id)
    if current_user.id != int(id):
        return render_template("users/user_list.html", user=user)
    else:
        if user:
            return render_template('users/show.html', user=user)
        else:
            return render_template("users/user_list.html", user=user)


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

@users_blueprint.route('/<id>/edit', methods=['POST'])
def update(id):
    user = User.get_by_id(id)
    if request.form['username']:
        user.username = request.form['username']    
    if request.form['name']:
        user.name = request.form['name']
    if request.form['email']:
        user.email = request.form['email']
    if request.form['password'] and request.form['confirm_password']:
        user.password = request.form['password']
        user.confirm_password = request.form['confirm_password']
    if user.save():
        flash("Successfully editted.")
    else:
        flash(user.errors)
    return redirect(url_for('users.edit', id=current_user.id))


@users_blueprint.route('/<id>/upload', methods=["GET"])
@login_required
def upload(id):
    if current_user.id != int(id):
        return redirect(url_for('users.upload', id=current_user.id))
    else:
        user = User.get_or_none(User.id == id)
        if user:
            return render_template('users/upload.html', user=user)
        else:
            return redirect(url_for('users.upload', id=current_user.id))
    
    return render_template("users/upload.html")

@users_blueprint.route('/<id>/upload', methods=["POST"])
@login_required
def upload_image(id):
    file = request.files["my_file"]
    try:
        s3.upload_fileobj(
            file,
            os.environ["BUCKET_NAME"],
            "images/" + file.filename,
            ExtraArgs = {
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )
        flash("Successfully uploaded") 
    except:
        flash("Did you select a file?")
    bucket_name = os.environ["BUCKET_NAME"]
    region = os.environ["REGION"]
    platform = os.environ["PLATFORM"]
    url = f"https://{bucket_name}.{region}.{platform}/images/{file.filename}"
    user = User.get_by_id(id)
    user.profile_image_url = url
    if user.save():
        flash("Profile picture changed.")
    else:
        flash("Profile picture not changed.")
    return redirect(url_for("users.profile", id=current_user.id))
