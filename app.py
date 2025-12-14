import os
import sys
from datetime import datetime
try:
	from flask import Flask, render_template, request, redirect, url_for, flash, session
except ImportError:
	sys.stderr.write("Module 'flask' not found.\n")
	sys.stderr.write("Start the app using the project's virtualenv or install dependencies.\n")
	sys.stderr.write("Examples:\n")
	sys.stderr.write("  .\\.venv\\Scripts\\python.exe .\\app.py\n")
	sys.stderr.write("  pip install flask mysql-connector-python\n")
	sys.exit(1)

from db import (
	get_all_users,
	insert_user,
	get_user,
	update_user,
	delete_user,
	get_all_tipoemergencia,
	get_tipoemergencia,
	insert_tipoemergencia,
	update_tipoemergencia,
	delete_tipoemergencia,
	get_all_servicioemergencia,
	get_servicioemergencia,
	insert_servicioemergencia,
	update_servicioemergencia,
	delete_servicioemergencia,
	get_all_contactoemergencia,
	get_contactoemergencia,
	insert_contactoemergencia,
	update_contactoemergencia,
	delete_contactoemergencia,
    get_all_emergencia,
    get_emergencia,
    insert_emergencia,
    update_emergencia,
    delete_emergencia,
    get_all_historialestados,
    get_historialestados,
    insert_historialestados,
    update_historialestados,
    delete_historialestados,
    get_all_despacho,
    get_despacho,
    insert_despacho,
    update_despacho,
    delete_despacho,
    register_user,
    authenticate_user,
    get_user_by_id,
    get_emergencias_historial,
)
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', 'dev-secret')


@app.route('/')
def index():
	try:
		current_user = None
		historial = []
		
		if 'user_id' in session:
			user_id = session['user_id']
			current_user = get_user_by_id(user_id)
			historial = get_emergencias_historial(user_id, limit=5)
		
		return render_template('index.html', current_user=current_user, historial=historial)
	except Exception as e:
		flash(f"Error: {e}", 'danger')
		return render_template('index.html', current_user=None, historial=[])


@app.route('/tipos')
def tipos():
	try:
		tipos = get_all_tipoemergencia()
	except Exception as e:
		flash(f"Error al obtener tipos: {e}", 'danger')
		tipos = []
	return render_template('tipo_list.html', tipos=tipos)


@app.route('/tipos/nuevo', methods=['GET'])
def nuevo_tipo_form():
	return render_template('tipo_form.html', tipo=None)


@app.route('/tipos/nuevo', methods=['POST'])
def nuevo_tipo():
	nombre = request.form.get('nombre')
	descripcion = request.form.get('descripcion')
	nivel = request.form.get('nivel')
	estado = request.form.get('estado')

	if not nombre or not nivel or not estado:
		flash('Nombre, nivel y estado son obligatorios.', 'warning')
		return redirect(url_for('nuevo_tipo_form'))

	try:
		new_id = insert_tipoemergencia(nombre, descripcion, nivel, estado)
		flash(f'Tipo creado correctamente (id={new_id}).', 'success')
		return redirect(url_for('tipos'))
	except Exception as e:
		flash(f'Error al crear tipo: {e}', 'danger')
		return redirect(url_for('nuevo_tipo_form'))


@app.route('/tipos/editar/<int:tipo_id>', methods=['GET'])
def editar_tipo_form(tipo_id):
	try:
		tipo = get_tipoemergencia(tipo_id)
	except Exception as e:
		flash(f'Error al cargar tipo: {e}', 'danger')
		return redirect(url_for('tipos'))
	if not tipo:
		flash('Tipo no encontrado.', 'warning')
		return redirect(url_for('tipos'))
	return render_template('tipo_form.html', tipo=tipo)


@app.route('/tipos/editar/<int:tipo_id>', methods=['POST'])
def editar_tipo(tipo_id):
	nombre = request.form.get('nombre')
	descripcion = request.form.get('descripcion')
	nivel = request.form.get('nivel')
	estado = request.form.get('estado')

	if not nombre or not nivel or not estado:
		flash('Nombre, nivel y estado son obligatorios.', 'warning')
		return redirect(url_for('editar_tipo_form', tipo_id=tipo_id))

	try:
		rows = update_tipoemergencia(tipo_id, nombre, descripcion, nivel, estado)
		flash('Tipo actualizado correctamente.', 'success')
		return redirect(url_for('tipos'))
	except Exception as e:
		flash(f'Error al actualizar tipo: {e}', 'danger')
		return redirect(url_for('editar_tipo_form', tipo_id=tipo_id))


