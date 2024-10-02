from flask import Flask, request, render_template

app = Flask(__name__)

# almacenar los usuarios
usuarios = []


@app.route('/')
def index():
    return render_template('app.html', usuarios=usuarios)

# Insertar un nuevo registro vía GET
@app.route('/registrar', methods=['GET'])
def registrar():
    nombre_usuario = request.args.get('Nombre_Usuario')
    contrasena = request.args.get('contrasena')

    # Crear un nuevo ID no repetido
    usuario_id = len(usuarios) + 1

    # Añadir el nuevo usuario a la lista
    nuevo_usuario = {'id': usuario_id, 'nombre': nombre_usuario, 'contrasena': contrasena}
    usuarios.append(nuevo_usuario)

    # Redirigir a pagina principal
    return render_template('app.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)
