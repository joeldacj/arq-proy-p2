import os
from flask import Flask, render_template_string
import mysql.connector

app = Flask(__name__)

# --- Configuración de la Base de Datos ---
# Usar variables de entorno es una mejor práctica para credenciales,
# pero para este ejemplo simple, puedes ponerlas directamente POR AHORA
# (En producción, SIEMPRE usa variables de entorno o Azure Key Vault)

DB_HOST = "mysql-prod-jcastro114.mysql.database.azure.com" # <--- ¡Tu nombre de host interno de MySQL!
DB_USER = "jcastro114"                     # <--- ¡Tu usuario administrador de MySQL!
DB_PASSWORD = "Enciclopedia2226."                   # <--- ¡Tu contraseña de MySQL!
DB_NAME = "mysql-prod-jcastro114"                  # <--- El nombre de una base de datos en tu servidor (puedes usar la por defecto o crear una simple)

# Plantilla HTML simple para mostrar el resultado
HTML_TEMPLATE = """
<!doctype html>
<html>
<head><title>Estado de la Conexión a DB</title></head>
<body>
    <h1>Estado de la Conexión a la Base de Datos MySQL</h1>
    <p>Intentando conectar a: {{ db_host }}</p>
    <p>Usuario: {{ db_user }}</p>
    <br>
    {% if connection_status == 'success' %}
        <p style="color: green;">¡Conexión exitosa!</p>
        <p>Versión de la base de datos: {{ db_version }}</p>
    {% else %}
        <p style="color: red;">Error al conectar a la base de datos.</p>
        <p>Error: {{ error_message }}</p>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    db_connection_status = 'failure'
    error_message = ''
    db_version = ''

    try:
        # Intentar establecer la conexión
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME # Si no tienes una base de datos específica, puedes omitir esto inicialmente
        )
        if conn.is_connected():
            db_connection_status = 'success'
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION();")
            db_version = cursor.fetchone()[0]
            cursor.close()
            conn.close()

    except mysql.connector.Error as e:
        error_message = str(e)
        db_connection_status = 'failure'

    # Renderizar la plantilla HTML con el resultado
    return render_template_string(HTML_TEMPLATE,
                                  db_host=DB_HOST,
                                  db_user=DB_USER,
                                  connection_status=db_connection_status,
                                  error_message=error_message,
                                  db_version=db_version)

if __name__ == '__main__':
    # Este bloque solo se ejecuta si corres el archivo directamente
    # En Azure App Service, el servidor web (Gunicorn/Waitress)
    # se encargará de correr la aplicación.
    # Puedes usar un puerto diferente para probar localmente si quieres.
    app.run(debug=True) # debug=True muestra errores detallados (úril para desarrollo local)