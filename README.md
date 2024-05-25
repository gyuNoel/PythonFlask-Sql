# Orders Database API
This project is a RESTful API for managing users, products, and orders using Flask, MySQL, and HTTP Basic Authentication. The API provides endpoints for performing CRUD operations on users, products, and orders, as well as retrieving order details. The project includes unit tests for the API endpoints.

## Project Details
- Framework: Flask
- Database: MySQL
- A uthentication: HTTP Basic Authentication
- Testing: unittest
 
## Installation Instructions
***Prerequisites***
- Python 3.7+
- MySQL
- pip package manager

## Set-up
1. Clone the repository.

`git clone https://github.com/gyuNoel/PythonFlask-Sql.git`

`cd project`

3. Create a virtual environment.

`python -m venv <desired-folder-name>`

`<desired-folder-name>\Scripts\activate`

4. Install necessary libraries.
   
`pip install -r requirements.txt`

## Configure MySQL 
Ensure that MySQL is running and make sure to have a database named orders.
Download the .sql file used in the [project here](https://drive.google.com/file/d/1GZmP48OzY7hQ5PNYLbqJnY5fjBIN62U1/view?usp=sharing)


## Usage examples
***Authentication***

This API uses HTTP Basic Authentication. To execute CRUD, please use [Postman](https://www.postman.com)

- Create a new tab on Postman.
- Under Authorization, Change Type to Basic Auth and enter Username and Password. (Username and Password are inside the api.py file)
- Under Headers, add a new key 'Content Type' with value application/json.

## Routes
## ***GET METHOD***

**/users**
- Show all user details

**/orders**
- Show orders

**/orderdetails**
- Show order details 

**/products**
- Show available products

**/users/<user_id>**
- Show specific user details

**/users/<user_id>/orders**
- Show all orders of specific user

## **POST METHOD**
**/users**
- Add new users

- Set method to POST
- Make sure Authorization and Header Content-Type are set.
-  Under Body, go to raw and type
`
{
"Username":"<Desired-Username>".
"email":"youremail@example.com"
}`
- Press Send.

## **PUT METHOD**
**/users/<user_id>**
- Replace existing users' details (username and email)

**Set method to PUT**
- Make sure Authorization and Header Content-Type are set.
- Under Body, go to raw and type
`
{
"Username":"<Desired-Username>".
"email":"youremail@example.com"
}`

- Press Send.


## **DELETE METHOD**
**/users/<user_id>**
- Deletes existing user

**Set method to DELETE**
- Once the user ID is on the URL bar, press send.

## Error Handling
The API provides meaningful error messages and HTTP status codes to indicate the success or failure of an operation.


