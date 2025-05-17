from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, nombre, correo, contrasena, rol, activo=True):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol
        self.activo = activo

    @classmethod
    def check_password(cls, contrasena_hash, contrasena):
        return check_password_hash(contrasena_hash, contrasena)