class Profesor:
    def __init__(self, id_profesor, nombre, a_paterno, a_materno, genero,
                 categoria=None, grado=None, num_trabajador=None,
                 rfc=None, curp=None, ingreso_unam=None, ingreso_carrera=None,
                 correo=None, num_cel=None, num_tel=None, direccion=None):
        self.id_profesor = id_profesor
        self.nombre = nombre
        self.a_paterno = a_paterno
        self.a_materno = a_materno
        self.genero = genero
        self.categoria = categoria
        self.grado = grado
        self.num_trabajador = num_trabajador
        self.rfc = rfc
        self.curp = curp
        self.ingreso_unam = ingreso_unam
        self.ingreso_carrera = ingreso_carrera
        self.correo = correo
        self.num_cel = num_cel
        self.num_tel = num_tel
        self.direccion = direccion
        self.id_categoria = None
        self.id_grado = None