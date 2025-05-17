# Consulta Docentes – FES Aragón

**Consulta Docentes** es una aplicación web para la gestión y consulta de información de profesores de la FES Aragón. Permite a usuarios sin privilegios ver y exportar datos, y a administradores crear, editar, eliminar o desactivar cuentas y registros. Incluye también un dashboard con estadísticas de género, categoría y grado académico.

---

## 🛠️ Tecnologías

- **Back-end**: Python 3.11, [Flask](https://flask.palletsprojects.com/)  
- **Base de datos**: MySQL  
- **ORM/DB driver**: [flask-mysqldb](https://github.com/flask-mysqldb/flask-mysqldb)  
- **Autenticación**: [Flask‑Login](https://flask-login.readthedocs.io/) + Werkzeug (hash de contraseñas con scrypt)  
- **Front-end**: HTML5, Bootstrap 5, Jinja2, Apache ECharts  
- **Despliegue**: render.com (u otro PaaS) con variables de entorno y base de datos remota  

---

## 🚀 Características

- **Módulo Usuarios**  
  - Alta, edición, baja (soft‑delete via `activo`), roles (`admin` vs. `usuario`).  
  - Login/Logout seguro, control de sesiones, CSRF protection.  

- **Módulo Profesores**  
  - Listado responsivo (tabla y tarjetas móviles).  
  - Crear, editar y eliminar profesores.  
  - Importar/Exportar CSV con validación previa.  
  - Búsqueda en tiempo real y selección múltiple.  
  - Fechas de ingreso mostradas de forma “relativa” con tooltip de la fecha exacta.

- **Dashboard**  
  - Distribución por categoría (barra horizontal).  
  - Distribución por género (pie chart).  
  - Distribución por grado (barra horizontal).  
  - Gráficos responsivos, colores llamativos, resize automático.

- **Footer legal**  
  - Aviso de derechos, licencia CC BY‑NC 4.0, enlaces a avisos de privacidad y CCTV.

---

## 📥 Instalación local

1. **Clona el repositorio**  
   ```bash
   git clone https://github.com/tu_org/consulta_docentes.git
   cd consulta_docentes
