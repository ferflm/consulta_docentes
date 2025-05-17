from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from ..models.model_user import Model_User

from datetime import datetime
import io
import json
import csv

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/usuarios')
@login_required
def usuarios():
    if current_user.rol != 'admin':
        abort(403)
    lista = Model_User.get_all(current_app.mysql)
    return render_template('usuarios.html', usuarios=lista)

@usuario_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
def add_usuario():
    # Sólo admins pueden crear usuarios
    if current_user.rol != 'admin':
        abort(403)

    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        correo = request.form['correo'].strip()
        contrasena = request.form['contrasena']
        rol = request.form['rol']

        # Validar campos
        if rol not in ['usuario', 'admin']:
            flash('El rol seleccionado no es válido.', 'danger')
            return redirect(url_for('usuario.add_usuario'))

        # Hash de la contraseña
        hash_pw = generate_password_hash(contrasena)

        try:
            Model_User.create_user(current_app.mysql, nombre, correo, hash_pw, rol)
            flash('Usuario creado correctamente.', 'success')
            return redirect(url_for('usuario.usuarios'))
        except Exception as e:
            flash(f'Error al crear usuario: {e}', 'danger')
            return redirect(url_for('usuario.add_usuario'))

    # GET → mostrar el formulario
    return render_template('nuevo_usuario.html')

@usuario_bp.route('/usuarios/editar/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
def edit_usuario(id_usuario):
    if current_user.rol != 'admin':
        abort(403)
    # GET: mostrar formulario con datos
    if request.method == 'GET':
        u = Model_User.get_user_by_id(current_app.mysql, id_usuario)
        if not u:
            abort(404)
        return render_template('editar_usuario.html', usuario=u)
    # POST: guardar cambios
    nombre = request.form['nombre'].strip()
    correo = request.form['correo'].strip()
    rol = request.form['rol']
    if rol not in ['usuario', 'admin']:
        flash('Rol inválido.', 'danger')
        return redirect(url_for('usuario.editar_usuario', id_usuario=id_usuario))
    try:
        Model_User.update_user(current_app.mysql, id_usuario, nombre, correo, rol)
        flash('Usuario actualizado correctamente.', 'success')
    except Exception as e:
        flash(f'Error al actualizar usuario: {e}', 'danger')
    return redirect(url_for('usuario.usuarios'))

# Toggle activo/desactivo
@usuario_bp.route('/usuarios/toggle/<int:id_usuario>', methods=['POST'])
@login_required
def toggle_usuario(id_usuario):
    if current_user.rol != 'admin':
        abort(403)
    try:
        nuevo_estado = Model_User.toggle_user(current_app.mysql, id_usuario)
        msg = 'Usuario activado.' if nuevo_estado else 'Usuario desactivado.'
        flash(msg, 'success')
    except Exception as e:
        flash(f'Error al cambiar estado: {e}', 'danger')
    return redirect(url_for('usuario.usuarios'))

@usuario_bp.route('/usuarios/delete/<int:id_usuario>', methods=['POST'])
@login_required
def delete_usuario(id_usuario):
    if current_user.rol != 'admin':
        abort(403)
    try:
        Model_User.delete_user(current_app.mysql, id_usuario)
        flash('Usuario eliminado correctamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar usuario: {e}', 'danger')
    return redirect(url_for('usuario.usuarios'))
