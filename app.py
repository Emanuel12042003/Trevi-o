from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
import pusher
import logging

# Configurar logger
logging.basicConfig(level=logging.INFO)

# Conexión a la base de datos
def obtener_conexion():
    return mysql.connector.connect(
        host="darkorchid-worm-307341.hostingersite.com",
        database="u230126021_SALARIOS",
        user="u230126021_Emanuel12",
        password="Hernandez1204"
    )

# Configuración Pusher
pusher_client = pusher.Pusher(
    app_id="1874485",
    key="970a7d4d6af4b86adcc6",
    secret="2e26ccd3273ad909a49d",
    cluster="us2",
    ssl=True
)

app = Flask(__name__)

# Página principal
@app.route("/")
def index():
    return render_template("empleados.html")

### CRUD Empleados ###
@app.route("/empleados", methods=["GET", "POST"])
def empleados():
    con = obtener_conexion()
    cursor = con.cursor(dictionary=True)
    
    if request.method == "POST":
        id_empleado = request.form.get("id_empleado")
        nombre = request.form["nombre"]
        puesto = request.form["puesto"]
        departamento = request.form["departamento"]
        
        if id_empleado:
            cursor.execute("""
                UPDATE empleados SET nombre=%s, puesto=%s, departamento=%s WHERE id_empleado=%s
            """, (nombre, puesto, departamento, id_empleado))
        else:
            cursor.execute("""
                INSERT INTO empleados (nombre, puesto, departamento) VALUES (%s, %s, %s)
            """, (nombre, puesto, departamento))
        
        con.commit()
        notificar_actualizacion("empleados")
        con.close()
        return jsonify({"message": "Empleado guardado exitosamente"})
    
    cursor.execute("SELECT * FROM empleados")
    empleados = cursor.fetchall()
    con.close()
    return jsonify(empleados)

### CRUD Asistencias ###
@app.route("/asistencias", methods=["GET", "POST"])
def asistencias():
    con = obtener_conexion()
    cursor = con.cursor(dictionary=True)
    
    if request.method == "POST":
        id_asistencia = request.form.get("id_asistencia")
        id_empleado = request.form["id_empleado"]
        fecha = request.form["fecha"]
        hora_entrada = request.form["hora_entrada"]
        hora_salida = request.form["hora_salida"]
        
        if id_asistencia:
            cursor.execute("""
                UPDATE asistencias SET id_empleado=%s, fecha=%s, hora_entrada=%s, hora_salida=%s WHERE id_asistencia=%s
            """, (id_empleado, fecha, hora_entrada, hora_salida, id_asistencia))
        else:
            cursor.execute("""
                INSERT INTO asistencias (id_empleado, fecha, hora_entrada, hora_salida) VALUES (%s, %s, %s, %s)
            """, (id_empleado, fecha, hora_entrada, hora_salida))
        
        con.commit()
        notificar_actualizacion("asistencias")
        con.close()
        return jsonify({"message": "Asistencia guardada exitosamente"})
    
    cursor.execute("SELECT * FROM asistencias")
    asistencias = cursor.fetchall()
    con.close()
    return jsonify(asistencias)

### CRUD Bonificaciones ###
@app.route("/bonificaciones", methods=["GET", "POST"])
def bonificaciones():
    con = obtener_conexion()
    cursor = con.cursor(dictionary=True)
    
    if request.method == "POST":
        id_bonificacion = request.form.get("id_bonificacion")
        id_empleado = request.form["id_empleado"]
        motivo = request.form["motivo"]
        monto = request.form["monto"]
        fecha = request.form["fecha"]
        
        if id_bonificacion:
            cursor.execute("""
                UPDATE bonificaciones SET id_empleado=%s, motivo=%s, monto=%s, fecha=%s WHERE id_bonificacion=%s
            """, (id_empleado, motivo, monto, fecha, id_bonificacion))
        else:
            cursor.execute("""
                INSERT INTO bonificaciones (id_empleado, motivo, monto, fecha) VALUES (%s, %s, %s, %s)
            """, (id_empleado, motivo, monto, fecha))
        
        con.commit()
        notificar_actualizacion("bonificaciones")
        con.close()
        return jsonify({"message": "Bonificación guardada exitosamente"})
    
    cursor.execute("SELECT * FROM bonificaciones")
    bonificaciones = cursor.fetchall()
    con.close()
    return jsonify(bonificaciones)

# Función de notificación con Pusher
def notificar_actualizacion(canal):
    pusher_client.trigger(canal, "actualizacion", {})

if __name__ == "__main__":
    app.run(debug=True)
