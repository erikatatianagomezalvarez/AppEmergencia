import os
from flask import Flask, render_template, request, redirect, url_for, flash

from db import (
	get_all_users,
	insert_user,
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
)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', 'dev-secret')


@app.route('/')
def index():
	return redirect(url_for('tipos'))


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
	return render_template('usuario_form.html')


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


if __name__ == '__main__':
	app.run(debug=True, port=5000)