from flask import Flask, render_template, request, redirect, url_for, flash, Response, send_file, abort
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash

import io
import csv
import json
from datetime import datetime, date

# Models
from .models.model_user import Model_User
from .models.entities.User import User
from .models.model_profesor import Model_Profesor
from .models.model_categoria import Model_Categoria
from .models.model_grado import Model_Grado

# Entities
from .models.entities.Profesor import Profesor

from .routes.auth_routes import auth_bp
from .routes.profesor_routes import profesor_bp
from .routes.usuario_routes import usuario_bp

mysql = MySQL()
login_manager_app = LoginManager()

def tiempo_transcurrido(fecha):
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
    elif isinstance(fecha, datetime):
        fecha = fecha.date()

    ahora = date.today()
    diferencia = ahora - fecha
    años = diferencia.days // 365
    meses = (diferencia.days % 365) // 30
    dias = (diferencia.days % 365) % 30

    if años > 0:
        return f"{años} año{'s' if años > 1 else ''}"
    elif meses > 0:
        return f"{meses} mes{'es' if meses > 1 else ''}"
    elif dias > 0:
        return f"{dias} día{'s' if dias > 1 else ''}"
    else:
        return "Hoy"

def init_app(config_class):
    app = Flask(__name__)
    csrf = CSRFProtect(app)
    csrf.init_app(app)
    app.config.from_object(config_class)

    mysql.init_app(app)
    app.mysql = mysql 
    login_manager_app.init_app(app)

    app.jinja_env.filters['relativo'] = tiempo_transcurrido

    # Register blueprints
    app.register_blueprint(profesor_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(auth_bp)

    print(app.url_map)

    @app.after_request
    def add_header(response):
        # Deshabilita caché en todas las respuestas
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @login_manager_app.user_loader
    def load_user(user_id):
        return Model_User.get_user_by_id(mysql, user_id)

    return app