from flask import Flask, render_template, request, jsonify
import mysql.connector
import pusher

# Conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

# Inicialización de la app Flask
app = Flask(__name__)

# Configuración de Pusher
pusher_client = pusher.Pusher(
    app_id="1874485",
    key="970a7d4d6af4b86adcc6",
    secret="2e26ccd3273ad909a49d",
    cluster="us2",
    ssl=True
)

@app.route("/")
def index():
    return render_template("app.html")

# CRUD de usuarios

# Crear un usuario (POST)
@app.route("/usuarios/crear", methods=["POST"])
def crear_usuario():
    if not con.is_connected():
        con.reconnect()

    nombre_usuario = request.form["nombre_usuario"]
    contrasena = request.form["contrasena"]

    cursor = con.cursor()
    sql = "INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena) VALUES (%s, %s)"
    val = (nombre_usuario, contrasena)

    cursor.execute(sql, val)
    con.commit()
    cursor.close()

    notificar_actualizacion_usuarios()

    return jsonify({"message": "Usuario creado exitosamente"})

# Leer (obtener) todos los usuarios (GET)
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tst0_usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    
    return jsonify(usuarios)

# Leer (obtener) un usuario por id_usuario (GET)
@app.route("/usuarios/editar/<int:id_usuario>", methods=["GET"])
def editar_usuario(id_usuario):
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tst0_usuarios WHERE Id_Usuario = %s", (id_usuario,))
    usuario = cursor.fetchone()
    cursor.close()

    return jsonify(usuario)

# Actualizar un usuario (POST)
@app.route("/usuarios/actualizar/<int:id_usuario>", methods=["POST"])
def actualizar_usuario(id_usuario):
    if not con.is_connected():
        con.reconnect()

    nombre_usuario = request.form["nombre_usuario"]
    contrasena = request.form["contrasena"]

    cursor = con.cursor()
    sql = "UPDATE tst0_usuarios SET Nombre_Usuario = %s, Contrasena = %s WHERE Id_Usuario = %s"
    val = (nombre_usuario, contrasena, id_usuario)

    cursor.execute(sql, val)
    con.commit()
    cursor.close()

    notificar_actualizacion_usuarios()

    return jsonify({"message": "Usuario actualizado exitosamente"})

# Eliminar un usuario (POST)
@app.route("/usuarios/eliminar/<int:id_usuario>", methods=["POST"])
def eliminar_usuario(id_usuario):
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "DELETE FROM tst0_usuarios WHERE Id_Usuario = %s"
    val = (id_usuario,)

    cursor.execute(sql, val)
    con.commit()
    cursor.close()

    notificar_actualizacion_usuarios()

    return jsonify({"message": "Usuario eliminado exitosamente"})

# Función para notificar cambios con Pusher
def notificar_actualizacion_usuarios():
    pusher_client.trigger("canalUsuarios", "actualizacion", {})

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
