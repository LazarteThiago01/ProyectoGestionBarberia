from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
# Nueva librería obligatoria para encriptar claves
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# --- CONFIGURACIÓN DE BASE DE DATOS ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barberia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'burzaco1936' 

db = SQLAlchemy(app)

# --- MODELOS (TABLAS EN SQLITE) ---
class Turno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    peluquero = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(20), default='pendiente')

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False) # Guardará la clave encriptada
    rol = db.Column(db.String(20), default='cliente') 

class Peluquero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

# --- RUTAS PÚBLICAS / CLIENTES ---

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
    
    return redirect('/')

# --- REGISTRO DE USUARIOS SEGURO ---
@app.route('/registro', methods=['POST'])
def registro():
    usuario_ingresado = request.form.get('usuario')
    password_ingresada = request.form.get('password')
    
    if usuario_ingresado and password_ingresada:
        existe = Usuario.query.filter_by(username=usuario_ingresado).first()
        if existe:
            return redirect('/?action=registro&error=usuario_existe')
            
        # 1. Encriptamos la contraseña antes de guardarla
        password_encriptada = generate_password_hash(password_ingresada)
        
        # 2. Control de Roles automático para el Grupo 12 sin claves expuestas
        rol_asignado = 'cliente'
        if usuario_ingresado.lower() in ['thiago', 'martin']:
            rol_assigned = 'admin'
            
        nuevo_usuario = Usuario(username=usuario_ingresado, password=password_encriptada, rol=rol_assigned)
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        session['username'] = nuevo_usuario.username
        session['rol'] = nuevo_usuario.rol
        return redirect('/')
        
    return redirect('/?action=registro&error=1')

# --- LOGIN UNIFICADO SEGURO ---
@app.route('/login', methods=['POST'])
def login():
    usuario_ingresado = request.form.get('usuario')
    password_ingresada = request.form.get('password')
    
    if usuario_ingresado and password_ingresada:
        # Buscamos al usuario en la base de datos por su nombre
        usuario_db = Usuario.query.filter_by(username=usuario_ingresado).first()
        
        # check_password_hash descifra y compara de forma segura las credenciales
        if usuario_db and check_password_hash(usuario_db.password, password_ingresada):
            session['username'] = usuario_db.username
            session['rol'] = usuario_db.rol
            
            # Si eres admin, te manda directo al panel de turnos
            if usuario_db.rol == 'admin':
                return redirect('/turnos')
            return redirect('/')
            
    return redirect('/?action=login&error=credenciales')

# --- LOGOUT UNIFICADO ---
@app.route('/logout')
def logout():
    session.clear() 
    return redirect('/')


# =====================================================================
# RUTAS DEL PANEL DE USUARIO (CLIENTE)
# =====================================================================

@app.route('/mis-turnos')
def mis_turnos():
    if not session.get('username'):
        return redirect('/')
        
    usuario_actual = session.get('username')
    turnos_cliente = Turno.query.filter_by(nombre=usuario_actual).all()
    return render_template('mis_turnos.html', turnos=turnos_cliente)


# =====================================================================
# RUTAS DEL PANEL DE ADMINISTRACIÓN PROTEGIDAS (ADMIN)
# =====================================================================

@app.route('/turnos')
def ver_turnos():
    if session.get('rol') != 'admin':
        return redirect('/') 
        
    lista_turnos = Turno.query.all()
    return render_template('turnos.html', turnos=lista_turnos) 

@app.route('/admin/peluqueros/')
def panel_peluqueros():
    if session.get('rol') != 'admin':
        return redirect('/')
        
    lista_p = Peluquero.query.all()
    return render_template('admin.peluqueros.html', peluqueros=lista_p)


# --- ACCIONES ADMINISTRATIVAS REALES ---

@app.route('/admin/peluqueros/agregar', methods=['POST'])
def agregar_peluquero():
    if session.get('rol') != 'admin':
        return redirect('/')
    
    nombre_b = request.form.get('nombre')
    if nombre_b:
        nuevo_p = Peluquero(nombre=nombre_b)
        db.session.add(nuevo_p)
        db.session.commit()
    return redirect('/admin/peluqueros/')

@app.route('/admin/peluqueros/eliminar/<int:id>')
def eliminar_peluquero(id):
    if session.get('rol') != 'admin':
        return redirect('/')
        
    p = db.session.get(Peluquero, id)
    if p:
        db.session.delete(p)
        db.session.commit()
    return redirect('/admin/peluqueros/')

@app.route('/admin/turnos/confirmar/<int:id>')
def confirmar_turno(id):
    if session.get('rol') != 'admin':
        return redirect('/')
        
    turno = db.session.get(Turno, id)
    if turno:
        turno.estado = 'confirmado'
        db.session.commit()
    return redirect('/turnos')

@app.route('/admin/turnos/cancelar/<int:id>')
def cancelar_turno(id):
    if session.get('rol') != 'admin':
        return redirect('/')
        
    turno = db.session.get(Turno, id)
    if turno:
        turno.estado = 'cancelado'
        db.session.commit()
    return redirect('/turnos')


# --- INICIO DEL SERVIDOR ---
if __name__ == '__main__':
    app.run(debug=True)