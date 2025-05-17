from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort, send_file, Response
from flask_login import login_required, current_user

from ..models.model_profesor import Model_Profesor
from ..models.entities.Profesor import Profesor
from ..models.model_categoria import Model_Categoria
from ..models.model_grado import Model_Grado

from datetime import datetime, date
import io
import json
import csv

profesor_bp = Blueprint('profesor', __name__)

@profesor_bp.route('/')
@login_required
def profesores():
    lista = Model_Profesor.get_profesores(current_app.mysql)
    return render_template('profesores.html', profesores = lista)


## GET
@profesor_bp.route('/profesores/plantilla', methods=['GET'])
@login_required
def descargar_plantilla():
    return send_file('static/csv/plantilla.csv', mimetype='text/csv', as_attachment=True, download_name='plantilla.csv')

@profesor_bp.route('/dashboard')
@login_required
def dashboard():
    try:
        cursor = current_app.mysql.connection.cursor()

        # Distribución por género
        cursor.execute("SELECT genero, COUNT(*) FROM profesor GROUP BY genero")
        genero_data = cursor.fetchall()

        # Distribución por categoría
        cursor.execute("""
            SELECT c.nombre_categoria, COUNT(*) 
            FROM profesor p
            JOIN categoria c ON p.id_categoria = c.id_categoria 
            GROUP BY c.nombre_categoria
        """)
        categoria_data = cursor.fetchall()

        # Distribución por grado
        cursor.execute("""
            SELECT g.nombre_grado, COUNT(*) 
            FROM profesor p
            JOIN grado g ON p.id_grado = g.id_grado 
            GROUP BY g.nombre_grado
        """)
        grado_data = cursor.fetchall()

        cursor.close()

        return render_template('dashboard.html',
                            genero_data=genero_data,
                            categoria_data=categoria_data,
                            grado_data=grado_data)

    except Exception as ex:
        flash(f'Error al cargar datos del dashboard: {ex}', 'danger')
        return redirect(url_for('profesor.profesores'))

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return '<h1>Page not found</h1>'

## POST
@profesor_bp.route('/delete/<int:id_profesor>', methods=['POST'])
@login_required
def delete_profesor(id_profesor):
    if current_user.rol != 'admin':
        abort(403)
    try:
        Model_Profesor.delete_by_id(current_app.mysql, id_profesor)
        flash('Profesor eliminado correctamente', 'success')
    except Exception as ex:
        flash(f'Error al eliminar el profesor: {str(ex)}', 'danger')
    profesores = Model_Profesor.get_profesores(current_app.mysql)
    return render_template('profesores.html', profesores = profesores)

@profesor_bp.route('/exportar', methods=['POST'])
@login_required
def export_profesores():
    if current_user.rol != 'admin':
        abort(403)
    seleccionados = request.form.getlist('seleccionados')

    if not seleccionados:
        flash('No se seleccionaron profesores para exportar.', 'warning')
        return redirect(url_for('profesor.profesores'))
    
    try:
        ids = tuple(map(int, seleccionados))
        profesores = Model_Profesor.get_profesores_by_ids(current_app.mysql, ids)

        output = io.StringIO()
        output.write('\ufeff') # Add BOM for Excel compatibility

        writer = csv.writer(output)
        writer.writerow(['ID', 'Nombre', 'Apellido Paterno', 'Apellido Materno', 'Género',
                        'Categoría', 'Grado', 'Núm. Trabajador', 'RFC', 'CURP',
                        'Ingreso UNAM', 'Ingreso Carrera', 'Correo', 'Celular', 'Teléfono', 'Dirección'])
        
        for p in profesores:
            writer.writerow([p.id_profesor, p.nombre, p.a_paterno, p.a_materno, p.genero,
                            p.categoria, p.grado, p.num_trabajador, p.rfc, p.curp,
                            p.ingreso_unam, p.ingreso_carrera, p.correo, p.num_cel,
                            p.num_tel, p.direccion])
            
        response = Response(output.getvalue(), mimetype='text/csv')
        response.headers.set('Content-Disposition', 'attachment', filename='profesores.csv')
        return response
    except Exception as e:
        flash(f'Error al exportar profesores: {e}', 'danger')
        return redirect(url_for('profesor.profesores'))

