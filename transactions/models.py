from django.db import models

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True, db_index=True)
    amount = models.FloatField()
    features = models.JSONField(help_text="JSON list of V1-V28 features + Time")
    fraud_probability = models.FloatField()
    is_fraud = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.fraud_probability:.4f}"

    class Meta:
        ordering = ['-created_at']