@app.route('/tipos/eliminar/<int:tipo_id>', methods=['POST'])
def eliminar_tipo(tipo_id):
	try:
		rows = delete_tipoemergencia(tipo_id)
		flash('Tipo eliminado.' if rows else 'Tipo no encontrado.', 'info')
	except Exception as e:
		flash(f'Error al eliminar tipo: {e}', 'danger')
	return redirect(url_for('tipos'))


@app.route('/usuarios')
def usuarios():
	try:
		users = get_all_users()
	except Exception as e:
		flash(f"Error al obtener usuarios: {e}", 'danger')
		users = []
	return render_template('usuarios_list.html', users=users)


@app.route('/usuarios/nuevo', methods=['GET'])
def nuevo_usuario_form():
	return render_template('usuario_form.html', user=None)


@app.route('/usuarios/nuevo', methods=['POST'])
def nuevo_usuario():
	nombre = request.form.get('nombre')
	email = request.form.get('email')
	telefono = request.form.get('telefono')

	if not nombre or not email:
		flash('Nombre y correo son obligatorios.', 'warning')
		return redirect(url_for('nuevo_usuario_form'))

	try:
		new_id = insert_user(nombre, email, telefono)
		flash(f'Usuario creado correctamente (id={new_id}).', 'success')
		return redirect(url_for('usuarios'))

	except Exception as e:
		flash(f'Error al crear usuario: {e}', 'danger')
		return redirect(url_for('nuevo_usuario_form'))


@app.route('/servicios')
def servicios():
    try:
        servicios = get_all_servicioemergencia()
    except Exception as e:
        flash(f"Error al obtener servicios: {e}", 'danger')
        servicios = []
    return render_template('servicio_list.html', servicios=servicios)


@app.route('/servicios/nuevo', methods=['GET'])
def nuevo_servicio_form():
    return render_template('servicio_form.html', servicio=None)


@app.route('/servicios/nuevo', methods=['POST'])
def nuevo_servicio():
    nombre = request.form.get('nombre')
    tipo = request.form.get('tipo')
    telefono = request.form.get('telefono')
    disponibilidad = request.form.get('disponibilidad')
    direccion = request.form.get('direccion')
    capacidad = request.form.get('capacidad') or None
    horario = request.form.get('horario')
    especialidad = request.form.get('especialidad')
    estado = request.form.get('estado')

    if not nombre or not tipo or not estado:
        flash('Nombre, tipo y estado son obligatorios.', 'warning')
        return redirect(url_for('nuevo_servicio_form'))

    try:
        # convertir capacidad a int si viene
        capacidad_val = int(capacidad) if capacidad else None
        new_id = insert_servicioemergencia(nombre, tipo, telefono, disponibilidad, direccion, capacidad_val, horario, especialidad, estado)
        flash(f'Servicio creado correctamente (id={new_id}).', 'success')
        return redirect(url_for('servicios'))
    except Exception as e:
        flash(f'Error al crear servicio: {e}', 'danger')
        return redirect(url_for('nuevo_servicio_form'))


@app.route('/servicios/editar/<int:servicio_id>', methods=['GET'])
def editar_servicio_form(servicio_id):
    try:
        servicio = get_servicioemergencia(servicio_id)
    except Exception as e:
        flash(f'Error al cargar servicio: {e}', 'danger')
        return redirect(url_for('servicios'))
    if not servicio:
        flash('Servicio no encontrado.', 'warning')
        return redirect(url_for('servicios'))
    return render_template('servicio_form.html', servicio=servicio)


