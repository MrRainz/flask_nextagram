from app import app
from flask import render_template
from flask_login import current_user
from models.user import *
from app import login_manager
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.follows.views import follows_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from instagram_web.util.google_oauth import oauth

assets = Environment(app)
assets.register(bundles)
oauth.init_app(app)
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(follows_blueprint, url_prefix="/follows")

@app.errorhandler(500)
def error_500(e):
    return render_template('500.html'), 500

@app.errorhandler(401)
def error_401(e):
    return render_template('401.html'), 401

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def error_403(e):
    return render_template('403.html'), 403

@app.errorhandler(400)
def error_400(e):
    return render_template('400.html'), 400


@app.route("/")
def home():
    if current_user.is_authenticated:
        user = User.get_or_none(User.id == current_user.id)
        followings = user.get_followings()        
    else:
        followings = []
    return render_template('home.html', followings=followings)
