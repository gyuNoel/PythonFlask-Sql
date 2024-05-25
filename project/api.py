from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "orders"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

users ={
    "gyuNoel":"passWord",
    "crimsonweave":"luna600",
}

@auth.verify_password
def verify_password(username,password):
    if username in users and users[username] == password:
        return username


@app.route("/")
@auth.login_required()
def hello_world():
    return "<p>Orders Database.</p>"

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

def dict_to_xml(data):
    xml = ['<root>']
    for item in data:
        xml.append('<item>')
        for key, value in item.items():
            xml.append(f'<{key}>{value}</{key}>')
        xml.append('</item>')
    xml.append('</root>')
    return ''.join(xml)

def output_format(data, format):
    if format == 'xml':
        xml_data = dict_to_xml(data)
        response = make_response(xml_data, 200)
        response.headers["Content-Type"] = "application/xml"
    else:  # Default to JSON
        response = make_response(jsonify(data), 200)
        response.headers["Content-Type"] = "application/json"
    return response

@app.route("/users", methods=["GET"])
@auth.login_required()
def get_users():
    format = request.args.get('format', 'json')
    data = data_fetch("""select * from users""")
    return output_format(data, format)

@app.route("/products", methods=["GET"])
@auth.login_required()
def get_products():
    format = request.args.get('format', 'json')
    data = data_fetch("""SELECT name,price,stock from orders.products""")
    return output_format(data, format)

@app.route("/orders", methods=["GET"])
@auth.login_required()
def get_orders():
    format = request.args.get('format', 'json')
    data = data_fetch("""select * from orders""")
    return output_format(data, format)

@app.route("/orderdetails", methods=["GET"])
@auth.login_required()
def get_order_details():
    format = request.args.get('format', 'json')
    data = data_fetch("""select * from orderdetails""")
    return output_format(data, format)

@app.route("/users/<int:id>", methods=["GET"])
@auth.login_required()
def get_user_by_id(id):
    format = request.args.get('format', 'json')
    data = data_fetch("""SELECT user_id, username ,email FROM users where user_id = {}""".format(id))
    return output_format(data, format)

@app.route("/users/<int:id>/orders", methods=["GET"])
@auth.login_required()
def get_orders_by_user_id(id):
    format = request.args.get('format', 'json')
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
    return output_format(data, format)

@app.route("/users", methods=["POST"])
@auth.login_required()
def add_user():
    cur = mysql.connection.cursor()
    info = request.get_json()
    username = info["Username"]
    email = info["email"]
    cur.execute(
        """ INSERT INTO users (username, email) VALUE (%s, %s)""",
        (username, email),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "username added successfully", "rows_affected": rows_affected}
        ),
        201,
    )

@app.route("/users/<int:id>", methods=["PUT"])
@auth.login_required()
def edit_user(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    username = info["Username"]
    email = info["email"]
    cur.execute(
        """ UPDATE users SET username=%s, email=%s WHERE user_id = %s""",
        (username, email,id),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "username edited successfully", "rows_affected": rows_affected}
        ),
        201,
    )

@app.route("/users/<int:id>", methods=["DELETE"])
@auth.login_required()
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM users where user_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "User deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

if __name__ == "__main__":
    app.run(debug=True)

