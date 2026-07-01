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
import secrets, json

route = Blueprint("route", __name__)

current_user:Usuario

@route.get("/")
def index():
    return render_template("index.html")

@route.get("/dashboard")
@route.get("/dashboard/<id>")
@login_required
def dashboard(id:str=""):

    evento:Evento = Evento.get_or_none(Evento.pub_id == id)

    class dados:
        event_id        = evento.pub_id if evento else None
        eventos_names   = [i for i in Evento.select().where(Evento.usuario == current_user)]
        eventos_names.reverse()
        evento_detalhes = json.loads(evento.data) if evento else {}

        url_evento      = str(request.host_url + url_for("route.webhook", id=current_user.pub_id)).replace("//", "/")

    return render_template("dashboard.html", dados=dados)



@route.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":

        email = request.form.get("email", "").strip()
        if email != "":

            user:Usuario = Usuario.get_or_none(Usuario.email == email)
            if user:
                login_user(user)
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
    logout_user()
    return redirect(url_for("route.login"))


@route.route("/webhook/<id>/event", methods=["GET", "POST", "PUT", "DELET"])
def webhook(id):

    user:Usuario = Usuario.get_or_none(Usuario.pub_id == id)
    if user:
        nome  = request.headers.get("Host", secrets.token_urlsafe(16)) + f" {request.method}"
        event = request.json if request.is_json else {}
        
        try:
            data = dict(
                headers={k:v for k,v in request.headers.items()},
                body=json.loads(json.dumps(event)),
            )
            event:Evento = Evento.create(
                usuario=user,
                nome=nome,
                data=json.dumps(data)
            )
            print("Novo Evento gerado")
        except Exception as e:
            print("Ouve um Erro", e)
            return {"message":"Erro ao processar webhook"}, 500
        
    return {"message":"webhook recebido com sucesso"}, 200
