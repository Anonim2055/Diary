from pymongo import MongoClient
from flask import Flask, request, jsonify, render_template, redirect
from imgur_api import upload as img_up
import requests
import json
import datetime
from my_time import get_current_timestamp as get_time

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

    return render_template('home.html')

@app.route("/login", methods=['POST','GET'])
def log():

    return render_template("login.html")


@app.route("/signup", methods=['POST','GET'])
def home():

    # Render the index.html template
    return render_template("signup.html")
# @app.route('/index.html',methods=['GET'])
#     def indexx()







@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    response = img_up(file)
    # print(response)

    upload_time = get_time()
    try:
        db.images.insert_one({
        "img_url": response['img_url'],
        "timestamp": upload_time
    })
    except Exception:

        return '', 503

    return jsonify(response['status'])




@app.route('/upload',methods=['GET'])
def uf():
    return render_template('up.html'), 200


@app.route('/users', methods=['GET'])
def utest():
    istrue = request.args.get("istrue")
    # check if istrue is true
    if istrue == "true":

        return "this is true", 200
    elif istrue == "false" :

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



@app.route('/form-example', methods=['POST'])
def form_example():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
    user = dict({'name': name, 'email': email, 'password' : password})
    url = 'http://127.0.0.1:5000/users'
    nuser = json.dumps(user)
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, data=nuser, headers=headers)
    #return response
    return f'Hello {name}, your email is {email}, your pass is{password}'


@app.route('/error')
def always_return_500():
    # return status code 500
    return '', 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/get_images", methods=['GET'])
def get_image_url():
    user_id = request.args.get("user_id")

    # Поиск всех документов с заданным user_id
    user_data_cursor = db.images.find({"user_id": user_id})

    user_data_list = []

    # Проходим по каждому документу и добавляем его в список
    for user_data in user_data_cursor:
        img_url = user_data.get("img_url", "URL not available")
        created_at_timestamp = user_data.get("timestamp", None)
        created_at = None
        if created_at_timestamp:
            created_at = datetime.datetime.fromtimestamp(created_at_timestamp).strftime('%Y-%m-%d %H:%M:%S')

        user_data_list.append({
            "user_id": user_id,
            "img_url": img_url,
            "created_at": created_at
        })

    if user_data_list:
        return (user_data_list)
    else:
        return jsonify({"message": "User ID not found"}), 200

    #except Exception as e:
        #return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

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
