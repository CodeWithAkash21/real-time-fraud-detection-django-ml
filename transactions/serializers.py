from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'amount', 'features', 'fraud_probability', 'is_fraud', 'created_at']
        read_only_fields = ['fraud_probability', 'is_fraud', 'created_at']

class DetectionRequestSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(max_length=100)
    amount = serializers.FloatField()
    features = serializers.ListField(
        child=serializers.FloatField(),
        min_length=28, 
        help_text="List of feature values (V1-V28)" 
    )
