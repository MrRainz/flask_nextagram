from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_user, logout_user
from models.user import *
from app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from instagram_web.util.google_oauth import oauth

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/new', methods=["GET"])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route('/', methods=["POST"])
def create():
    username_or_email = request.form['username/email']
    input_password = request.form['password']
    if not username_or_email or not input_password:
        flash("Input field cannot be null.", "danger")
        return redirect(url_for('sessions.new'))
    else:
        if "@" in username_or_email:
            user = User.get_or_none(User.email == username_or_email)
        else:
            user = User.get_or_none(User.username == username_or_email)

    if user:
        if check_password_hash(user.hash_password, input_password):
            login_user(user)
            flash("Logged in!", "success")
            return redirect(url_for('home'))
        else:
            flash("Incorrect password", "danger")
            return redirect(url_for('sessions.new'))
    else:
        flash("Invalid username/email", "danger")
        return redirect(url_for('sessions.new'))


@sessions_blueprint.route('/log_out', methods=["POST"])
def logout():
    logout_user()
    flash("Logged out!", "success")
    return redirect(url_for('home'))


@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route("/authorize/google")
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        flash("Successfully logged in!", "success")
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))