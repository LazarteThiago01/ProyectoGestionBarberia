from flask import Flask, render_template, request

app = Flask(__name__)

# Esta es la ruta principal: lo que se ve al entrar a http://127.0.0.1:5000
@app.route('/')
def home():
    # render_template busca el archivo index.html dentro de la carpeta /templates
    return render_template('index.html')

# Esta ruta recibe los datos del formulario cuando el usuario hace clic en "Reservar"
@app.route('/reservar', methods=['POST'])
def reservar():
    # Capturamos los datos que el usuario escribió en el HTML
    nombre_cliente = request.form.get('nombre')
    email_cliente = request.form.get('email')
    peluquero_elegido = request.form.get('peluquero')
    fecha_turno = request.form.get('fecha')

    # Por ahora, solo vamos a mostrar un mensaje de éxito en la pantalla
    return f"<h1>¡Turno Registrado!</h1> <p>Hola {nombre_cliente}, tu turno con el peluquero {peluquero_elegido} para el {fecha_turno} ha sido reservado. Te enviaremos un correo a {email_cliente}.</p> <a href='/'>Volver al inicio</a>"

if __name__ == '__main__':
    # El modo debug=True permite que el servidor se reinicie solo cada vez que guardas un cambio
    app.run(debug=True)