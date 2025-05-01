from .entities.Grado import Grado

class Model_Grado():

    @classmethod
    def get_grados(cls, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_grado, nombre_grado FROM grado"
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()

            grados = []
            for row in rows:
                grado = Grado(*row)
                grados.append(grado)

            return grados
        except Exception as ex:
            raise Exception(ex)