from .entities.Profesor import Profesor

class Model_Profesor():

    @classmethod
    def get_profesores(cls, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_profesor, nombre, a_paterno, a_materno, genero, nombre_categoria, nombre_grado, num_trabajador, rfc, curp, ingreso_unam, ingreso_carrera, correo, num_cel, num_tel, direccion FROM profesor p JOIN categoria c ON p.id_categoria = c.id_categoria JOIN grado g ON p.id_grado = g.id_grado"
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()

            profesores = []
            for row in rows:
                profesor = Profesor(*row)
                profesores.append(profesor)

            return profesores
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_by_id(cls, db, id_profesor):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM profesor WHERE id_profesor = %s"
            cursor.execute(sql, (id_profesor,))
            db.connection.commit()
            cursor.close()
        except Exception as ex:
            raise Exception(ex)