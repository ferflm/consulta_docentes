from .entities.Categoria import Categoria

class Model_Categoria():

    @classmethod
    def get_categorias(cls, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_categoria, nombre_categoria FROM categoria"
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()

            categorias = []
            for row in rows:
                categoria = Categoria(*row)
                categorias.append(categoria)

            return categorias
        except Exception as ex:
            raise Exception(ex)