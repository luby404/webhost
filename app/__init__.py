from flask import Flask

from .models import init_models
from app.ext.auth import init_auth

from app.routes import route

app = Flask(__name__)
app.secret_key = "oewkedas a, sdalsndaçlsda"

init_models()
init_auth(app)

app.register_blueprint(route)