@profesor_bp.route('/profesores/importar/confirmar', methods=['POST'])
@login_required
def confirmar_importacion():
    if current_user.rol != 'admin':
        abort(403)
    try:
        registros_json = request.form['data_json']
        registros = json.loads(registros_json)

        insertados = 0
        for r in registros:
            profesor = Profesor(
                    id_profesor=None,
                    nombre=r['nombre'],
                    a_paterno=r['a_paterno'],
                    a_materno=r['a_materno'],
                    genero=r['genero'],
                    num_trabajador=r['num_trabajador'],
                    rfc=r['rfc'],
                    curp=r['curp'],
                    ingreso_unam=r['ingreso_unam'],
                    ingreso_carrera=r['ingreso_carrera'],
                    correo=r['correo'],
                    num_cel=r['num_cel'],
                    num_tel=r['num_tel'],
                    direccion=r['direccion']
                )
            
            profesor.id_categoria = r['id_categoria']
            profesor.id_grado = r['id_grado']
            Model_Profesor.insert_profesor(current_app.mysql, profesor)
            insertados += 1

        flash(f'{insertados} profesores importados exitosamente.', 'success')
    except Exception as e:
        flash(f'Error durante la importación: {e}', 'danger')

    return redirect(url_for('profesor.profesores'))


## GET & POST
@profesor_bp.route('/editar/<int:id_profesor>', methods=['GET', 'POST'])
@login_required
def edit_profesor(id_profesor):
    if current_user.rol != 'admin':
        abort(403)
    if request.method == 'POST':
        datos = request.form
        profesor = Profesor(
            id_profesor=id_profesor,
            nombre=datos['nombre'],
            a_paterno=datos['a_paterno'],
            a_materno=datos['a_materno'],
            genero=datos['genero'],
            num_trabajador=datos['num_trabajador'],
            rfc=datos['rfc'],
            curp=datos['curp'],
            ingreso_unam=datos['ingreso_unam'],
            ingreso_carrera=datos['ingreso_carrera'],
            correo=datos['correo'],
            num_cel=datos['num_cel'],
            num_tel=datos['num_tel'],
            direccion=datos['direccion']
        )
        profesor.id_categoria = int(datos['id_categoria'])
        profesor.id_grado = int(datos['id_grado'])

        try:
            Model_Profesor.update_profesor(current_app.mysql, profesor)
            flash('Profesor actualizado correctamente.', 'success')
            return redirect(url_for('profesor.profesores'))
        except Exception as e:
            flash(f'Error al actualizar: {e}', 'danger')

    profesor = Model_Profesor.get_profesor_by_id(current_app.mysql, id_profesor)
    categorias = Model_Categoria.get_categorias(current_app.mysql)
    grados = Model_Grado.get_grados(current_app.mysql)
    return render_template('editar_profesor.html', profesor=profesor, categorias=categorias, grados=grados)

@profesor_bp.route('/agregar', methods=['GET', 'POST'])
@login_required
def add_profesor():
    if current_user.rol != 'admin':
        abort(403)
    if request.method == 'POST':
        datos = request.form
        profesor = Profesor(
            id_profesor=None,
            nombre=datos['nombre'],
            a_paterno=datos['a_paterno'],
            a_materno=datos['a_materno'],
            genero=datos['genero'],
            num_trabajador=datos['num_trabajador'],
            rfc=datos['rfc'],
            curp=datos['curp'],
            ingreso_unam=datos['ingreso_unam'],
            ingreso_carrera=datos['ingreso_carrera'],
            correo=datos['correo'],
            num_cel=datos['num_cel'],
            num_tel=datos['num_tel'],
            direccion=datos['direccion']
        )
        profesor.id_categoria = int(datos['id_categoria'])
        profesor.id_grado = int(datos['id_grado'])

        try:
            Model_Profesor.insert_profesor(current_app.mysql, profesor)
            flash('Profesor agregado correctamente.', 'success')
            return redirect(url_for('profesor.profesores'))
        except Exception as e:
            flash(f'Error al agregar profesor: {e}', 'danger')

    categorias = Model_Categoria.get_categorias(current_app.mysql)
    grados = Model_Grado.get_grados(current_app.mysql)
    return render_template('nuevo_profesor.html', categorias=categorias, grados=grados)


