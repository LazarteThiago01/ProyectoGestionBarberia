from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- CONFIGURACIÓN DE BASE DE DATOS ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barberia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELOS (TABLAS) ---
class Turno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    peluquero = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.String(50), nullable=False)

class Peluquero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

# Crear las tablas
with app.app_context():
    db.create_all()

# --- RUTAS PÚBLICAS ---

@app.route('/')
def home():
    # Traemos los peluqueros para el selector del index
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

# --- RUTAS DE ADMINISTRACIÓN ---

@app.route('/turnos')
def ver_turnos():
    todos_los_turnos = Turno.query.all()
    return render_template('turnos.html', lista_turnos=todos_los_turnos)

@app.route('/admin/peluqueros/')
def admin_peluqueros():
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

# --- INICIO DEL SERVIDOR (SIEMPRE AL FINAL) ---
if __name__ == '__main__':
    app.run(debug=True)