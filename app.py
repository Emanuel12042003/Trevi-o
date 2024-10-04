from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
import datetime
import pytz
import pusher

# Configuración de la conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

# Ruta para el index
@app.route("/")
def index():
    return render_template("app.html")

# Función para obtener todos los usuarios
@app.route("/usuarios")
def obtener_usuarios():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tst0_usuarios")
    usuarios = cursor.fetchall()
    con.close()

    return make_response(jsonify(usuarios))

# Función para agregar o editar usuarios
@app.route("/usuarios/guardar", methods=["POST"])
def guardar_usuario():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.form.get("id_usuario")
    nombre_usuario = request.form["nombre_usuario"]
    contrasena = request.form["contrasena"]

    cursor = con.cursor()

    if id_usuario:
        # Si se proporciona id_usuario, entonces es una actualización
        sql = """
        UPDATE tst0_usuarios SET
        Nombre_Usuario = %s,
        Contrasena = %s
        WHERE Id_Usuario = %s
        """
        val = (nombre_usuario, contrasena, id_usuario)
    else:
        # Si no hay id_usuario, entonces es una inserción
        sql = """
        INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena)
        VALUES (%s, %s)
        """
        val = (nombre_usuario, contrasena)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({"status": "success"}))

# Función para obtener los datos de un usuario específico
@app.route("/usuarios/editar", methods=["GET"])
def editar_usuario():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.args.get("id_usuario")
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tst0_usuarios WHERE Id_Usuario = %s", (id_usuario,))
    usuario = cursor.fetchone()
    con.close()

    return make_response(jsonify(usuario))

# Función para eliminar un usuario
@app.route("/usuarios/eliminar", methods=["POST"])
def eliminar_usuario():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.form["id_usuario"]
    cursor = con.cursor()
    cursor.execute("DELETE FROM tst0_usuarios WHERE Id_Usuario = %s", (id_usuario,))
    con.commit()
    con.close()

    return make_response(jsonify({"status": "success"}))

if __name__ == "__main__":
    app.run(debug=True)
