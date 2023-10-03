import bcrypt
from pymongo import MongoClient
from flask import Flask, request, jsonify, render_template, redirect, session

from imgur_api import upload as img_up
import requests
import json
import datetime
from get_timestamp import get_current_timestamp as get_time

app = Flask(__name__)
# with open('cid', 'r') as t_id:
#     cid = str(t_id.read())
# dbkeys = open("mdb", "r").readlines()
# #dbhost = dbkeys[0].split(':')[1]
# dbport = int(dbkeys[1].split(':')[1])
# dbhost = dbkeys[0][dbkeys[0].index(":")+1:-1]
# print ("dbport:","lol","dbhost:",dbhost)
try:
#check if mongoDB work
    mongo = MongoClient(host='localhost', port=27017, serverSelectionTimeoutMs=5000)
    db = mongo.diary
    print("Mongo Connect")
except Exception:
    print("Unable")

@app.route('/home', methods=['GET'])
def hom():
    return redirect('/')

@app.route('/', methods=['GET'])
def index():
    try:
        username = session['username']
    except Exception:
        username = None

    return render_template('home.html', username=username)

@app.route("/login", methods=['POST','GET'])
def log():
    if request.method == 'POST':
        users = db.users
        login_user = users.find_one({'name': request.form['username']})
        print("login_user")
        if login_user:
            print('login_user')
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = request.form['username']
                return redirect('home')
    return render_template("login.html")


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({
                'name': request.form['username'],
                'password': hashpass
            })
            session['username'] = request.form['username']
            return redirect('home')

        return 'That username already exists!'

    # Render the index.html template
    return render_template("signup.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    try :
        user_id = session['username']
        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        response = img_up(file)
    #print(response)
        page = str("/desc?img_url="+response['img_url'])
        return redirect(page)
    except Exception:
        redirect('/')
    #return jsonify(response['status'])

@app.route('/upload', methods=['GET'])
def uf():
    try :
        user_id = session['username']
        #user_id = request.args.get("user_id")
        # if user_id == None:
        #     return redirect('/')
        return render_template('up.html', user_id=user_id)
    except Exception:
        return redirect('/')

@app.route('/desc', methods=['GET'])
def desc_get():
    try:
        user_id = session['username']
        img_url = request.args.get('img_url')
        return render_template("description.html", user_id=user_id, img_url=img_url)
    except Exception:
        return redirect('/')

@app.route('/desc', methods=['POST'])
def desc_load():
    try:
        user_id = session['username']
        description = request.form.get("description")

        img_url = request.form.get("img_url")
        upload_time = get_time()
        try:
            db.images.insert_one({
            "img_url": img_url,
            "timestamp": upload_time,
            "user_id": user_id,
            "description": description
        })
        except Exception:

            return '', 503
        page = str("user_photos/" + user_id)
        return redirect(page)
    except Exception:
        redirect('/')




@app.route('/users', methods=['GET'])
def utest():
    istrue = request.args.get("istrue")
    # check if istrue is true
    if istrue == "true":

        return "this is true", 200
    elif istrue == "false":

        return "this is  not true", 200
    else:

        return "Didn't get param", 200

@app.route('/users',methods=['POST'])
def add_user():
    body = request.json
    required_keys = {"name", "email", "password"}
    # check if there's any invalid key in the request body
    if set(body.keys()) != required_keys:
        return jsonify({"error": "Invalid or missing field in request body"}), 400
        # return error message with 400 status code

    result = db.users.insert_one({
        "email": body["email"],
        "name": body["name"],
        "password": body["password"]
    })
    resp = jsonify({
        "id": str(result.inserted_id),
        "message": "user added"
    })
    return resp


@app.route('/test', methods=['GET'])
def sUp():
    return render_template('signup_post_test.html')



#

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


#@app.route("/get_images", methods=['GET'])
def get_image_url(user_id=None):
    us_id2 = user_id
    user_id = request.args.get("user_id")
    if user_id == None:
        user_id = us_id2
    # search every 'user id'
    user_data_cursor = db.images.find({"user_id": user_id})
    user_data_list = []
    # add everything to list
    for user_data in user_data_cursor:
        img_url = user_data.get("img_url", "URL not available")
        created_at_timestamp = user_data.get("timestamp", None)
        created_at = None
        description = user_data.get('description', None)
        if created_at_timestamp:
            created_at = datetime.datetime.fromtimestamp(created_at_timestamp).strftime('%Y-%m-%d')

        user_data_list.append({
            "user_id": user_id,
            "img_url": img_url,
            "created_at": created_at,
            "description": description
        })
    print(user_data_list)
    if user_data_list:
        print(user_data_list)
        return user_data_list
    else:
        print('bad')
        return ({"message": "User ID not found"}), 200

    #except Exception as e:
        #return jsonify({"error": str(e)}), 500

@app.route("/user_photos/<user_id>", methods=['GET'])
def user_photos(user_id):
    #print(user_id)
    try:
        if user_id == session['username']:

            data = (get_image_url(user_id))
            print('_____________')
            print(data)
            print('_____________')
            return render_template("photos.html", photos=data)
        else:
            page="/user_photos/"+session['username']
            return redirect(page)
    except Exception:
        return redirect('/')

if __name__ == "__main__":
    app.secret_key = 'mysecret'
    app.run(host='localhost', debug=True)





#@app.route('/form-example', methods=['POST'])
# def form_example():
#     email = request.form.get('email')
#     password = request.form.get('password')
#     name = request.form.get('name')
#     user = dict({'name': name, 'email': email, 'password' : password})
#     url = 'http://127.0.0.1:5000/users'
#     nuser = json.dumps(user)
#     headers = {
#         "Content-Type": "application/json"
#     }
#     response = requests.post(url, data=nuser, headers=headers)
#     #return response
#     return f'Hello {name}, your email is {email}, your pass is{password}'


# def imgur(file):
#     client_id=cid
#     headers = {'Authorization': f'Client-ID {client_id}'}
#     response = request.post('https://api.imgur.com/3/image', headers=headers, files=file)

#     if response.status_code == 200:
#         # Successfully uploaded the image
#         imgur_response = response.json()
#         img_url = imgur_response['data']['link']
#         return img_url
#     else:
#         # Failed to upload the image
#         print("Image upload failed. Status code:", response.status_code)
#         return None
