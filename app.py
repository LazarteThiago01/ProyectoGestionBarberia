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

#base de datos
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy # Nueva librería

app = Flask(__name__)

# Configuración de la Base de Datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barberia.db'
db = SQLAlchemy(app)

# Definimos cómo se guarda un Turno
class Turno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    peluquero = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.String(50), nullable=False)

# Creamos el archivo de la base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reservar', methods=['POST'])
def reservar():
    # 1. Obtenemos los datos del formulario
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    peluquero = request.form.get('peluquero')
    fecha = request.form.get('fecha')

    # 2. Creamos el objeto Turno y lo guardamos en la DB
    nuevo_turno = Turno(nombre=nombre, email=email, peluquero=peluquero, fecha=fecha)
    db.session.add(nuevo_turno)
    db.session.commit()

    return f"Turno guardado en la base de datos para {nombre}!"

if __name__ == '__main__':
    app.run(debug=True)

# vista para peluqueros
@app.route('/turnos')
def ver_turnos():
    # Consultamos todos los turnos guardados en la base de datos
    todos_los_turnos = Turno.query.all()
    return render_template('turnos.html', lista_turnos=todos_los_turnos)