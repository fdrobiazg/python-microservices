import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)

app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))

def JWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz,
        },
        secret,
        algorithm="HS256",     
    )

@app.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Authorization failed. Missing credentials.", 401
    
    cur = mysql.connection.cursor()
    res = cur.execute(
        f"SELECT username, password FROM user WHERE username='{str(auth.username)}'"
    )

    if res > 0:
        usr_row = cur.fetchone()
        email = usr_row[0]
        password = usr_row[1]

        if auth.username != email or auth.password != password:
            return "Authorization failed. Invalid credentials.", 401
        else:
            return JWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "Authorization failed. Invalid credentials.", 401

@app.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "Authorization failed. Missing credentials.", 401
    
    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded_jwt = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except:
        return "Authorization failed.", 403
    
    return decoded_jwt, 200


@app.route("/health", methods=["GET"])
def health():
    return "Healthy.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)