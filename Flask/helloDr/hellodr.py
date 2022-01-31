from flask import Flask, request, flash, session, url_for
from flask.templating import render_template
from flaskext.mysql import MySQL
from flask_cors import CORS, cross_origin
import pymysql
import mysql.connector
from mysql.connector.errorcode import ER_MAXVALUE_IN_VALUES_IN
from werkzeug.utils import redirect
import re
import os



app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)

mysql = MySQL()
   
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'hellodr'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/index')
@app.route('/home')
@app.route('/')
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/doctors')
def doctors():
    if 'loggedin' in session:
        return render_template('doctors.html')
    return render_template('logindr.html')

    

@app.route('/patients')
def patients():
    if 'loggedin' in session:
    # User is loggedin show them the home page
        return render_template('patients.html', name=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('loginpt'))


@app.route('/logindr', methods=['POST', 'GET'])
def logindr():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor.execute('SELECT * FROM doctors WHERE email = %s AND password = %s', (email, password))
        draccount = cursor.fetchone()
        if draccount:
            session['loggedin'] = True
            session['id'] = draccount['id']
            session['username'] = draccount['name']
            flash('Welcome doctor ♥', 'success')
            return redirect(url_for('doctors'))
        else:
            msg = 'Incorrect username or password'
            flash('Incorrect username or password!!', 'danger')
            return redirect("url_for('logindr')")

    return render_template('logindr.html')

@app.route('/loginpt', methods=['POST','GET'])
def loginpt():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form.get('email')
        password = request.form.get('password')
        cursor.execute('SELECT * FROM patients WHERE email = %s AND password = %s', (email, password))
        ptaccount = cursor.fetchone()
        if ptaccount:
            session['loggedin'] = True
            session['id'] = ptaccount['id']
            session['username'] = ptaccount['name']
            flash('Welcome doctor ♥', 'success')
            return redirect(url_for('patients'))
        else:
            msg = 'Incorrect username or password'
            flash('Incorrect username or password!!', 'danger')
            return redirect(url_for('loginpt'))
    return render_template('loginpt.html')

@app.route('/registerdr', methods=['POST','GET'])
def registerdr():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST'and 'email' in request.form and 'password' in request.form:

        
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        department = request.form['department']

        cursor.execute('SELECT * FROM doctors WHERE email = %s', (email))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
            flash('You are already part of the family doctor ♥', 'info')
            return redirect(url_for('home'))
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not name or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO doctors VALUES (NULL, %s, %s, %s, %s)', (name, email, password, department)) 
            conn.commit()
            flash('Welcome to the family doctor ♥', 'success')
            msg = 'Hello Dr, You have successfully registered!'
            return redirect(url_for('doctors'))
    return render_template('registerdr.html')

@app.route('/registerpt', methods=['POST','GET'])
def registerpt():
   # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST'and 'email' in request.form and 'password' in request.form:

        
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']

        cursor.execute('SELECT * FROM patients WHERE email = %s', (email))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
            flash('You are already part of the family ♥', 'info')
            return redirect(url_for('home'))
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not name or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO patients VALUES (NULL, %s, %s, %s, %s)', (name, age, email, password)) 
            conn.commit()
            flash('Welcome to the family ♥', 'success')
            msg = 'Hello Dr, You have successfully registered!'
            return redirect(url_for('patients'))
    return render_template('registerpt.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('name', None)
   # Redirect to login page
   return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
