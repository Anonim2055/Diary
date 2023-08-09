from pymongo import MongoClient
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

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
    resp=jsonify({
        "message":"Flask run"
    })
    return resp
@app.route("/login",methods=['POST','GET'])
def log():
    return render_template("login.html")
@app.route("/signUp",methods=['POST','GET'])
def home():
    # Render the index.html template
    return render_template("signup.html")
# @app.route('/index.html',methods=['GET'])
#     def indexx()
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
