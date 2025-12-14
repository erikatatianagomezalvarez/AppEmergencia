# AppEmergencia

Descripción
-----------
Aplicación web mínima en Python/Flask para gestionar usuarios y tipos de emergencia contra una base de datos MySQL.

Estructura del proyecto
-----------------------
- `app.py` : Aplicación Flask con rutas para `usuarios` y `tbtipoemergencia` (CRUD básico).
- `db.py` : Módulo con la lógica de conexión a MySQL (`get_connection`) y funciones de acceso a datos (usuarios y tipos).
- `test_conection.py` : script de prueba de conexión (original).
- `templates/` : Plantillas HTML:
  - `usuarios_list.html`, `usuario_form.html` — listado y formulario de usuarios.
  - `tipo_list.html`, `tipo_form.html` — listado y formulario para `tbtipoemergencia`.

Arquitectura y decisiones
-------------------------
- Micro aplicación Flask (un solo proceso) para desarrollo y pruebas.
- Acceso a datos mediante `mysql-connector-python` y SQL parametrizado — no se usa ORM por ahora.
- Separación de responsabilidades: `app.py` (rutas y vistas) y `db.py` (conexión + queries).
- Manejo simple de errores con `flash` en vistas y excepciones propagadas desde `db.py`.
- `insert_user` invoca `ensure_auto_increment(4)` para asegurar que `tbusuario` tenga AUTO_INCREMENT >= 4 antes de insertar (requiere permisos `ALTER TABLE`).

Variables de entorno (configuración)
-----------------------------------
Se pueden configurar (opcionales) mediante variables de entorno. Valores por defecto incluidos en `db.py`.
- `DB_HOST` (por defecto `localhost`)
- `DB_PORT` (por defecto `3306`)
- `DB_USER` (por defecto `root`)
- `DB_PASSWORD` (por defecto `12345678`)
- `DB_NAME` (por defecto `sistema_emergencias`)
- `FLASK_SECRET` (por defecto `dev-secret`) — usado para `session`/`flash`.

Instalación y ejecución (Windows - PowerShell)
--------------------------------------------
1. Crear y activar entorno virtual (recomendado):
```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```
2. Instalar dependencias:
```powershell
pip install --upgrade pip
pip install flask mysql-connector-python
```
3. (Opcional) Exportar variables de entorno para tu sesión (ajusta credenciales/puerto):
```powershell
$env:DB_HOST='localhost'
$env:DB_PORT='3306'
$env:DB_USER='root'
$env:DB_PASSWORD='12345678'
$env:DB_NAME='sistema_emergencias'
$env:FLASK_SECRET='mi-secreto-dev'
```
4. Ejecutar la aplicación:

PowerShell (recomendado — evita problemas con `Activate.ps1`):
```powershell
.\run.ps1
```

Windows CMD:
```bat
run.bat
```

Si prefieres usar `python` directamente asegúrate de usar el Python del venv:
```powershell
.\.venv\Scripts\python.exe .\app.py
```
5. Abrir en el navegador:

http://127.0.0.1:5000/usuarios
http://127.0.0.1:5000/tipos

Generar `requirements.txt` (opcional):
```powershell
pip freeze > requirements.txt
```

Esquema de tablas (ejemplo)
---------------------------
**IMPORTANTE:** Para que las claves foráneas funcionen, crea las tablas en **este orden**:
1. Primero: `tbusuario` (tabla padre)
2. Segundo: `tbtipoemergencia` (tabla padre)
3. Tercero: `tbcontactoemergencia` y `tbemergencia` (tablas hijo, que referencian a las padre)

**Opción recomendada:** Ejecuta el archivo `schema.sql` incluido en el proyecto:
```bash
mysql -h localhost -u root -p sistema_emergencias < schema.sql
```

O copia y ejecuta manualmente en MySQL:

-- Tabla de usuarios (ejemplo)
```sql
CREATE TABLE tbusuario (
  idUsuario INT AUTO_INCREMENT PRIMARY KEY,
  cedulaUsuario VARCHAR(20),
  nombresApellidosUsuario VARCHAR(200),
  telefonoUsuario VARCHAR(50),
  contactoEmergenciaUsuario VARCHAR(50),
  tipoUsuario VARCHAR(50),
  direccionUsuario VARCHAR(255),
  emailUsuario VARCHAR(150),
  fechaRegistroUsuario DATETIME,
  estadoUsuario VARCHAR(20)
);
```

-- Tabla tipos de emergencia
```sql
CREATE TABLE tbtipoemergencia (
  idTipoEmergencia INT AUTO_INCREMENT PRIMARY KEY,
  nombreTipoEmergencia VARCHAR(50) NOT NULL,
  descripcionTipoEmergencia TEXT,
  nivelPrioridadTipoEmergencia_3 ENUM('baja','media','alta','critica') NOT NULL,
  estadoTipoEmergencia_4 ENUM('activo','inactivo') NOT NULL
);
```

-- Tabla emergencias (CRUD completo implementado)
```sql
CREATE TABLE tbemergencia (
  idEmergencia INT AUTO_INCREMENT PRIMARY KEY,
  tbUsuario_idUsuario INT NOT NULL,
  tbTipoEmergencia_idTipoEmergencia INT NOT NULL,
  codigoEmergencia INT,
  fechaHoraEmergencia DATETIME,
  tipoEmergencia INT,
  estadoEmergencia ENUM('reportada','en_proceso','atendida','cerrada'),
  ubicacionEmergencia VARCHAR(300),
  latitudEmergencia DECIMAL(11,8),
  longitudEmergencia DECIMAL(11,8),
  descripcionEmergencia TEXT,
  prioridadEmergencia ENUM('baja','media','alta','critica'),
  idusuarioreportaEmergencia INT,
  fechaCierreEmergencia DATETIME,
  observacionesEmergencia TEXT,
  FOREIGN KEY (tbUsuario_idUsuario) REFERENCES tbusuario(idUsuario) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (tbTipoEmergencia_idTipoEmergencia) REFERENCES tbtipoemergencia(idTipoEmergencia) ON DELETE CASCADE ON UPDATE CASCADE
);
```

