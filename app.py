from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Lista para almacenar hasta 5 usuarios
usuarios = []

# Ruta principal para renderizar el formulario y la tabla
@app.route('/')
def index():
    return render_template('app.html', usuarios=usuarios)

# Ruta para insertar un nuevo registro vía GET
@app.route('/registrar', methods=['GET'])
def registrar():
    nombre_usuario = request.args.get('Nombre_Usuario')
    contrasena = request.args.get('contrasena')

    # Crear un nuevo ID basado en la longitud de la lista de usuarios
    usuario_id = len(usuarios) + 1

    # Añadir el nuevo usuario a la lista
    nuevo_usuario = {'id': usuario_id, 'nombre': nombre_usuario, 'contrasena': contrasena}
    usuarios.append(nuevo_usuario)

    # Mantener solo los últimos 5 registros
    if len(usuarios) > 5:
        usuarios.pop(0)

    # Redirigir al usuario a la página principal para ver la tabla actualizada
    return render_template('app.html', usuarios=usuarios)

# Ruta para obtener los usuarios en formato JSON (para actualización periódica con AJAX)
@app.route('/obtener_usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify({'usuarios': usuarios})

if __name__ == '__main__':
    app.run(debug=True)
