E-commerce Django Project
Overview
This is a Django-based e-commerce RESTful API that allows users to browse products, make purchases using PayPal, and manage their accounts. The project uses Django REST Framework for API development, Djoser for JWT authentication, and PayPal for secure payment processing. It is hosted on GitHub and deployed to Render.
Features

User Management: Register, log in, and manage user profiles using JWT authentication.
Product Management: View available products with details like name and price.
Order Processing: Create orders and pay securely via PayPal.
API Documentation: Swagger and DRF docs for easy endpoint exploration.
Admin Interface: Manage products, orders, and users via Django’s admin panel.

Prerequisites

Python 3.8+
PostgreSQL (for production) or SQLite (for development)
PayPal developer account for payment integration
Git for cloning the repository
Virtual environment tool (e.g., venv or pipenv)

Installation

Clone the Repository:
git clone https://github.com/okonkwo348/E-commerce.git
cd E-commerce


Set Up a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt

Ensure requirements.txt includes:
django
djangorestframework
djoser
djangorestframework-simplejwt
paypalrestsdk
psycopg2-binary
gunicorn


Configure Environment Variables:Create a .env file in the project root:
touch .env

Add the following (replace with your values):
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3  # Or PostgreSQL URL for production
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
PAYPAL_RETURN_URL=http://localhost:8000/api/orders/payment/success/
PAYPAL_CANCEL_URL=http://localhost:8000/api/orders/payment/cancel/


Run Migrations:
python manage.py migrate


Create a Superuser (for admin access):
python manage.py createsuperuser


Start the Development Server:
python manage.py runserver

Access the API at http://localhost:8000.


API Endpoints
Below are the main endpoints for the users, products, and orders apps, plus authentication routes.
Authentication (Djoser)

Register: POST /api/auth/users/
Body: {"username": "string", "password": "string", "email": "string"}


Login: POST /api/auth/jwt/create/
Body: {"username": "string", "password": "string"}
Returns: JWT access and refresh tokens


Refresh Token: POST /api/auth/jwt/refresh/
Body: {"refresh": "string"}


User Profile: GET /api/auth/users/me/ (requires authentication)

Users

List Users: GET /api/users/ (admin only)
Retrieve User: GET /api/users/<id>/ (admin or self)

Products

List Products: GET /api/products/
Retrieve Product: GET /api/products/<id>/
Create Product: POST /api/products/ (admin only)
Body: {"name": "string", "price": "decimal", "description": "string"}



Orders

Create Payment: POST /api/orders/payment/<product_id>/
Initiates a PayPal payment for a product.
Returns: {"payment_url": "string", "order_id": "integer"}
Example: POST /api/orders/payment/1/ redirects to PayPal for payment.


Payment Success: GET /api/orders/payment/success/
Confirms payment after PayPal redirect.
Query Params: ?paymentId=string&PayerID=string
Returns: {"message": "Payment successful", "order": {order_details}}


List Orders: GET /api/orders/ (authenticated user)
Retrieve Order: GET /api/orders/<id>/ (authenticated user)

API Documentation

Swagger UI: http://localhost:8000/swagger-docs/
DRF Docs: http://localhost:8000/docs/

PayPal Integration
The orders app integrates PayPal for secure payments:

Create Payment: When a user selects a product, the CreatePaymentView generates a PayPal payment link. The user is redirected to PayPal to complete the payment.
Payment Success: After payment, PayPal redirects back to the success endpoint, where PaymentSuccessView confirms the payment and updates the order status.
Setup: Ensure PayPal credentials are set in .env. Get credentials from the PayPal Developer Dashboard.

Deployment to Render

Push your code to GitHub.
Create a Render account and a new Web Service.
Configure:
Build Command: pip install -r requirements.txt && python manage.py migrate
Start Command: gunicorn project.wsgi:application --bind 0.0.0.0:$PORT
Environment Variables: Add SECRET_KEY, DATABASE_URL (PostgreSQL), PAYPAL_*, etc.


Deploy and test the live URL.
Set DEBUG=False and configure static files for production.

Testing

Run tests: python manage.py test
Test PayPal payments in sandbox mode using test accounts from the PayPal Developer Dashboard.
Use tools like Postman to test API endpoints.

Contributing

Fork the repository.
Create a feature branch: git checkout -b feature-name
Commit changes: git commit -m "Add feature"
Push to GitHub: git push origin feature-name
Open a pull request.

Contact
For issues or questions, contact okonkwo348 or open an issue on the GitHub repository.
License
This project is licensed under the MIT License.
