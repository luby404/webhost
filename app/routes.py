from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)
from datetime import datetime, timedelta
from flask_login import login_user, current_user, logout_user, login_required

from app.models import Usuario, Evento

route = Blueprint("route", __name__)


@route.get("/")
def index():
    return render_template("index.html")

@route.get("/dashboard")
@route.get("/dashboard/<id>")
@login_required
def dashboard(id:str=""):
    """ Retorna a pagina com a lista dos webhook ou a pagina com os detalhes do webhooks """

    return render_template("dashboard.html")



@route.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":

        email = request.form.get("email", "").strip()
        if email != "":

            user:Usuario = Usuario.get_or_none(Usuario.email == email)
            if user:
                login(user)
                flash("Usuario Logado com sucesso")
                return redirect(url_for("route.dashboard"))
            else:
                return render_template("confirm.html", email=email)
        else:
            flash("Requisição invalida.")
    
    return render_template("auth.html")

@route.post("/create_account")
def create_account():
    email = request.form.get("email", "").strip()
    try:
        user:Usuario = Usuario.create(email=email)
        login_user(user)
        return redirect(url_for("route.dashboard"))
    except:
        flash("o email ja existe")
        return redirect(url_for("route.login"))


@route.get("/logout")
@login_required
def logout():

    return redirect(url_for("route.login"))


@route.route("/webhook/<id>/event", methods=["GET", "POST", "PUT", "DELET"])
def webhook():

    return {"message", "webhook recebido com sucesso"}
