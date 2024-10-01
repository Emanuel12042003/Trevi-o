from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Conexión a la base de datos MySQL
def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='nombre_de_tu_base_de_datos',
            user='tu_usuario',
            password='tu_contraseña'
        )
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return connection

# Ruta para el formulario de registro
@app.route('/')
def index():
    return render_template('app.html')

# Ruta para procesar el formulario
@app.route('/registrar', methods=['POST'])
def registrar():
    nombre_usuario = request.form['Nombre_Usuario']
    contrasena = request.form['contrasena']
    confirmar_contrasena = request.form['confirmar_contrasena']

    if contrasena != confirmar_contrasena:
        flash('Las contraseñas no coinciden.')
        return redirect(url_for('index'))

    # Guardar en la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO Usuarios (Nombre_Usuario, contrasena) VALUES (%s, %s)", (nombre_usuario, contrasena))
        connection.commit()
        flash('Usuario registrado exitosamente.')
    except Error as e:
        flash(f"Error al registrar usuario: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
