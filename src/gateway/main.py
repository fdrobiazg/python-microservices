import ssl
import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate, access
from utils import storage

app = Flask(__name__)
app.config["Mongo_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app, uri="mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.8.2")

gfs = gridfs.GridFS(mongo.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel

@app.route("/login", methods=["POST"])
def login():
    jwt, err = access.login(request)

    if not err:
        return jwt
    else:
        return err

@app.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)

    access = json.loads(access)

    if access["admin"]:
        if len(request.files) != 1:
            return "Incorrect number of files - exactly 1 file is required.", 400
        
        _, file = request.files.items()
        err = storage.upload(file, gfs, channel, access)

        if err:
            return err
        
        return "File uploaded successfuly.", 200
    else:
        return "Authorization failed.", 401
    
@app.route("/download", methods=["GET"])
def download():
    pass

@app.route("/health", methods=["GET"])
def health():
    return "Healthy.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)