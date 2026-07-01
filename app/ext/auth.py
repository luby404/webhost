from flask_login import LoginManager
from app.models import Usuario

auth = LoginManager()

auth.login_view = "route.login"

@auth.user_loader
def _load_user(id:int):
    return Usuario.get_or_none(Usuario.id == id)

def init_auth(app):
    auth.init_app(app)
    return auth
