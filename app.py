import os
from flask import Flask, render_template, request, redirect, url_for, flash

from db import get_all_users, insert_user

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', 'dev-secret')


@app.route('/')
def index():
	return redirect(url_for('usuarios'))


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