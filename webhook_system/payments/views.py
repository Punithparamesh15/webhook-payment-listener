from django.shortcuts import render
import json
from django.conf import settings
from django.db import IntegrityError, transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError

from .models import PaymentEvent
from .serializers import PaymentEventListSerializer
from .services.signature import verify_signature
from .services.parser import extract_fields, PayloadError, ensure_event_list, normalize_event_type
from django.db.models import Count

# Create your views here.
"""
Consistent error response format (reviewer-friendly).
"""
def error_response(code: str, message: str, http_status: int, details: dict | None = None):
    return Response(
        {"error": {"code": code, "message": message, "details": details or {}}},
        status=http_status,
    )

class PaymentWebhookAPIView(APIView):
    """
    POST /webhook/payments

    1) Signature validation (must use raw body)
    2) DRF JSON parsing (cleaner than manual json.loads)
    3) Convert payload to list of events (supports your fixed company payload)
    4) Process each event object in the list
    5) Normalize event_type for consistent output / storage (optional but clean)
    6) Store each event in DB, avoiding duplicates via unique event_id constraint
    7) Return summary of accepted vs duplicate events
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):

        raw_body = request.body
        signature = request.headers.get("X-Razorpay-Signature")
        
        # 
        if not verify_signature(settings.WEBHOOK_SECRET, raw_body, signature):
            return error_response(
                "INVALID_SIGNATURE",
                "Missing or incorrect webhook signature.",
                status.HTTP_403_FORBIDDEN,
            )

        # 
        try:
            payload = request.data
        except ParseError:
            return error_response(
                "INVALID_JSON",
                "Request body must be valid JSON.",
                status.HTTP_400_BAD_REQUEST,
            )
        
        # 
        try:
            events = ensure_event_list(payload)
        except PayloadError as e:
            return error_response(
                "INVALID_PAYLOAD",
                str(e),
                status.HTTP_400_BAD_REQUEST,
            )

        accepted = 0
        duplicates = 0

        # 
        for event_obj in events:
            try:
                event_type, event_id, payment_id = extract_fields(event_obj)
            except PayloadError as e:
                return error_response(
                    "INVALID_PAYLOAD",
                    str(e),
                    status.HTTP_400_BAD_REQUEST,
                )

            # 
            event_type = normalize_event_type(event_type)

            try:
                _, created = PaymentEvent.objects.get_or_create(
                    event_id=event_id,
                    defaults={
                        "event_type": event_type,
                        "payment_id": payment_id,
                        "payload": event_obj,  # store the single event object (not the full list)
                    },
                )
            except IntegrityError:
                created = False

            if created:
                accepted += 1
            else:
                duplicates += 1

        return Response(
            {"status": "accepted", "accepted": accepted, "duplicates": duplicates},
            status=status.HTTP_200_OK,
        )

class PaymentEventsAPIView(APIView):
    """
    GET /payments/{payment_id}/events
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, payment_id: str):
        events = PaymentEvent.objects.filter(payment_id=payment_id).order_by("received_at")
        return Response(PaymentEventListSerializer(events, many=True).data, status=status.HTTP_200_OK)
    
class PaymentsListAPIView(APIView):
    """
    GET /payments
    Returns all unique payment IDs
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = (PaymentEvent.objects.values("payment_id").annotate(events=Count("id")).order_by("payment_id"))
        return Response(list(data), status=status.HTTP_200_OK)