from flask_admin import Admin
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from flask_food.admin import AdminDashboard

admin = Admin(index_view=AdminDashboard())
db = SQLAlchemy()
migrate = Migrate()
toolbar = DebugToolbarExtension()
csrf = CSRFProtect()
login = LoginManager()

login.login_view = "auth.login"
login.login_message = "Авторизуйтесь для доступа."
