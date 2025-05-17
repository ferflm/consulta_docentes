from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user
from ..models.model_user import Model_User
from ..models.entities.User import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        temp_user = User(None,
                        request.form['username'],
                        None,
                        request.form['password'],
                        None,  # rol
                        True)  # activo placeholder
        logged_user = Model_User.login(current_app.mysql, temp_user)

        if not logged_user:
            flash('Credenciales inválidas.', 'danger')
        elif not logged_user.activo:
            flash('Cuenta deshabilitada. Contacta al administrador.', 'warning')
        else:
            login_user(logged_user)
            return redirect(url_for('profesor.profesores'))

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
