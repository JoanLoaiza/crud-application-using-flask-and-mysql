
from flask import Flask, flash, render_template, redirect, url_for, request, session
from module.database import Database
import re
import json

app = Flask(__name__)
app.secret_key = "abc123456"
db = Database()


@app.route('/')
@app.route('/contactos/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        data = db.login(username, password)
        if data != ():
            session['loggedin'] = True
            session['username'] = username
            return redirect(url_for('home'))
        elif username == "admin" and password == "admin":
            return redirect(url_for('home'))
        else:
            flash("Usuario/contraseña incorrecta...!", "danger")
    return render_template('auth/login.html')


@app.route('/contactos/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if db.validate_if_account_exists(username, email):
            flash("La cuenta ya existe!", "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Email incorrecto!", "danger")
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash(
                "El nombre de usuario debe contener sólo caracteres y números!", "danger")
        elif not username or not password or not email:
            flash("Nombre de usuario/contraseña incorrectos!", "danger")
        elif db.register(username, email, password):
            flash("Se ha registrado con éxito!", "success")
            return redirect(url_for('login'))

    elif request.method == 'POST':
        flash("Por favor, rellene el formulario!", "danger")
    return render_template('auth/register.html', title="Registro")


@app.route('/contactos')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/contactos/home')
def home():
    if 'loggedin' in session:
        username = ""
        if session['username'] != "":
            if session['username'] == "admin":
                username = "Administrador"
            else:
                username = session['username']
            data = db.read(None)
            return render_template('home/home.html', username=username, data=data, title="Home")
    return redirect(url_for('login'))


@app.route('/contactos/profile')
def profile():
    if 'loggedin' in session:
        if session['username'] != "":
            username = session['username']
            return render_template('auth/profile.html', username=username, title="Perfil")
    return redirect(url_for('login'))


@app.route('/add/')
def add():
    return render_template('home/add.html')


@app.route('/addphone', methods=['POST', 'GET'])
def addphone():
    if request.method == 'POST' and request.form['save']:
        if db.insert(request.form, id):
            flash("Se ha añadido un nuevo número de teléfono")
        else:
            flash("Ha ocurrido un error al añadir el número de teléfono")

        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.route('/update/<int:id>/')
def update(id):
    data = db.read(id)

    if len(data) == 0:
        return redirect(url_for('home'))
    else:
        session['update'] = id
        return render_template('home/update.html', data=data)


@app.route('/updatephone', methods=['POST'])
def updatephone():
    if request.method == 'POST' and request.form['update']:

        if db.update(session['update'], request.form):
            flash('Se ha actualizado el número de teléfono')

        else:
            flash('Ha ocurrido un error al actualizar el número de teléfono')

        session.pop('update', None)

        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.route('/delete/<int:id>/')
def delete(id):
    data = db.read(id)

    if len(data) == 0:
        return redirect(url_for('home'))
    else:
        session['delete'] = id
        return render_template('home/delete.html', data=data)


@app.route('/deletephone', methods=['POST'])
def deletephone():
    if request.method == 'POST' and request.form['delete']:

        if db.delete(session['delete']):
            flash('Se ha eliminado el número de teléfono')

        else:
            flash('Ha ocurrido un error al eliminar el número de teléfono')

        session.pop('delete', None)

        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('include/error.html')


if __name__ == '__main__':
    app.run(debug=True)
