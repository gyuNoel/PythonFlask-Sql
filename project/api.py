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

@app.route("/orders", methods=["GET"])
def get_orders():
    data = data_fetch("""select * from orders""")
    return make_response(jsonify(data), 200)

@app.route("/orderdetails", methods=["GET"])
def get_order_details():
    data = data_fetch("""select * from orderdetails""")
    return make_response(jsonify(data), 200)

@app.route("/users/<int:id>", methods=["GET"])
def get_user_by_id(id):
    data = data_fetch("""SELECT user_id, username ,email FROM users where user_id = {}""".format(id))
    return make_response(jsonify(data), 200)

@app.route("/users/<int:id>/orders", methods=["GET"])
def get_orders_by_user_id(id):
    data = data_fetch("""SELECT 
    o.order_id, 
    u.username AS user_name,
    p.name AS product_name,
    p.price AS product_price,
    o.order_date,
    od.quantity,
    o.status AS order_status
FROM 
    orders o
JOIN 
    users u ON o.user_id = u.user_id
JOIN 
    orderdetails od ON o.order_id = od.order_id
JOIN 
    products p ON od.product_id = p.product_id
where u.user_id = {}
                        """.format(id))
    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)