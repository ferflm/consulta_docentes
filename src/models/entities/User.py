from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, nombre, correo, contrasena):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena

    @classmethod
    def check_password(self, contrasena_hash, contrasena):
        return check_password_hash(contrasena_hash, contrasena)
    