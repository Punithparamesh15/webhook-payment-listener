from django.db import models

# Create your models here.
class PaymentEvent(models.Model):
    event_id = models.CharField(max_length=128, unique=True, db_index=True)
    event_type = models.CharField(max_length=128, db_index=True)
    payment_id = models.CharField(max_length=128, db_index=True)
    payload = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["received_at"]

    def __str__(self):
        return f"{self.payment_id} - {self.event_type} ({self.event_id})"