from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
import pusher
import datetime
import pytz

# Conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

# Página principal que carga el CRUD de usuarios
@app.route("/")
def index():
    con.close()
    return render_template("app.html")

# Crear o actualizar un usuario
@app.route("/usuarios/guardar", methods=["POST"])
def usuariosGuardar():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.form.get("id_usuario")
    nombre_usuario = request.form["nombre_usuario"]
    contrasena = request.form["contrasena"]

    cursor = con.cursor()
    if id_usuario:  # Actualizar
        sql = """
        UPDATE tst0_usuarios SET Nombre_Usuario = %s, Contrasena = %s WHERE Id_Usuario = %s
        """
        val = (nombre_usuario, contrasena, id_usuario)
    else:  # Crear nuevo usuario
        sql = """
        INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena) VALUES (%s, %s)
        """
        val = (nombre_usuario, contrasena)

    cursor.execute(sql, val)
    con.commit()
    cursor.close()
    con.close()

    notificar_actualizacion_usuarios()

    return make_response(jsonify({"message": "Usuario guardado exitosamente"}))

# Obtener todos los usuarios
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tst0_usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    con.close()

    return make_response(jsonify(usuarios))

# Obtener un usuario por su ID
@app.route("/usuarios/editar", methods=["GET"])
def editar_usuario():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.args.get("id")
    cursor = con.cursor(dictionary=True)
    sql = "SELECT * FROM tst0_usuarios WHERE Id_Usuario = %s"
    val = (id_usuario,)
    cursor.execute(sql, val)
    usuario = cursor.fetchone()
    cursor.close()
    con.close()

    return make_response(jsonify(usuario))

# Eliminar un usuario
@app.route("/usuarios/eliminar", methods=["POST"])
def eliminar_usuario():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.form["id"]
    cursor = con.cursor()
    sql = "DELETE FROM tst0_usuarios WHERE Id_Usuario = %s"
    val = (id_usuario,)
    cursor.execute(sql, val)
    con.commit()
    cursor.close()
    con.close()

    notificar_actualizacion_usuarios()

    return make_response(jsonify({"message": "Usuario eliminado exitosamente"}))

# Notificar a través de Pusher sobre actualizaciones en la tabla de usuarios
def notificar_actualizacion_usuarios():
    pusher_client = pusher.Pusher(
        app_id="1874485",
        key="970a7d4d6af4b86adcc6",
        secret="2e26ccd3273ad909a49d",
        cluster="us2",
        ssl=True
    )
    pusher_client.trigger("canalUsuarios", "actualizacion", {})

if __name__ == "__main__":
    app.run(debug=True)
