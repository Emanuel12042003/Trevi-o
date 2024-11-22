from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import logging

# Configurar el logger
logging.basicConfig(level=logging.INFO)

# Configurar la conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="GestionAsistenciaBonificacion",
    user="tu_usuario",
    password="tu_contraseña"
)

app = Flask(__name__)
app.secret_key = "clave_secreta_para_sesiones"

# -------------------
# Ruta de inicio de sesión
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nombre_usuario = request.form["nombre_usuario"]
        contrasena = request.form["contrasena"]
        
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario and check_password_hash(usuario["contrasena"], contrasena):
            session["id_usuario"] = usuario["id_usuario"]
            session["nombre_usuario"] = usuario["nombre_usuario"]
            session["rol"] = usuario["rol"]
            
            if usuario["rol"] == "Recursos Humanos":
                return redirect(url_for("recursos_humanos"))
            else:
                return redirect(url_for("vista_usuario"))
        else:
            flash("Usuario o contraseña incorrectos", "danger")
    
    return render_template("app.html")

# -------------------
# Ruta de cierre de sesión
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -------------------
# Vista para trabajadores normales
@app.route("/usuario")
def vista_usuario():
    if "id_usuario" not in session or session["rol"] != "Trabajador Normal":
        return redirect(url_for("login"))

    id_usuario = session["id_usuario"]
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.nombre_usuario, 
               SUM(CASE WHEN bd.tipo = 'Bonificación' THEN bd.monto ELSE 0 END) AS total_bonificaciones,
               SUM(CASE WHEN bd.tipo = 'Descuento' THEN bd.monto ELSE 0 END) AS total_descuentos,
               (SUM(CASE WHEN bd.tipo = 'Bonificación' THEN bd.monto ELSE 0 END) - 
                SUM(CASE WHEN bd.tipo = 'Descuento' THEN bd.monto ELSE 0 END)) AS sueldo_neto
        FROM usuarios u
        LEFT JOIN bonificaciones_descuentos bd ON u.id_usuario = bd.id_usuario
        WHERE u.id_usuario = %s
        GROUP BY u.nombre_usuario;
    """, (id_usuario,))
    datos = cursor.fetchone()
    cursor.close()
    
    return render_template("usuarios.html", datos=datos)

# -------------------
# Vista para Recursos Humanos
@app.route("/recursos_humanos")
def recursos_humanos():
    if "id_usuario" not in session or session["rol"] != "Recursos Humanos":
        return redirect(url_for("login"))

    return render_template("recursos_humanos.html")

# -------------------
# CRUD para gestión de usuarios
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    if "id_usuario" not in session or session["rol"] != "Recursos Humanos":
        return redirect(url_for("login"))
    
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()

    return jsonify(usuarios)

@app.route("/usuarios/guardar", methods=["POST"])
def guardar_usuario():
    if "id_usuario" not in session or session["rol"] != "Recursos Humanos":
        return redirect(url_for("login"))
    
    id_usuario = request.form.get("id_usuario")
    nombre_usuario = request.form["nombre_usuario"]
    contrasena = request.form["contrasena"]
    rol = request.form["rol"]

    cursor = con.cursor()
    if id_usuario:  # Actualizar
        sql = """
        UPDATE usuarios SET nombre_usuario = %s, contrasena = %s, rol = %s WHERE id_usuario = %s
        """
        contrasena_hashed = generate_password_hash(contrasena)
        cursor.execute(sql, (nombre_usuario, contrasena_hashed, rol, id_usuario))
    else:  # Crear nuevo usuario
        sql = """
        INSERT INTO usuarios (nombre_usuario, contrasena, rol) VALUES (%s, %s, %s)
        """
        contrasena_hashed = generate_password_hash(contrasena)
        cursor.execute(sql, (nombre_usuario, contrasena_hashed, rol))
    
    con.commit()
    cursor.close()
    return jsonify({"message": "Usuario guardado exitosamente"})

@app.route("/usuarios/eliminar/<int:id_usuario>", methods=["POST"])
def eliminar_usuario(id_usuario):
    if "id_usuario" not in session or session["rol"] != "Recursos Humanos":
        return redirect(url_for("login"))
    
    cursor = con.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    con.commit()
    cursor.close()

    return jsonify({"message": "Usuario eliminado exitosamente"})

# -------------------
# Main
if __name__ == "__main__":
    app.run(debug=True)