@app.route('/servicios/editar/<int:servicio_id>', methods=['POST'])
def editar_servicio(servicio_id):
    nombre = request.form.get('nombre')
    tipo = request.form.get('tipo')
    telefono = request.form.get('telefono')
    disponibilidad = request.form.get('disponibilidad')
    direccion = request.form.get('direccion')
    capacidad = request.form.get('capacidad') or None
    horario = request.form.get('horario')
    especialidad = request.form.get('especialidad')
    estado = request.form.get('estado')

    if not nombre or not tipo or not estado:
        flash('Nombre, tipo y estado son obligatorios.', 'warning')
        return redirect(url_for('editar_servicio_form', servicio_id=servicio_id))

    try:
        capacidad_val = int(capacidad) if capacidad else None
        rows = update_servicioemergencia(servicio_id, nombre, tipo, telefono, disponibilidad, direccion, capacidad_val, horario, especialidad, estado)
        flash('Servicio actualizado correctamente.', 'success')
        return redirect(url_for('servicios'))
    except Exception as e:
        flash(f'Error al actualizar servicio: {e}', 'danger')
        return redirect(url_for('editar_servicio_form', servicio_id=servicio_id))


@app.route('/servicios/eliminar/<int:servicio_id>', methods=['POST'])
def eliminar_servicio(servicio_id):
    try:
        rows = delete_servicioemergencia(servicio_id)
        flash('Servicio eliminado.' if rows else 'Servicio no encontrado.', 'info')
    except Exception as e:
        flash(f'Error al eliminar servicio: {e}', 'danger')
    return redirect(url_for('servicios'))


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/usuarios/editar/<int:user_id>', methods=['GET'])
def editar_usuario_form(user_id):
	try:
		user = get_user(user_id)
	except Exception as e:
		flash(f'Error al cargar usuario: {e}', 'danger')
		return redirect(url_for('usuarios'))
	if not user:
		flash('Usuario no encontrado.', 'warning')
		return redirect(url_for('usuarios'))
	return render_template('usuario_form.html', user=user)


@app.route('/usuarios/editar/<int:user_id>', methods=['POST'])
def editar_usuario(user_id):
	cedula = request.form.get('cedula')
	nombre = request.form.get('nombre')
	telefono = request.form.get('telefono')
	contacto = request.form.get('contacto')
	tipo = request.form.get('tipo')
	direccion = request.form.get('direccion')
	email = request.form.get('email')
	fecha = request.form.get('fecha') or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	estado = request.form.get('estado')

	if not nombre or not email:
		flash('Nombre y correo son obligatorios.', 'warning')
		return redirect(url_for('editar_usuario_form', user_id=user_id))

	try:
		rows = update_user(user_id, cedula, nombre, telefono, contacto, tipo, direccion, email, fecha, estado)
		flash('Usuario actualizado correctamente.', 'success')
		return redirect(url_for('usuarios'))
	except Exception as e:
		flash(f'Error al actualizar usuario: {e}', 'danger')
		return redirect(url_for('editar_usuario_form', user_id=user_id))


@app.route('/usuarios/eliminar/<int:user_id>', methods=['POST'])
def eliminar_usuario(user_id):
	try:
		rows = delete_user(user_id)
		flash('Usuario eliminado.' if rows else 'Usuario no encontrado.', 'info')
	except Exception as e:
		flash(f'Error al eliminar usuario: {e}', 'danger')
	return redirect(url_for('usuarios'))


@app.route('/contactos')
def contactos():
	try:
		contactos = get_all_contactoemergencia()
	except Exception as e:
		flash(f"Error al obtener contactos: {e}", 'danger')
		contactos = []
	return render_template('contacto_list.html', contactos=contactos)


@app.route('/contactos/nuevo', methods=['GET'])
def nuevo_contacto_form():
	try:
		tipos = get_all_tipoemergencia()
	except Exception as e:
		flash(f'Error al cargar tipos: {e}', 'danger')
		tipos = []
	return render_template('contacto_form.html', contacto=None, tipos=tipos)


@app.route('/contactos/nuevo', methods=['POST'])
def nuevo_contacto():
	tipo_id = request.form.get('tipo_id')
	nombre = request.form.get('nombre')
	telefono = request.form.get('telefono')
	tipo = request.form.get('tipo')
	descripcion = request.form.get('descripcion')
	estado = request.form.get('estado')

	if not tipo_id or not nombre or not tipo or not estado:
		flash('Tipo, nombre, tipo de contacto y estado son obligatorios.', 'warning')
		return redirect(url_for('nuevo_contacto_form'))

	try:
		tipo_id_val = int(tipo_id)
		new_id = insert_contactoemergencia(tipo_id_val, nombre, telefono, tipo, descripcion, estado)
		flash(f'Contacto creado correctamente (id={new_id}).', 'success')
		return redirect(url_for('contactos'))
	except Exception as e:
		flash(f'Error al crear contacto: {e}', 'danger')
		return redirect(url_for('nuevo_contacto_form'))


