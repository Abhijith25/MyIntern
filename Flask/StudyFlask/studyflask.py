from flask import Flask, render_template, url_for, redirect
from flask.helpers import flash
from flaskext.mysql import MySQL
import pymysql
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'users'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


# configuring a secret key to avoid and prevent modification of cookies and other security
# to do that open python interpreter import secrets
# secrets.token_hex(16) - would give you a 16 digit hex key as token
# paste it here

app.config['SECRET_KEY'] = '9a741fee812944734d18f2803a33b609'

# Creating posts

posts = [

    {
        'author':'Abhijith',
        'title':'My First Flask Project',
        'content':'This is my first Flask Project',
        'date_posted':'January 07, 2022'
    },

     {
        'author':'VSA',
        'title':'My First Post in the Project',
        'content':'This is my first post in the Flask Project',
        'date_posted':'January 08, 2022'
    }





]


# default home page on opening the web application
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts = posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    # on successful validation display an alert in flask called flash and the category that is a string that is given as success
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
        # also set it in such a way that all flash messages also gets displayed in other pages also.
        # refer layout.html for that
    return render_template('register.html', title='Connect with Us', form = form)

@app.route('/login', methods=['GET','POST'])
def login():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@studyflask.com' and form.password.data == 'abhi_441':
            flash('Login successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed!! Check email and password', 'danger')
    return render_template('login.html', title='Hop In', form = form)

if __name__ == '__main__':
    app.run(debug=True)