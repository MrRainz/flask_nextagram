import os
from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_user, logout_user
from models.user import *
from app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from instagram_web.util.google_oauth import oauth

follows_blueprint = Blueprint('follows',
                            __name__,
                            template_folder='templates')


@follows_blueprint.route('/<user_id>', methods=["GET"])
def new(user_id):
    return render_template('follows/new.html')