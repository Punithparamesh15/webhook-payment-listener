from django.urls import path
from .views import *

urlpatterns = [
    path("webhook/payments", PaymentWebhookAPIView.as_view(), name="webhook-payments"),
    path("payments", PaymentsListAPIView.as_view(), name="payments-list"),
    path("payments/<str:payment_id>/events", PaymentEventsAPIView.as_view(), name="payment-events"),
]