from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- CONFIGURACIÓN DE BASE DE DATOS ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barberia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'burzaco1936' 
ADMIN_PASSWORD = "burzaco1936" # Si alguien se registra con esta clave, será Admin

db = SQLAlchemy(app)

# --- MODELOS (TABLAS) ---
class Turno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    peluquero = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.String(50), nullable=False)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(20), default='cliente') 

class Peluquero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

# --- RUTAS PÚBLICAS ---

@app.route('/')
def home():
    lista_p = Peluquero.query.all()
    return render_template('index.html', peluqueros=lista_p)

@app.route('/reservar', methods=['POST'])
def reservar():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    peluquero = request.form.get('peluquero')
    fecha = request.form.get('fecha')

    nuevo_turno = Turno(nombre=nombre, email=email, peluquero=peluquero, fecha=fecha)
    db.session.add(nuevo_turno)
    db.session.commit()
    return f"<h1>¡Turno Registrado!</h1><p>Hola {nombre}, turno con {peluquero} guardado.</p><a href='/'>Volver</a>"

# -- LOGIN Y REGISTRO --

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        user = request.form.get('username')
        passw = request.form.get('password')
        
        # Lógica automática: si la clave es la de admin, se guarda con rol admin
        determinar_rol = 'cliente'
        if passw == ADMIN_PASSWORD:
            determinar_rol = 'admin'

        nuevo_usuario = Usuario(username=user, password=passw, rol=determinar_rol)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        passw = request.form.get('password')
        usuario = Usuario.query.filter_by(username=user, password=passw).first()
        
        if usuario:
            session['user_id'] = usuario.id
            session['rol'] = usuario.rol
            session['username'] = usuario.username
            return redirect(url_for('home'))
        else:
            return "Usuario o contraseña incorrectos"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# --- RUTAS DE ADMINISTRACIÓN ---

@app.route('/turnos')
def ver_turnos():
    if session.get('rol') != 'admin':
        return "Acceso denegado.", 403
    todos_los_turnos = Turno.query.all()
    return render_template('turnos.html', lista_turnos=todos_los_turnos)

@app.route('/admin/peluqueros/')
def admin_peluqueros():
    if session.get('rol') != 'admin':
        return "Acceso denegado.", 403
    todos = Peluquero.query.all()
    return render_template('admin_peluqueros.html', peluqueros=todos)

@app.route('/admin/agregar_peluquero', methods=['POST'])
def agregar_peluquero():
    nombre = request.form.get('nombre')
    if nombre:
        nuevo = Peluquero(nombre=nombre)
        db.session.add(nuevo)
        db.session.commit()
    return redirect(url_for('admin_peluqueros'))

@app.route('/admin/eliminar_peluquero/<int:id>')
def eliminar_peluquero(id):
    p = db.session.get(Peluquero, id)
    if p:
        db.session.delete(p)
        db.session.commit()
    return redirect(url_for('admin_peluqueros'))

# --- INICIO DEL SERVIDOR (AL FINAL DE TODO) ---
if __name__ == '__main__':
    app.run(debug=True)