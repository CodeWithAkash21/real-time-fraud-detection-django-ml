from django.urls import path
from .views import FraudDetectionView, DashboardStatsView, TransactionListView

urlpatterns = [
    path('detect/', FraudDetectionView.as_view(), name='fraud-detect'),
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
]