Consideraciones técnicas y seguridad
------------------------------------
- No expongas credenciales en código: usa variables de entorno o un gestor de secretos.
- `FLASK_SECRET` debe ser fuerte en producción.
- No usar el servidor Flask de desarrollo en producción. Para producción usa Gunicorn, uWSGI o similar detrás de un proxy (Nginx).
- Añadir protección CSRF en formularios (por ejemplo con `Flask-WTF`) si se pone en producción.
- Validación y saneamiento de entradas: actualmente simple; validar y sanitizar datos antes de insertarlos.
- Permisos de BD: el usuario DB necesita `SELECT`, `INSERT`, `UPDATE`, `DELETE` y, si se mantiene `ensure_auto_increment`, `ALTER TABLE`.

Resolución de problemas comunes
-------------------------------
- Error `ModuleNotFoundError: No module named 'flask'`: instalar dependencias en el entorno activo (`pip install flask`).
- Error `Can't connect to MySQL server on 'localhost:3306' (10061)`: comprobar que MySQL está en ejecución y en qué puerto escucha.
  - Probar cambiar `DB_PORT` a `3306` si usas el puerto estándar.
  - Si MySQL está en Docker/WSL, asegúrate de exponer el puerto o de conectar al host/puerto correctos.
  - Verifica credenciales y que el usuario tenga permisos.
- Error `Duplicate entry ... for key 'PRIMARY'`: tu tabla no usa `AUTO_INCREMENT` o ya existe un registro con el id indicado. El código actual omite `idUsuario` en el INSERT y espera `AUTO_INCREMENT`.

Endpoints disponibles
---------------------
- Usuarios
  - `GET /usuarios` — lista usuarios.
  - `GET /usuarios/nuevo` — formulario nuevo usuario.
  - `POST /usuarios/nuevo` — crear usuario.
  - `GET /usuarios/editar/<id>` — formulario editar.
  - `POST /usuarios/editar/<id>` — actualizar.
  - `POST /usuarios/eliminar/<id>` — eliminar.
- Tipos de emergencia
  - `GET /tipos` — lista tipos.
  - `GET /tipos/nuevo` — formulario nuevo tipo.
  - `POST /tipos/nuevo` — crear tipo.
  - `GET /tipos/editar/<id>` — formulario editar.
  - `POST /tipos/editar/<id>` — actualizar.
  - `POST /tipos/eliminar/<id>` — eliminar.
- Servicios de emergencia
  - `GET /servicios` — lista servicios.
  - `GET /servicios/nuevo` — formulario nuevo servicio.
  - `POST /servicios/nuevo` — crear servicio.
  - `GET /servicios/editar/<id>` — formulario editar.
  - `POST /servicios/editar/<id>` — actualizar.
  - `POST /servicios/eliminar/<id>` — eliminar.
- Contactos de emergencia
  - `GET /contactos` — lista contactos.
  - `GET /contactos/nuevo` — formulario nuevo contacto.
  - `POST /contactos/nuevo` — crear contacto.
  - `GET /contactos/editar/<id>` — formulario editar.
  - `POST /contactos/editar/<id>` — actualizar.
  - `POST /contactos/eliminar/<id>` — eliminar.
- Emergencias
  - `GET /emergencias` — lista emergencias.
  - `GET /emergencias/nuevo` — formulario nueva emergencia.
  - `POST /emergencias/nuevo` — crear emergencia.
  - `GET /emergencias/editar/<id>` — formulario editar.
  - `POST /emergencias/editar/<id>` — actualizar.
  - `POST /emergencias/eliminar/<id>` — eliminar.
- Historial de Estados de Emergencias
  - `GET /historialestados` — lista historial.
  - `GET /historialestados/nuevo` — formulario nuevo registro.
  - `POST /historialestados/nuevo` — crear registro.
  - `GET /historialestados/editar/<id>` — formulario editar.
  - `POST /historialestados/editar/<id>` — actualizar.
  - `POST /historialestados/eliminar/<id>` — eliminar.
- Despachos
  - `GET /despacho` — lista despachos.
  - `GET /despacho/nuevo` — formulario nuevo despacho.
  - `POST /despacho/nuevo` — crear despacho.
  - `GET /despacho/editar/<id>` — formulario editar.
  - `POST /despacho/editar/<id>` — actualizar.
  - `POST /despacho/eliminar/<id>` — eliminar.
- Admin
  - `GET /admin` — panel central con enlaces a todos los CRUDs.

Próximos pasos recomendados
---------------------------
- Añadir autenticación/roles si el sistema tendrá usuarios reales.
- Añadir validaciones en servidor y cliente.
- Añadir CSRF y protección contra ataques XSS/SQL (ya usamos consultas parametrizadas).
- Crear scripts de migración o `schema.sql` para inicializar la BD.

Contacto
-------
Si quieres que adapte el proyecto para Docker, WSL, o que añada edición/eliminación de `usuarios` o un panel admin, dímelo y lo implemento.

*** Fin README
