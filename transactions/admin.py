from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'amount', 'fraud_probability', 'is_fraud', 'created_at')
    list_filter = ('is_fraud', 'created_at')
    search_fields = ('transaction_id',)
    ordering = ('-created_at',)
