from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)
from datetime import datetime, timedelta
from flask_login import login_user, current_user, logout_user

route = Blueprint("route", __name__)


@route.get("/")
def index():
    return render_template("index.html")

@route.get("/dashboard")
@route.get("/dashboard/<id>")
def dashboard(id:str=""):
    """ Retorna a pagina com a lista dos webhook ou a pagina com os detalhes do webhooks """

    return render_template("dashboard.html")



@route.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        flash("Usuario Logado com sucesso")
        return redirect(url_for("route.dashboard"))
    else:
        return render_template("login.html")

@route.route("/webhook/<id>/event", methods=["GET", "POST", "PUT", "DELET"])
def webhook():

    return {"message", "webhook recebido com sucesso"}
