from flask import Flask, render_template, request, jsonify
import mysql.connector
import pusher

# Configuración de conexión a la base de datos
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

@app.route("/")
def index():
    return render_template("empleados.html")

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
        pusher_client.trigger("empleados", "actualizacion", {})
        con.close()
        return jsonify({"message": "Empleado guardado correctamente"})
    
    cursor.execute("SELECT * FROM empleados")
    empleados = cursor.fetchall()
    con.close()
    return jsonify(empleados)

if __name__ == "__main__":
    app.run(debug=True)