@app.route('/contactos/editar/<int:contacto_id>', methods=['GET'])
def editar_contacto_form(contacto_id):
	try:
		contacto = get_contactoemergencia(contacto_id)
		tipos = get_all_tipoemergencia()
	except Exception as e:
		flash(f'Error al cargar datos: {e}', 'danger')
		return redirect(url_for('contactos'))
	if not contacto:
		flash('Contacto no encontrado.', 'warning')
		return redirect(url_for('contactos'))
	return render_template('contacto_form.html', contacto=contacto, tipos=tipos)


@app.route('/contactos/editar/<int:contacto_id>', methods=['POST'])
def editar_contacto(contacto_id):
	tipo_id = request.form.get('tipo_id')
	nombre = request.form.get('nombre')
	telefono = request.form.get('telefono')
	tipo = request.form.get('tipo')
	descripcion = request.form.get('descripcion')
	estado = request.form.get('estado')

	if not tipo_id or not nombre or not tipo or not estado:
		flash('Tipo, nombre, tipo de contacto y estado son obligatorios.', 'warning')
		return redirect(url_for('editar_contacto_form', contacto_id=contacto_id))

	try:
		tipo_id_val = int(tipo_id)
		rows = update_contactoemergencia(contacto_id, tipo_id_val, nombre, telefono, tipo, descripcion, estado)
		flash('Contacto actualizado correctamente.', 'success')
		return redirect(url_for('contactos'))
	except Exception as e:
		flash(f'Error al actualizar contacto: {e}', 'danger')
		return redirect(url_for('editar_contacto_form', contacto_id=contacto_id))


@app.route('/contactos/eliminar/<int:contacto_id>', methods=['POST'])
def eliminar_contacto(contacto_id):
	try:
		rows = delete_contactoemergencia(contacto_id)
		flash('Contacto eliminado.' if rows else 'Contacto no encontrado.', 'info')
	except Exception as e:
		flash(f'Error al eliminar contacto: {e}', 'danger')
	return redirect(url_for('contactos'))


@app.route('/emergencias')
def emergencias():
	try:
		emergencias = get_all_emergencia()
	except Exception as e:
		flash(f"Error al obtener emergencias: {e}", 'danger')
		emergencias = []
	return render_template('emergencia_list.html', emergencias=emergencias)


@app.route('/emergencias/nuevo', methods=['GET'])
def nuevo_emergencia_form():
	try:
		usuarios = get_all_users()
		tipos = get_all_tipoemergencia()
	except Exception as e:
		flash(f'Error al cargar datos: {e}', 'danger')
		usuarios = []
		tipos = []
	return render_template('emergencia_form.html', emergencia=None, usuarios=usuarios, tipos=tipos)


@app.route('/emergencias/nuevo', methods=['POST'])
def nuevo_emergencia():
	usuario_id = request.form.get('tbUsuario_idUsuario')
	tipo_id = request.form.get('tbTipoEmergencia_idTipoEmergencia')
	codigo = request.form.get('codigoEmergencia')
	fecha_hora = request.form.get('fechaHoraEmergencia')
	tipo = request.form.get('tipoEmergencia')
	estado = request.form.get('estadoEmergencia')
	ubicacion = request.form.get('ubicacionEmergencia')
	latitud = request.form.get('latitudEmergencia') or None
	longitud = request.form.get('longitudEmergencia') or None
	descripcion = request.form.get('descripcionEmergencia')
	prioridad = request.form.get('prioridadEmergencia')
	idusuarioreporta = request.form.get('idusuarioreportaEmergencia')
	fecha_cierre = request.form.get('fechaCierreEmergencia') or None
	observaciones = request.form.get('observacionesEmergencia')

	if not usuario_id or not tipo_id or not codigo or not fecha_hora or not estado:
		flash('Usuario, tipo, código, fecha/hora y estado son obligatorios.', 'warning')
		return redirect(url_for('nuevo_emergencia_form'))

	try:
		usuario_id_val = int(usuario_id)
		tipo_id_val = int(tipo_id)
		codigo_val = int(codigo)
		lat_val = float(latitud) if latitud else None
		lon_val = float(longitud) if longitud else None
		new_id = insert_emergencia(usuario_id_val, tipo_id_val, codigo_val, fecha_hora, tipo, estado, ubicacion, lat_val, lon_val, descripcion, prioridad, idusuarioreporta, fecha_cierre, observaciones)
		flash(f'Emergencia creada correctamente (id={new_id}).', 'success')
		return redirect(url_for('emergencias'))
	except Exception as e:
		flash(f'Error al crear emergencia: {e}', 'danger')
		return redirect(url_for('nuevo_emergencia_form'))


