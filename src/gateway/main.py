import ssl
import os, gridfs, pika, json
from flask import Flask, request, send_file
# from flask_pymongo import PyMongo
from pymongo import MongoClient
from auth import validate, access
from utils import storage
from bson.objectid import ObjectId

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
        err = storage.upload(file, src_gfs, channel, access)

        if err:
            return err
        
        return "File uploaded successfuly.", 200
    else:
        return "Authorization failed.", 401
    
@app.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request)

    if err:
        return err
    
    access = json.loads(access)

    if access["admin"]:
        fid = request.args.get("fid")

        if not fid:
            return "Fid is required.", 400
        
        try:
            out = out_gfs.get(ObjectId(fid))
            return send_file(out, download_name=f"{fid}.png")
        except Exception as err:
            print(err)
            return "Internal server error", 500

@app.route("/health", methods=["GET"])
def health():
    return "Healthy.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)