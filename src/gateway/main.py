import ssl
import os, gridfs, pika, json
from flask import Flask, request
# from flask_pymongo import PyMongo
from pymongo import MongoClient
from auth import validate, access
from utils import storage

MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_URI = os.environ.get("MONGO_URI")
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")

app = Flask(__name__)

mongo = MongoClient(MONGO_URI,
                    username=MONGO_USER, 
                    password=MONGO_PASSWORD,
                    authSource='admin')

src_gfs = gridfs.GridFS(mongo['src_img'])
out_gfs = gridfs.GridFS(mongo['processed_img'])

connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()

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
        
        file = request.files['file']
        app.logger.info(f"File: {file}\n\n, Type:{type(file)}")
        err = storage.upload(file, src_gfs, channel, access)

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
    app.run(host="0.0.0.0", port=8000, debug=True)