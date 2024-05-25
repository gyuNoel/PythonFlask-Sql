from api import *
import unittest
import json

class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.auth_headers = {
            'Authorization': 'Basic ' + 'Z3l1Tm9lbDpwYXNzV29yZA==',  # Base64 for "gyuNoel:passWord"
            'Content-Type': 'application/json'
        }
        
        with self.app.app_context():
            # Set up your test database and add any required test data
            cur = MySQL().connection.cursor()
            cur.execute("CREATE DATABASE IF NOT EXISTS test_db")
            cur.execute("USE test_db")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(50) NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    product_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    stock INT NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    order_date DATETIME,
                    status VARCHAR(20),
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS orderdetails (
                    orderdetails_id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT,
                    product_id INT,
                    quantity INT,
                    FOREIGN KEY (order_id) REFERENCES orders(order_id),
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                )
            """)
            MySQL().connection.commit()
            cur.close()

    def tearDown(self):
        with self.app.app_context():
            # Drop all tables after tests
            cur = MySQL().connection.cursor()
            cur.execute("DROP DATABASE IF EXISTS test_db")
            cur.close()

    def test_get_users(self):
        response = self.client.get('/users', headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_add_user(self):
        new_user = {
            "Username": "NewAddedUser",
            "email": "newaddeduser@example.com"
        }
        response = self.client.post('/users', headers=self.auth_headers, data=json.dumps(new_user))
        self.assertEqual(response.status_code, 201)
        self.assertIn('username added successfully', response.get_data(as_text=True))

    def test_edit_user(self):
        edit_user = {
            "Username": "Lom0",
            "email": "randomemail900@example.com"
        }
        response = self.client.put('/users/1', headers=self.auth_headers, data=json.dumps(edit_user))
        self.assertEqual(response.status_code, 201)
        self.assertIn('username added successfully', response.get_data(as_text=True))

    def test_delete_user(self):
        response = self.client.delete('/users/122', headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('User deleted successfully', response.get_data(as_text=True))

    def test_get_products(self):
        response = self.client.get('/products', headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_get_orders(self):
        response = self.client.get('/orders', headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_get_order_details(self):
        response = self.client.get('/orderdetails', headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id(self):
        response = self.client.get('/users/1', headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_get_orders_by_user_id(self):
        response = self.client.get('/users/1/orders', headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
if __name__ == "__main__":
    unittest.main()