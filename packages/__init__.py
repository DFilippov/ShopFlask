from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from packages.config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
# TODO: remove
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from packages import routes
from packages.models.category import Category
from packages.models.item import Item
from packages.models.quantity_history import QuantityHistory
from packages.models.user import User


