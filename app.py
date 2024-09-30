from flask import Flask, render_template, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Crear la base de datos
def init_db():
    conn = sqlite3.connect('sensores.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id_log INTEGER PRIMARY KEY AUTOINCREMENT,
            temperatura DOUBLE,
            humedad DOUBLE,
            fecha_hora DATETIME
        )
    ''')
    conn.commit()
    conn.close()

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint para registrar datos
@app.route('/registrar', methods=['POST'])
def registrar():
    temperatura = request.form['temperatura']
    humedad = request.form['humedad']
    fecha_hora = request.form['fecha_hora']

    conn = sqlite3.connect('sensores.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO registros (temperatura, humedad, fecha_hora)
        VALUES (?, ?, ?)
    ''', (float(temperatura), float(humedad), fecha_hora))
    conn.commit()
    
    # Obtener el último ID insertado
    last_id = cursor.lastrowid
    conn.close()

    # Respuesta JSON con los datos ingresados
    return jsonify({
        'id_log': last_id,
        'temperatura': temperatura,
        'humedad': humedad,
        'fecha_hora': fecha_hora
    })

if __name__ == '__main__':
    init_db()  # Inicializa la base de datos
    app.run(debug=True)