@app.route('/emergencias/editar/<int:emergencia_id>', methods=['GET'])
def editar_emergencia_form(emergencia_id):
	try:
		emergencia = get_emergencia(emergencia_id)
		usuarios = get_all_users()
		tipos = get_all_tipoemergencia()
	except Exception as e:
		flash(f'Error al cargar datos: {e}', 'danger')
		return redirect(url_for('emergencias'))
	if not emergencia:
		flash('Emergencia no encontrada.', 'warning')
		return redirect(url_for('emergencias'))
	return render_template('emergencia_form.html', emergencia=emergencia, usuarios=usuarios, tipos=tipos)


@app.route('/emergencias/editar/<int:emergencia_id>', methods=['POST'])
def editar_emergencia(emergencia_id):
	usuario_id = request.form.get('tbUsuario_idUsuario')
	tipo_id = request.form.get('tbTipoEmergencia_idTipoEmergencia')
	codigo = request.form.get('codigoEmergencia')
	fecha_hora = request.form.get('fechaHoraEmergencia')
	tipo = request.form.get('tipoEmergencia')
	estado = request.form.get('estadoEmergencia')
	ubicacion = request.form.get('ubicacionEmergencia')
	latitud = request.form.get('latitudEmergencia') or None
	longitud = request.form.get('longitudEmergencia') or None
	descripcion = request.form.get('descripcionEmergencia')
	prioridad = request.form.get('prioridadEmergencia')
	idusuarioreporta = request.form.get('idusuarioreportaEmergencia')
	fecha_cierre = request.form.get('fechaCierreEmergencia') or None
	observaciones = request.form.get('observacionesEmergencia')

	if not usuario_id or not tipo_id or not codigo or not fecha_hora or not estado:
		flash('Usuario, tipo, código, fecha/hora y estado son obligatorios.', 'warning')
		return redirect(url_for('editar_emergencia_form', emergencia_id=emergencia_id))

	try:
		usuario_id_val = int(usuario_id)
		tipo_id_val = int(tipo_id)
		codigo_val = int(codigo)
		lat_val = float(latitud) if latitud else None
		lon_val = float(longitud) if longitud else None
		rows = update_emergencia(emergencia_id, usuario_id_val, tipo_id_val, codigo_val, fecha_hora, tipo, estado, ubicacion, lat_val, lon_val, descripcion, prioridad, idusuarioreporta, fecha_cierre, observaciones)
		flash('Emergencia actualizada correctamente.', 'success')
		return redirect(url_for('emergencias'))
	except Exception as e:
		flash(f'Error al actualizar emergencia: {e}', 'danger')
		return redirect(url_for('editar_emergencia_form', emergencia_id=emergencia_id))


@app.route('/emergencias/eliminar/<int:emergencia_id>', methods=['POST'])
def eliminar_emergencia(emergencia_id):
	try:
		rows = delete_emergencia(emergencia_id)
		flash('Emergencia eliminada.' if rows else 'Emergencia no encontrada.', 'info')
	except Exception as e:
		flash(f'Error al eliminar emergencia: {e}', 'danger')
	return redirect(url_for('emergencias'))




@app.route('/historialestados')
def historialestados():
	try:
		historialestados = get_all_historialestados()
	except Exception as e:
		flash(f"Error al obtener historial: {e}", 'danger')
		historialestados = []
	return render_template('historialestados_list.html', historialestados=historialestados)


@app.route('/historialestados/nuevo', methods=['GET'])
def nuevo_historialestados_form():
	try:
		emergencias = get_all_emergencia()
		usuarios = get_all_users()
	except Exception as e:
		flash(f'Error al cargar datos: {e}', 'danger')
		emergencias = []
		usuarios = []
	return render_template('historialestados_form.html', historial=None, emergencias=emergencias, usuarios=usuarios)


