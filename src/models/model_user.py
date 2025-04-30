from .entities.User import User

class Model_User():
    
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_usuario, nombre, correo, contrasena_hash FROM usuario WHERE nombre = %s"
            cursor.execute(sql, (user.nombre,))

            row = cursor.fetchone()
            print('Row:', row)
            cursor.close()

            if row is not None and User.check_password(row[3], user.contrasena):
                return User(row[0], row[1], row[2], None)
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_user_by_id(self, db, user_id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_usuario, nombre, correo FROM usuario WHERE id_usuario = %s"
            cursor.execute(sql, (user_id,))

            row = cursor.fetchone()
            print('Row:', row)
            cursor.close()

            if row is not None:
                return User(row[0], row[1], row[2], None)
            else:
                return None
        except Exception as ex:
            raise Exception(ex)