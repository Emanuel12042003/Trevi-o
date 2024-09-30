from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configurar la base de datos (por ejemplo, SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensores.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definir el modelo de la base de datos
class SensorData(db.Model):
    id_log = db.Column(db.BigInteger, primary_key=True)
    temperatura = db.Column(db.Float, nullable=False)
    humedad = db.Column(db.Float, nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

# Ruta para la página principal y mostrar registros
@app.route('/')
def index():
    registros = SensorData.query.all()
    return render_template('index.html', registros=registros)

# Ruta para procesar el registro de los datos
@app.route('/registrar', methods=['POST'])
def registrar():
    if request.method == 'POST':
        temperatura = request.form['temperatura']
        humedad = request.form['humedad']
        fecha_hora = request.form['fecha_hora']

        # Crear una nueva instancia de SensorData
        nuevo_registro = SensorData(
            temperatura=float(temperatura),
            humedad=float(humedad),
            fecha_hora=datetime.strptime(fecha_hora, '%Y-%m-%dT%H:%M')
        )

        # Agregar el registro a la base de datos
        db.session.add(nuevo_registro)
        db.session.commit()

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
