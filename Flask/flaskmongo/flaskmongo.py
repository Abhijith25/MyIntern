from tabnanny import check
from flask import Flask, jsonify, json, make_response, request
from flask_pymongo import PyMongo
import json_util
from datetime import datetime
import pytz
from bson import ObjectId

app = Flask(__name__)

mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/users")
db = mongodb_client.db

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        usr = request.json['usrmail']
        password = request.json['password']
        user_data = db.useraccounts.find_one({"$or": [{'username': usr},{'email': usr}]})
        # user_data = db.useraccounts.find_one({"$and":[{'username': usr}, {'password': password}]})
        # user_data = db.useraccounts.find_one({"$and": [{"$or": [{'username': usr},{'email': usr}]},{'password': "hello_abhi"}]})
        if user_data:
            username = user_data['username']
            password_check = user_data['password']
            if(password_check == password):
                return jsonify({"username": username, "status": "success"})
            else:
                return jsonify({"username": username, "status": "Incorrect password"})
        else:
            return jsonify({"username": str(usr), "status": "User does not exist"})
    
    response = "hello"
    # for user in user_data:
    #     id = str(user['_id'])
    #     del user['_id']
    #     user["_id"] = id
        
    #     response.append(user)
    # print(response)
    return jsonify(response)

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        user_data = db.useraccounts.find_one({"username": username})
        if user_data:
            user_email = user_data['email']
            return jsonify({'email': user_email, 'status': 'Already part of the family'})
        else:
            db.useraccounts.insert_one({"username": username, "email": email, "password": password})
            check_success = db.useraccounts.find_one({"email": email})
            if check_success:
                return jsonify({'username': check_success['username'], 'status': "Success"})
    return "Not a POST request"

@app.route('/getPosts', methods=['GET'])
def getPosts():
    
    post_data = db.posts.find()
    get_data=[]
    for post in post_data:
        date_time = post['date_posted']
        asia_tz = pytz.timezone('Asia/Kolkata')
        crct_datetime = date_time.astimezone(asia_tz)
        # post["_id"] =  str(post["_id"])
        id = str(post["_id"])
        del post['_id']
        del post['date_posted']
        post['_id'] = id
        post['date_posted'] = crct_datetime
        get_data.append(post)
        print("Date time: ",date_time)
        print("Correct date time: ",crct_datetime)


    return jsonify(get_data)

@app.route('/deletePost', methods=['POST', 'GET'])
def deletePost():
    if request.method == 'POST':
        post_id = request.json['post_id']
        obj_post_id = ObjectId(post_id)
        db.posts.delete_one({"_id": obj_post_id})
        chk_delete = db.posts.find_one({"_id": obj_post_id})
        if not chk_delete:
            return make_response(jsonify({'status':"success"}), 200)
        else:
            return make_response(jsonify({'status': 'Failed'}), 403)

@app.route('/addPosts', methods=['POST', 'GET'])
def addPosts():
    if request.method == 'POST':
        post_title = request.json['post_title']
        post_author = request.json['post_author']
        post_content = request.json['post_content']
        db.posts.insert_one(
            {
                "title": post_title,
                "author": post_author,
                "content": post_content,
                "date_posted": datetime.now()
            }
        )
        return jsonify({'status': 'success'})
    return "NOT a POST call"




if __name__ == '__main__':
    app.run(port=5000, debug=True)