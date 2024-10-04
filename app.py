from flask import Flask, render_template, request, jsonify, make_response
import pusher
import mysql.connector
import datetime
import pytz

app = Flask(__name__)

# Credenciales de Pusher
pusher_client = pusher.Pusher(
    app_id="1874485",
    key="970a7d4d6af4b86adcc6",
    secret="2e26ccd3273ad909a49d",
    cluster="us2",
    ssl=True
)

# Configuración de la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

@app.route("/")
def index():
    return render_template("app.html")

# Leer usuarios
@app.route("/usuarios")
def usuarios():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT Id_Usuario, Nombre_Usuario FROM tst0_usuarios")
    usuarios = cursor.fetchall()
    con.close()

    return make_response(jsonify(usuarios))

# Crear o actualizar usuario
@app.route("/usuarios/guardar", methods=["POST"])
def guardar_usuario():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.form.get("id_usuario")
    nombre_usuario = request.form["nombre_usuario"]
    contrasena = request.form["contrasena"]

    cursor = con.cursor()

    if id_usuario:
        # Actualizar usuario existente
        sql = "UPDATE tst0_usuarios SET Nombre_Usuario=%s, Contrasena=%s WHERE Id_Usuario=%s"
        val = (nombre_usuario, contrasena, id_usuario)
    else:
        # Crear nuevo usuario
        sql = "INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena) VALUES (%s, %s)"
        val = (nombre_usuario, contrasena)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    pusher_client.trigger("canalUsuarios", "actualizacionUsuario", {"message": "Usuario guardado correctamente"})

    return make_response(jsonify({}))

# Eliminar usuario
@app.route("/usuarios/eliminar", methods=["POST"])
def eliminar_usuario():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.form["id_usuario"]

    cursor = con.cursor()
    sql = "DELETE FROM tst0_usuarios WHERE Id_Usuario=%s"
    val = (id_usuario,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    pusher_client.trigger("canalUsuarios", "actualizacionUsuario", {"message": "Usuario eliminado correctamente"})

    return make_response(jsonify({}))
    
if __name__ == "__main__":
    app.run(debug=True)
