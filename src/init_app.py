from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect

# Models
from .models.model_user import Model_User
from .models.entities.User import User

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
                return redirect(url_for('home'))
            else:
                print('Credenciales inválidas...')
                flash('Credenciales inválidas...')
        return render_template('auth/login.html')
    
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/home')
    @login_required
    def home():
        return render_template('home.html')
    
    @app.route('/protected')
    @login_required
    def protected():
        return '<h1>Protected</h1>'
    
    def status_401(error):
        return redirect(url_for('login'))
    
    def status_404(error):
        return '<h1>Page not found</h1>'
    

    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)

    return app
