import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_pagedown import PageDown
from flaskext.markdown import Markdown

login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# app.config['GOOGLE_OAUTH_CLIENT_ID'] = os.environ.get("929432084569-usdl52gktsmqebaov7najvd3mnlrtj6n.apps.googleusercontent.com")
# app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = os.environ.get("JVzcWEcK4qefRnD7POaeP9m5")


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
pagedown = PageDown(app)
Migrate(app, db)
Markdown(app)

login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message = 'Please login to view this page, bro!'
login_manager.login_message_category = "info"

from blog.users.views import users_blueprint
from blog.posts.views import posts_blueprint, comments_blueprint
from blog.google.views import google_bp

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(posts_blueprint, url_prefix='/posts')
app.register_blueprint(google_bp, url_prefix='/login')
app.register_blueprint(comments_blueprint, url_prefix='/comment')