@app.route('/historialestados/nuevo', methods=['POST'])
def nuevo_historialestados():
	emergencia_id = request.form.get('tbEmergencia_idEmergencia')
	usuario_id = request.form.get('tbUsuario_idUsuario')
	estado_anterior = request.form.get('estadoAnterior')
	estado_nuevo = request.form.get('estadoNuevo')
	fecha_cambio = request.form.get('fechaCambioHistorialEstados')
	usuario_cambio = request.form.get('usuarioCambioHistorialEstados') or None
	motivo = request.form.get('motivoHistorialEstados')

	if not emergencia_id or not usuario_id or not estado_nuevo or not fecha_cambio:
		flash('Emergencia, usuario, estado nuevo y fecha cambio son obligatorios.', 'warning')
		return redirect(url_for('nuevo_historialestados_form'))

	try:
		emergencia_id_val = int(emergencia_id)
		usuario_id_val = int(usuario_id)
		usuario_cambio_val = int(usuario_cambio) if usuario_cambio else None
		new_id = insert_historialestados(emergencia_id_val, usuario_id_val, estado_anterior, estado_nuevo, fecha_cambio, usuario_cambio_val, motivo)
		flash(f'Registro de historial creado correctamente (id={new_id}).', 'success')
		return redirect(url_for('historialestados'))
	except Exception as e:
		flash(f'Error al crear registro: {e}', 'danger')
		return redirect(url_for('nuevo_historialestados_form'))


@app.route('/historialestados/editar/<int:historial_id>', methods=['GET'])
def editar_historialestados_form(historial_id):
	try:
		historial = get_historialestados(historial_id)
		emergencias = get_all_emergencia()
		usuarios = get_all_users()
	except Exception as e:
		flash(f'Error al cargar datos: {e}', 'danger')
		return redirect(url_for('historialestados'))
	if not historial:
		flash('Registro no encontrado.', 'warning')
		return redirect(url_for('historialestados'))
	return render_template('historialestados_form.html', historial=historial, emergencias=emergencias, usuarios=usuarios)


@app.route('/historialestados/editar/<int:historial_id>', methods=['POST'])
def editar_historialestados(historial_id):
	emergencia_id = request.form.get('tbEmergencia_idEmergencia')
	usuario_id = request.form.get('tbUsuario_idUsuario')
	estado_anterior = request.form.get('estadoAnterior')
	estado_nuevo = request.form.get('estadoNuevo')
	fecha_cambio = request.form.get('fechaCambioHistorialEstados')
	usuario_cambio = request.form.get('usuarioCambioHistorialEstados') or None
	motivo = request.form.get('motivoHistorialEstados')

	if not emergencia_id or not usuario_id or not estado_nuevo or not fecha_cambio:
		flash('Emergencia, usuario, estado nuevo y fecha cambio son obligatorios.', 'warning')
		return redirect(url_for('editar_historialestados_form', historial_id=historial_id))

	try:
		emergencia_id_val = int(emergencia_id)
		usuario_id_val = int(usuario_id)
		usuario_cambio_val = int(usuario_cambio) if usuario_cambio else None
		rows = update_historialestados(historial_id, emergencia_id_val, usuario_id_val, estado_anterior, estado_nuevo, fecha_cambio, usuario_cambio_val, motivo)
		flash('Registro actualizado correctamente.', 'success')
		return redirect(url_for('historialestados'))
	except Exception as e:
		flash(f'Error al actualizar registro: {e}', 'danger')
		return redirect(url_for('editar_historialestados_form', historial_id=historial_id))


@app.route('/historialestados/eliminar/<int:historial_id>', methods=['POST'])
def eliminar_historialestados(historial_id):
	try:
		rows = delete_historialestados(historial_id)
		flash('Registro eliminado.' if rows else 'Registro no encontrado.', 'info')
	except Exception as e:
		flash(f'Error al eliminar registro: {e}', 'danger')
	return redirect(url_for('historialestados'))


# ==================== RUTAS PARA DESPACHO ====================

@app.route('/despacho')
def despacho():
	try:
		despachos = get_all_despacho()
		return render_template('despacho_list.html', despachos=despachos)
	except Exception as e:
		flash(f'Error al obtener despachos: {e}', 'danger')
		return redirect(url_for('admin'))


