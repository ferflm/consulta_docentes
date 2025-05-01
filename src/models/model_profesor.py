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
        
    @classmethod
    def get_profesor_by_id(cls, db, id_profesor):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_profesor, nombre, a_paterno, a_materno, genero, nombre_categoria, nombre_grado, num_trabajador, rfc, curp, ingreso_unam, ingreso_carrera, correo, num_cel, num_tel, direccion FROM profesor p JOIN categoria c ON p.id_categoria = c.id_categoria JOIN grado g ON p.id_grado = g.id_grado WHERE id_profesor = %s"
            cursor.execute(sql, (id_profesor,))
            row = cursor.fetchone()
            cursor.close()

            if row:
                return Profesor(*row)
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update_profesor(cls, db, profesor):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE profesor SET nombre = %s, a_paterno = %s, a_materno = %s, genero = %s, id_categoria = %s, id_grado = %s, num_trabajador = %s, rfc = %s, curp = %s, ingreso_unam = %s, ingreso_carrera = %s, correo = %s, num_cel = %s, num_tel = %s, direccion = %s WHERE id_profesor = %s"
            
            values = (
                profesor.nombre, profesor.a_paterno, profesor.a_materno, profesor.genero,
                profesor.id_categoria, profesor.id_grado, profesor.num_trabajador,
                profesor.rfc, profesor.curp, profesor.ingreso_unam, profesor.ingreso_carrera,
                profesor.correo, profesor.num_cel, profesor.num_tel, profesor.direccion,
                profesor.id_profesor
            )
            
            cursor.execute(sql, values)
            db.connection.commit()
            cursor.close()
            return True
        except Exception as ex:
            raise Exception(ex)