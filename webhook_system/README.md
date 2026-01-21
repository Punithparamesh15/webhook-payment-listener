# Minimal Payment Webhook System

This project implements a minimal, secure webhook listener for mocked payment status updates (inspired by Razorpay / PayPal). It exposes:

- `POST /webhook/payments` for receiving payment events.
- `GET /payments/<payment_id>/events` for querying historical events of a payment.

## Features

- Secure webhook receiver with **HMAC SHA256 signature validation**
- Stores full webhook payload for audit and debugging
- API to fetch payment event history in chronological order
- Clean REST API design with proper HTTP status codes
- Uses SQLite by default (can be switched to PostgreSQL in production)

## Tech Stack

- Python 3.12
- Django
- Django REST Framework
- SQLite (default)
- Git

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Punithparamesh15/webhook-payment-listener.git
cd webhook-payment-listener

### 2. Create and activate virtual environment

python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run database migrations

python manage.py makemigrations
python manage.py migrate

### 5. Start the development server

python manage.py runserver

## Testing the Webhook

### Generate Signature

python scripts/make_signature.py mock_payloads/payment_authorized.json
python scripts/make_signature.py mock_payloads/payment_captured.json
python scripts/make_signature.py mock_payloads/payment_failed.json

### Send Webhook Request

curl -X POST http://localhost:8000/webhook/payments -H "Content-Type: application/json" -H "X-Razorpay-Signature: <GENERATED_SIGNATURE>" --data-binary @mock_payloads/payment_authorized.json

curl -X POST http://localhost:8000/webhook/payments -H "Content-Type: application/json" -H "X-Razorpay-Signature: <GENERATED_SIGNATURE>" --data-binary @mock_payloads/payment_captured.json	

curl -X POST http://localhost:8000/webhook/payments -H "Content-Type: application/json" -H "X-Razorpay-Signature: <GENERATED_SIGNATURE>" --data-binary @mock_payloads/payment_failed.json