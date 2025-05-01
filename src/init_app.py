from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect

# Models
from .models.model_user import Model_User
from .models.entities.User import User
from .models.model_profesor import Model_Profesor
from .models.model_categoria import Model_Categoria
from .models.model_grado import Model_Grado

# Entities
from .models.entities.Profesor import Profesor

mysql = MySQL()
login_manager_app = LoginManager()

def init_app(config_class):
    app = Flask(__name__)
    csrf = CSRFProtect(app)
    csrf.init_app(app)
    app.config.from_object(config_class)

    mysql.init_app(app)
    login_manager_app.init_app(app)

    @login_manager_app.user_loader
    def load_user(user_id):
        return Model_User.get_user_by_id(mysql, user_id)

    @app.route('/')
    def index():
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            temp_user = User(None, request.form['username'], None, request.form['password'])
            logged_user = Model_User.login(mysql, temp_user)

            if logged_user:
                login_user(logged_user)
                return redirect(url_for('profesores'))
            else:
                print('Credenciales inválidas...')
                flash('Credenciales inválidas...')
        return render_template('auth/login.html')
    
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))
    
    @app.route('/profesores')
    @login_required
    def profesores():
        lista = Model_Profesor.get_profesores(mysql)
        return render_template('profesores.html', profesores = lista)
    
    @app.route('/profesores/delete/<int:id_profesor>', methods=['POST'])
    @login_required
    def delete_profesor(id_profesor):
        try:
            Model_Profesor.delete_by_id(mysql, id_profesor)
            flash('Profesor eliminado correctamente', 'success')
        except Exception as ex:
            flash(f'Error al eliminar el profesor: {str(ex)}', 'danger')
        profesores = Model_Profesor.get_profesores(mysql)
        return render_template('profesores.html', profesores = profesores)
    
    @app.route('/profesores/editar/<int:id_profesor>', methods=['GET', 'POST'])
    @login_required
    def edit_profesor(id_profesor):
        if request.method == 'POST':
            datos = request.form
            profesor = Profesor(
                id_profesor=id_profesor,
                nombre=datos['nombre'],
                a_paterno=datos['a_paterno'],
                a_materno=datos['a_materno'],
                genero=datos['genero'],
                num_trabajador=datos['num_trabajador'],
                rfc=datos['rfc'],
                curp=datos['curp'],
                ingreso_unam=datos['ingreso_unam'],
                ingreso_carrera=datos['ingreso_carrera'],
                correo=datos['correo'],
                num_cel=datos['num_cel'],
                num_tel=datos['num_tel'],
                direccion=datos['direccion']
            )
            profesor.id_categoria = int(datos['id_categoria'])
            profesor.id_grado = int(datos['id_grado'])

            try:
                Model_Profesor.update_profesor(mysql, profesor)
                flash('Profesor actualizado correctamente.', 'success')
                return redirect(url_for('profesores'))
            except Exception as e:
                flash(f'Error al actualizar: {e}', 'danger')

        profesor = Model_Profesor.get_profesor_by_id(mysql, id_profesor)
        categorias = Model_Categoria.get_categorias(mysql)
        grados = Model_Grado.get_grados(mysql)
        return render_template('editar_profesor.html', profesor=profesor, categorias=categorias, grados=grados)
    
    @app.route('/profesores/agregar', methods=['GET', 'POST'])
    @login_required
    def add_profesor():
        if request.method == 'POST':
            datos = request.form
            profesor = Profesor(
                id_profesor=None,
                nombre=datos['nombre'],
                a_paterno=datos['a_paterno'],
                a_materno=datos['a_materno'],
                genero=datos['genero'],
                num_trabajador=datos['num_trabajador'],
                rfc=datos['rfc'],
                curp=datos['curp'],
                ingreso_unam=datos['ingreso_unam'],
                ingreso_carrera=datos['ingreso_carrera'],
                correo=datos['correo'],
                num_cel=datos['num_cel'],
                num_tel=datos['num_tel'],
                direccion=datos['direccion']
            )
            profesor.id_categoria = int(datos['id_categoria'])
            profesor.id_grado = int(datos['id_grado'])

            try:
                Model_Profesor.insert_profesor(mysql, profesor)
                flash('Profesor agregado correctamente.', 'success')
                return redirect(url_for('profesores'))
            except Exception as e:
                flash(f'Error al agregar profesor: {e}', 'danger')

        categorias = Model_Categoria.get_categorias(mysql)
        grados = Model_Grado.get_grados(mysql)
        return render_template('nuevo_profesor.html', categorias=categorias, grados=grados)

    def status_401(error):
        return redirect(url_for('login'))
    
    def status_404(error):
        return '<h1>Page not found</h1>'
    

    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)

    return app
