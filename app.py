import os
import config
from flask_wtf.csrf import CSRFProtect
from flask import Flask
from flask_login import LoginManager
from models.base_model import db

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

login_manager = LoginManager()
app = Flask('NEXTAGRAM', root_path=web_dir)
app.secret_key = os.getenv("SECRET_KEY")
csrf = CSRFProtect(app)
login_manager.init_app(app)

#def error_500(e):
#    return render_template('500.html'), 500
#
#app.register_error_handler(500, error_500)
#
#
#def error_404(e):
#    return render_template('404.html'), 404
#
#app.register_error_handler(404, error_404)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