@profesor_bp.route('/profesores/importar', methods=['GET', 'POST'])
@login_required
def import_profesores():
    if current_user.rol != 'admin':
        abort(403)
    if request.method == 'GET':
        return render_template('importar_profesores.html')

    archivo = request.files.get('archivo_csv')
    if not archivo or archivo.filename == '':
        flash('No se seleccionó ningún archivo.', 'warning')
        return redirect(url_for('profesor.importar_profesores'))

    try:
        contenido = archivo.read().decode('utf-8-sig')
        reader = csv.DictReader(io.StringIO(contenido))

        registros = []
        errores = []

        for i, row in enumerate(reader, start=2):  # Empieza en línea 2 por encabezados
            error = []
            try:
                profesor = Profesor(
                    id_profesor=None,
                    nombre=row['nombre'].strip(),
                    a_paterno=row['a_paterno'].strip(),
                    a_materno=row['a_materno'].strip(),
                    genero=row['genero'].strip(),
                    num_trabajador=row['num_trabajador'].strip(),
                    rfc=row['rfc'].strip(),
                    curp=row['curp'].strip(),
                    ingreso_unam=row['ingreso_unam'].strip(),
                    ingreso_carrera=row['ingreso_carrera'].strip(),
                    correo=row['correo'].strip(),
                    num_cel=row['num_cel'].strip(),
                    num_tel=row['num_tel'].strip(),
                    direccion=row['direccion'].strip()
                )
                profesor.id_categoria = int(row['id_categoria'])
                profesor.id_grado = int(row['id_grado'])

                # Validaciones
                if profesor.genero not in ['M', 'F']:
                    error.append('Género inválido')
                datetime.strptime(profesor.ingreso_unam, '%Y-%m-%d')
                datetime.strptime(profesor.ingreso_carrera, '%Y-%m-%d')

                registros.append(profesor)
            except Exception as e:
                errores.append({'linea': i, 'mensaje': str(e)})

            registros_dict = [
                {
                    "nombre": p.nombre,
                    "a_paterno": p.a_paterno,
                    "a_materno": p.a_materno,
                    "genero": p.genero,
                    "id_categoria": p.id_categoria,
                    "id_grado": p.id_grado,
                    "num_trabajador": p.num_trabajador,
                    "rfc": p.rfc,
                    "curp": p.curp,
                    "ingreso_unam": p.ingreso_unam,
                    "ingreso_carrera": p.ingreso_carrera,
                    "correo": p.correo,
                    "num_cel": p.num_cel,
                    "num_tel": p.num_tel,
                    "direccion": p.direccion
                }
                for p in registros
            ]

        return render_template('importar_validar.html',
                            registros=registros_dict,
                            errores=errores)
    except Exception as e:
        flash(f'Error al procesar el archivo: {e}', 'danger')
        return redirect(url_for('profesor.importar_profesores'))


## Function to calculate elapsed time
# This function calculates the elapsed time from a given date to today.
def tiempo_transcurrido(fecha):
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
    elif isinstance(fecha, datetime):
        fecha = fecha.date()

    ahora = date.today()
    diferencia = ahora - fecha
    años = diferencia.days // 365
    meses = (diferencia.days % 365) // 30
    dias = (diferencia.days % 365) % 30

    if años > 0:
        return f"{años} año{'s' if años > 1 else ''}"
    elif meses > 0:
        return f"{meses} mes{'es' if meses > 1 else ''}"
    elif dias > 0:
        return f"{dias} día{'s' if dias > 1 else ''}"
    else:
        return "Hoy"