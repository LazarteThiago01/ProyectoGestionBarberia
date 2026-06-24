# 💈 Sistema de Gestión - Barbería Burzaco

Proyecto desarrollado en Python utilizando el microframework **Flask** y **Flask-SQLAlchemy** 

## 🚀 Características
- **Sistema de Autenticación:** Registro e inicio de sesión de usuarios con manejo de roles (Admin / Cliente) mediante sesiones de Flask.
- **Gestión de Turnos:** Alta de reservas por parte de clientes con validación de fechas.
- **Panel de Administración:** Control total de turnos (confirmación y eliminación física) y administración de barberos disponibles.
- **Diseño Dark Modern:** Interfaz adaptativa optimizada con CSS nativo.

## 🛠️ Instalación y Uso
1. Activar el entorno virtual: `venv\Scripts\activate`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar la aplicación: `python app.py`

# 💈 Sistema de Gestión y Reserva de Citas - Barbería Burzaco

¡Bienvenido al sistema oficial de **Barbería Burzaco**! Este proyecto es una aplicación web dinámica desarrollada como trabajo práctico para la facultad. El ecosistema está diseñado bajo el patrón arquitectónico **MVC (Modelo-Vista-Controlador)** utilizando el microframework **Flask** en su núcleo y **Flask-SQLAlchemy** como ORM para la persistencia y manipulación estructurada de los datos.

---

## 🛠️ Stack Tecnológico Utilizado

El proyecto fue construido utilizando herramientas modernas de software libre enfocadas en la eficiencia, velocidad de respuesta y modularidad:

* **Backend:** Python 3.x & Flask (Microframework de alta escalabilidad).
* **Base de Datos:** SQLite3 gestionado mediante **Flask-SQLAlchemy**.
* **Manejo de Sesiones:** Flask-Session nativo para control de autenticación mediante cookies firmadas.
* **Frontend:** HTML5, CSS3 integrado y JavaScript nativo (ES6+) para validaciones asincrónicas en tiempo real.
* **Control de Versiones:** Git & GitHub.

---

## 🚀 Características Clave del Sistema

El sistema cuenta con lógica de negocio diferenciada según el tipo de usuario logueado en la plataforma:

### 👤 Módulo del Cliente
* **Autenticación Segura:** Registro e Inicio de sesión protegido con validaciones de campos obligatorios.
* **Gestión de Perfil:** Reconocimiento dinámico del nombre del cliente en el ecosistema mediante variables de sesión global (`session`).
* **Reserva Inteligente:** Formulario interactivo para agendar citas seleccionando el barbero de preferencia.
* **Validación de Fechas en Frontend:** Control mediante JavaScript que restringe el agendamiento de turnos en días pasados y bloquea automáticamente los domingos (días de cierre del local).
* **Panel "Mis Turnos":** Vista personalizada donde el cliente puede auditar el historial de sus citas y el estado actual de las mismas.

### ⚙️ Módulo de Administración (Panel de Control)
* **Control de Accesos por Roles:** Middleware lógico que impide que usuarios comunes accedan a las rutas críticas de administración.
* **KPIs en Tiempo Real:** Contador integrado que calcula la cantidad de turnos totales almacenados en el sistema mediante filtros de Jinja (`{{ turnos|length }}`).
* **Auditoría de Turnos:** Tabla centralizada con estados de citas ordenados mediante códigos de color (Verde: *Confirmado*, Amarillo: *Pendiente*, Rojo: *Cancelado*).
* **Acciones de Base de Datos Nativa:** * **Confirmar Turno:** Cambia el estado del modelo y ejecuta un `db.session.commit()`.
    * **Eliminar Turno:** Remueve físicamente el registro del turno de la base de datos mediante métodos `POST` seguros.
* **Gestión de Barberos:** Panel independiente para dar de alta y administrar el plantel de profesionales del salón.

---

## 📊 Arquitectura de la Base de Datos (Modelos)

La persistencia de datos utiliza dos tablas relacionales principales controladas por el ORM:

1.  **Modelo `Usuario`:** Almacena credenciales de acceso, nombres e identifica el rol (`admin` o `cliente`) para los permisos de navegación.
2.  **Modelo `Turno`:** Mapea el identificador único (`id`), nombre del cliente, correo electrónico, barbero asignado, la estampa de tiempo formateada (`datetime-local`) y el string correspondiente al estado administrativo (`pendiente`, `confirmado`, `cancelado`).

---

## 💻 Instalación y Despliegue Local

Para clonar y ejecutar este entorno de desarrollo de manera local, seguí estos pasos desde tu terminal:

### 1. Clonar el repositorio y posicionarse en la carpeta
```bash
git clone [https://github.com/tu-usuario/barberia-burzaco.git](https://github.com/tu-usuario/barberia-burzaco.git)
cd barberia-burzaco