@app.route('/despacho/nuevo', methods=['GET'])
def nuevo_despacho_form():
	try:
		servicios = get_all_servicioemergencia()
		emergencias = get_all_emergencia()
		return render_template('despacho_form.html', servicios=servicios, emergencias=emergencias)
	except Exception as e:
		flash(f'Error al cargar formulario: {e}', 'danger')
		return redirect(url_for('despacho'))


@app.route('/despacho/nuevo', methods=['POST'])
def nuevo_despacho():
	try:
		servicio_id = request.form.get('tbServicioEmergencia_idServicioEmergencia')
		emergencia_id = request.form.get('tbEmergencia_idEmergencia')
		id_servicio = request.form.get('idServicio')
		hora_asignacion = request.form.get('horaAsignacionDespacho')
		hora_llegada = request.form.get('horaLlegadaDespacho')
		hora_finalizacion = request.form.get('horaFinalizacionDespacho')
		estado = request.form.get('estadoDespacho')
		observaciones = request.form.get('observacionesDespacho')
		tiempo_respuesta = request.form.get('tiempoRespuestaDespacho')
		calificacion = request.form.get('calificacionDespacho')
		
		servicio_id_val = int(servicio_id) if servicio_id else None
		emergencia_id_val = int(emergencia_id) if emergencia_id else None
		id_servicio_val = int(id_servicio) if id_servicio else None
		tiempo_respuesta_val = int(tiempo_respuesta) if tiempo_respuesta else None
		calificacion_val = int(calificacion) if calificacion else None
		
		insert_despacho(servicio_id_val, emergencia_id_val, id_servicio_val, hora_asignacion, hora_llegada, hora_finalizacion, estado, observaciones, tiempo_respuesta_val, calificacion_val)
		flash('Despacho creado correctamente.', 'success')
		return redirect(url_for('despacho'))
	except Exception as e:
		flash(f'Error al crear despacho: {e}', 'danger')
		return redirect(url_for('nuevo_despacho_form'))


@app.route('/despacho/editar/<int:despacho_id>', methods=['GET'])
def editar_despacho_form(despacho_id):
	try:
		despacho_data = get_despacho(despacho_id)
		if not despacho_data:
			flash('Despacho no encontrado.', 'warning')
			return redirect(url_for('despacho'))
		servicios = get_all_servicioemergencia()
		emergencias = get_all_emergencia()
		return render_template('despacho_form.html', despacho=despacho_data, servicios=servicios, emergencias=emergencias)
	except Exception as e:
		flash(f'Error al cargar formulario: {e}', 'danger')
		return redirect(url_for('despacho'))


@app.route('/despacho/editar/<int:despacho_id>', methods=['POST'])
def editar_despacho(despacho_id):
	try:
		servicio_id = request.form.get('tbServicioEmergencia_idServicioEmergencia')
		emergencia_id = request.form.get('tbEmergencia_idEmergencia')
		id_servicio = request.form.get('idServicio')
		hora_asignacion = request.form.get('horaAsignacionDespacho')
		hora_llegada = request.form.get('horaLlegadaDespacho')
		hora_finalizacion = request.form.get('horaFinalizacionDespacho')
		estado = request.form.get('estadoDespacho')
		observaciones = request.form.get('observacionesDespacho')
		tiempo_respuesta = request.form.get('tiempoRespuestaDespacho')
		calificacion = request.form.get('calificacionDespacho')
		
		servicio_id_val = int(servicio_id) if servicio_id else None
		emergencia_id_val = int(emergencia_id) if emergencia_id else None
		id_servicio_val = int(id_servicio) if id_servicio else None
		tiempo_respuesta_val = int(tiempo_respuesta) if tiempo_respuesta else None
		calificacion_val = int(calificacion) if calificacion else None
		
		rows = update_despacho(despacho_id, servicio_id_val, emergencia_id_val, id_servicio_val, hora_asignacion, hora_llegada, hora_finalizacion, estado, observaciones, tiempo_respuesta_val, calificacion_val)
		flash('Despacho actualizado correctamente.', 'success')
		return redirect(url_for('despacho'))
	except Exception as e:
		flash(f'Error al actualizar despacho: {e}', 'danger')
		return redirect(url_for('editar_despacho_form', despacho_id=despacho_id))


@app.route('/despacho/eliminar/<int:despacho_id>', methods=['POST'])
def eliminar_despacho(despacho_id):
	try:
		rows = delete_despacho(despacho_id)
		flash('Despacho eliminado.' if rows else 'Despacho no encontrado.', 'info')
	except Exception as e:
		flash(f'Error al eliminar despacho: {e}', 'danger')
	return redirect(url_for('despacho'))


