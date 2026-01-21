# API Documentation

## POST /webhook/payments

Webhook receiver endpoint for payment status events.

### Request

- Method: `POST`
- URL: `/webhook/payments`
- Headers:
  - `Content-Type: application/json`
  - `X-Razorpay-Signature: <hmac_sha256(testsecret, raw_body)>`
- Body: JSON payload in Razorpay-like format, e.g.:

```json
{
    "event": "payment.authorized",
    "payload": {
      "payment": {
        "entity": {
          "id": "pay_001",
          "status": "authorized",
          "amount": 1000,
          "currency": "INR"
        }
      }
    },
    "created_at": 1751885965,
    "id": "evt_auth_001"
  }

### Response

#### 1. Success Response (200 OK)

New Event
{
  "status": "accepted",
  "event_id": "evt_auth_014"
}

Duplicate Event
{
  "status": "duplicate_ignored",
  "event_id": "evt_auth_014"
}


#### 2. Error Responses

403 – Invalid Signature
{
  "error": {
    "code": "INVALID_SIGNATURE",
    "message": "Missing or incorrect webhook signature.",
    "details": {}
  }
}

400 – Invalid JSON
{
  "error": {
    "code": "INVALID_JSON",
    "message": "Invalid JSON body.",
    "details": {}
  }
}

400 – Invalid Payload
{
  "error": {
    "code": "INVALID_PAYLOAD",
    "message": "Missing required fields: event, id, payload.payment.entity.id",
    "details": {}
  }
}

## GET /payments/{payment_id}/events

Returns all events for a specific payment.

### Request
- Method: GET
- URL: /payments/{payment_id}/events
- Example: /payments/pay_014/events

### Responses

Success Response (200 OK)

[
  {
    "event_type": "payment_authorized",
    "received_at": "2025-01-01T10:00:00Z"
  },
  {
    "event_type": "payment_captured",
    "received_at": "2025-01-01T10:05:00Z"
  }
]
