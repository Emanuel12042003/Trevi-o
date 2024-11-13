from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'e7b4efacf7381f83e05e'

# Configuración de la base de datos
db_config = {
    'host': '185.232.14.52',
    'user': 'u760464709_tst_sep_usr',
    'password': 'dJ0CIAFF',
    'database': 'u760464709_tst_sep'
}

# Función para conectar a la base de datos
def connect_db():
    return mysql.connector.connect(**db_config)

# Ruta para mostrar todas las experiencias
@app.route('/')
def index():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tst0_experiencias")
    experiencias = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', experiencias=experiencias)

# Ruta para agregar una nueva experiencia
@app.route('/agregar', methods=['POST'])
def agregar():
    nombre_apellido = request.form['nombre_apellido']
    comentario = request.form['comentario']
    calificacion = request.form['calificacion']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tst0_experiencias (Nombre_Apellido, Comentario, Calificacion) VALUES (%s, %s, %s)",
                   (nombre_apellido, comentario, calificacion))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Experiencia agregada exitosamente!')
    return redirect(url_for('index'))

# Ruta para eliminar una experiencia
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tst0_experiencias WHERE Id_Experiencia = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Experiencia eliminada exitosamente!')
    return redirect(url_for('index'))

# Ruta para actualizar una experiencia
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    nombre_apellido = request.form['nombre_apellido']
    comentario = request.form['comentario']
    calificacion = request.form['calificacion']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tst0_experiencias SET Nombre_Apellido = %s, Comentario = %s, Calificacion = %s WHERE Id_Experiencia = %s",
                   (nombre_apellido, comentario, calificacion, id))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Experiencia actualizada exitosamente!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