# ==================== RUTAS DE USUARIO - LOGIN Y REGISTRO ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')
		
		try:
			user = authenticate_user(email, password)
			if user:
				session['user_id'] = user['idUsuario']
				session['user_name'] = user['nombresApellidosUsuario']
				flash(f"¡Bienvenido, {user['nombresApellidosUsuario']}!", 'success')
				return redirect(url_for('index'))
			else:
				flash('Correo o contraseña incorrectos.', 'danger')
		except Exception as e:
			flash(f'Error en el login: {e}', 'danger')
	
	return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
	if request.method == 'POST':
		cedula = request.form.get('cedula')
		nombres_apellidos = request.form.get('nombres_apellidos')
		email = request.form.get('email')
		telefono = request.form.get('telefono')
		direccion = request.form.get('direccion')
		password = request.form.get('password')
		confirm_password = request.form.get('confirm_password')
		
		if password != confirm_password:
			flash('Las contraseñas no coinciden.', 'danger')
			return render_template('registro.html')
		
		try:
			user_id = register_user(cedula, nombres_apellidos, email, telefono, direccion, password)
			flash('¡Cuenta creada correctamente! Ahora puedes iniciar sesión.', 'success')
			return redirect(url_for('login'))
		except ValueError as e:
			flash(f'Error: {e}', 'danger')
		except Exception as e:
			flash(f'Error al registrar usuario: {e}', 'danger')
	
	return render_template('registro.html')


@app.route('/logout', methods=['POST'])
def logout():
	session.clear()
	flash('Has cerrado sesión correctamente.', 'info')
	return redirect(url_for('index'))


# ==================== RUTAS DE SOLICITUD DE AYUDA ====================

@app.route('/solicitar-ayuda')
def solicitar_ayuda():
	try:
		servicios = get_all_servicioemergencia()
		return render_template('solicitar_ayuda.html', servicios=servicios)
	except Exception as e:
		flash(f'Error al obtener servicios: {e}', 'danger')
		return redirect(url_for('index'))


@app.route('/formulario-ayuda/<int:servicio_id>', methods=['GET', 'POST'])
def formulario_ayuda(servicio_id):
	try:
		servicio = get_servicioemergencia(servicio_id)
		
		if not servicio:
			flash('Servicio no encontrado.', 'danger')
			return redirect(url_for('solicitar_ayuda'))
		
		if request.method == 'POST':
			nombre = request.form.get('nombre')
			telefono = request.form.get('telefono')
			ubicacion = request.form.get('ubicacion')
			grupo_sanguineo = request.form.get('grupo_sanguineo')
			descripcion = request.form.get('descripcion', '')
			
			try:
				# Obtener o crear usuario anónimo
				user_id = None
				if 'user_id' in session:
					user_id = session['user_id']
				
				# Crear emergencia
				tipo_emergencia_id = servicio['idServicioEmergencia']
				emergencia_id = insert_emergencia(
					user_id=user_id or 1,
					tipo_emergencia_id=tipo_emergencia_id,
					codigo_emergencia=None,
					fecha_hora=datetime.now(),
					tipo_emergencia=None,
					estado='reportada',
					ubicacion=ubicacion,
					latitud=None,
					longitud=None,
					descripcion=f"Solicitud: {descripcion}\nContacto: {nombre} ({telefono})\nGrupo Sanguíneo: {grupo_sanguineo}",
					prioridad='media',
					usuario_reporta=user_id or 1,
					fecha_cierre=None,
					observaciones=f"Solicitante: {nombre}\nTeléfono: {telefono}\nGrupo Sanguíneo: {grupo_sanguineo}"
				)
				
				flash('¡Solicitud de ayuda enviada correctamente! Los servicios de emergencia han sido notificados.', 'success')
				return redirect(url_for('index'))
			except Exception as e:
				flash(f'Error al enviar solicitud: {e}', 'danger')
		
		return render_template('formulario_ayuda.html', servicio=servicio)
	except Exception as e:
		flash(f'Error: {e}', 'danger')
		return redirect(url_for('solicitar_ayuda'))


if __name__ == '__main__':
	app.run(debug=True, port=5000)