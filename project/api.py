from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "orders"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/users", methods=["GET"])
def get_users():
    data = data_fetch("""select * from users""")
    return make_response(jsonify(data), 200)

@app.route("/products", methods=["GET"])
def get_products():
    data = data_fetch("""select * from products""")
    return make_response(jsonify(data), 200)



if __name__ == "__main__":
    app.run(debug=True)


