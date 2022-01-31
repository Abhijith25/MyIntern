from flask import Flask, render_template, jsonify,request
from flask.helpers import make_response
from flask_cors.decorator import cross_origin
from flask_cors.extension import CORS
from flaskext.mysql import MySQL

import pymysql

app = Flask(__name__)
CORS(app)

# MySQL configurations
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'users'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



@app.route('/register',methods=['POST', 'GET'])
@cross_origin()
def register():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        # Check if user already registered
        cursor.execute('SELECT * FROM useraccounts where email=%s', (email))
        acc = cursor.fetchone()
        
        if acc:
            data = {'username': str(username), 'status': 'User Already exists'}
            return make_response(jsonify(data), 403)
        else:
            cursor.execute('INSERT INTO useraccounts VALUES (NULL, %s, %s, %s)', (username, email, password))
            conn.commit()
            data = {'username':str(username),'status':'success'}
            return make_response(jsonify(data), 200)


@app.route('/login', methods=['POST', 'GET'])
def login():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        usr = request.json['usrmail']
        password = request.json['password']

        cursor.execute('select * from useraccounts where username = %s and password= %s OR email = %s and password=%s', (usr,password,usr,password))
        acc = cursor.fetchone()
        print(acc)

        if acc:
            data = {'username':acc['username'], 'status': 'success'}
            return make_response(jsonify(data), 200)
        else:
            data = {'username':str(usr), 'status': 'Incorrect Username/Password'}
            return make_response(jsonify(data), 403)
            
@app.route('/getPosts', methods=['GET'])
def getPosts():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM posts')
    post_data = cursor.fetchall()
    print(post_data)
    if post_data:
        return jsonify(post_data)
    return make_response(jsonify({'status':'No Posts found'}), 400)


@app.route('/addPosts', methods=['POST', 'GET'])
def addPosts():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        post_title = request.json['post_title']
        post_author = request.json['post_author']
        post_content = request.json['post_content']
        cursor.execute('insert into posts values(NULL, %s, %s, %s, current_timestamp())', (post_title, post_author, post_content))
        conn.commit()
        data = {'title':str(post_title),'status':'success'}
        return make_response(jsonify(data), 200)



if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True, port=5000)