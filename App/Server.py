from pymongo import MongoClient
from flask import Flask, request, jsonify, render_template
import requests
app = Flask(__name__)
# with open('cid', 'r') as t_id:
#     cid = str(t_id.read())

try:
#check if mongoDB work
    mongo=MongoClient(host="localhost",port=27017, serverSelectionTimeoutMs=5000)
    db = mongo.flask
    print("Mongo Connect")
except Exception:
    print("Unable")

@app.route('/home',methods=['GET'])
def hom():
    return render_template("home.html")

@app.route('/',methods=['GET'])
def index():
    resp = jsonify({
        "message":"Flask run"
    })
    return resp

@app.route("/login",methods=['POST','GET'])
def log():
    return render_template("login.html")


@app.route("/signup",methods=['POST','GET'])
def home():
    # Render the index.html template
    return render_template("signup.html")
# @app.route('/index.html',methods=['GET'])
#     def indexx()









@app.route('/upload', methods=['POST'])
def upload_file():
    with open('cid', 'r') as t_id:
        cid = str(t_id.read())
    headers = {'Authorization': f'Client-ID {cid}'}
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    response = requests.post('https://api.imgur.com/3/image', headers=headers, files={'image': file})
    
    
    if response.status_code == 200:
        imgur_response = response.json()
        img_url = imgur_response['data']['link']
        return jsonify({'message': 'Image uploaded successfully', 'image_url': img_url}), 200
    else:
        print("Image upload failed. Status code:", response.status_code)
        return jsonify({'error': 'Image upload failed'}), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

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
        "email":body["email"],
        "name": body["name"],
        "password": body["password"]
    })
    resp = jsonify({
        "id": str(result.inserted_id),
        "message": "user added"
    })
    return resp




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