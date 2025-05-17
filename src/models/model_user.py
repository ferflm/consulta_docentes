from .entities.User import User

class Model_User():
    
    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT id_usuario, nombre, correo, contrasena_hash, rol, activo
                FROM usuario
                WHERE nombre = %s
            """
            cursor.execute(sql, (user.nombre,))
            row = cursor.fetchone()
            cursor.close()

            if row and User.check_password(row[3], user.contrasena):
                # row = (id, nombre, correo, hash, rol, activo)
                return User(
                    row[0],  # id
                    row[1],  # nombre
                    row[2],  # correo
                    None,    # no guardamos contraseña en la sesión
                    row[4],  # rol
                    bool(row[5])  # activo
                )
            return None
        except Exception as ex:
            raise Exception(ex)

        
    @classmethod
    def get_user_by_id(cls, db, user_id):
        cursor = db.connection.cursor()
        sql = "SELECT id_usuario, nombre, correo, rol, activo FROM usuario WHERE id_usuario = %s"
        cursor.execute(sql, (user_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return User(row[0], row[1], row[2], None, row[3], bool(row[4]))
        return None

    @classmethod
    def get_all(cls, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_usuario, nombre, correo, rol, activo, fecha_creacion FROM usuario"
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def create_user(cls, db, nombre, correo, contrasena_hash, rol):
        cursor = db.connection.cursor()
        sql = """
        INSERT INTO usuario (nombre, correo, contrasena_hash, rol)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, correo, contrasena_hash, rol))
        db.connection.commit()
        cursor.close()

    @classmethod
    def update_user(cls, db, id_usuario, nombre, correo, rol):
        cursor = db.connection.cursor()
        sql = """
            UPDATE usuario
            SET nombre = %s, correo = %s, rol = %s
            WHERE id_usuario = %s
        """
        cursor.execute(sql, (nombre, correo, rol, id_usuario))
        db.connection.commit()
        cursor.close()
        return True

    @classmethod
    def toggle_user(cls, db, id_usuario):
        cursor = db.connection.cursor()
        # Cambiamos activo a su opuesto
        sql = "UPDATE usuario SET activo = NOT activo WHERE id_usuario = %s"
        cursor.execute(sql, (id_usuario,))
        db.connection.commit()
        # Recuperamos el nuevo estado
        cursor.execute("SELECT activo FROM usuario WHERE id_usuario = %s", (id_usuario,))
        nuevo = cursor.fetchone()[0]
        cursor.close()
        return bool(nuevo)
    
    @classmethod
    def delete_user(cls, db, id_usuario):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM usuario WHERE id_usuario = %s"
            cursor.execute(sql, (id_usuario,))
            db.connection.commit()
            cursor.close()
        except Exception as ex:
            raise Exception(ex)
