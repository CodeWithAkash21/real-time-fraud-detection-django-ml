from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.conf import settings
from .models import Transaction
from .serializers import TransactionSerializer, DetectionRequestSerializer
from .ml_utils import fraud_model

class FraudDetectionView(APIView):
    authentication_classes = [] # Disable CSRF usage for this demo
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DetectionRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            transaction_id = data['transaction_id']
            amount = data['amount']
            # Features list. We might need to ensure it has 29 elements + Amount = 30? 
            # Or assume logic handles it. 
            # Our model train logic: X = [Time, V1..V28, Amount]
            # INPUT: features=[v1..v28] (maybe?). 
            # Requirement: "Features: Time, Amount, and V1–V28".
            # Input JSON: "features": [float].
            # I will assume `features` in JSON is the raw list of V1-V28. 
            # And `Time`? The user didn't specify `Time` in input JSON. 
            # I will mock `Time` as 0 if missing (or use len(features) to guess).
            # If features has 30 items, assume full vector.
            # If features has 28 items, assume V1-V28 and append Amount?
            # Model expects 30 items: [Time, V1...V28, Amount] (based on `train_model.py` drop(columns=['Class']))
            # Actually, `train_model.py` column order depends on CSV. 
            # CSV order: Time, V1...V28, Amount, Class.
            # X order: Time, V1...V28, Amount. (30 cols).
            
            raw_features = data['features']
            
            # Construct the feature vector
            # Safe logic: 
            # If len == 30: use as is.
            # If len == 28: prepend Time=0, append Amount. (V1...V28).
            # If len == 29: ???
            
            if len(raw_features) == 30:
                final_features = raw_features
            elif len(raw_features) == 28:
                # Assume V1-V28
                final_features = [0.0] + raw_features + [amount]
            elif len(raw_features) == 29:
                # Assume Time + V1-V28? Or V1-V28 + Amount?
                # Let's assume Time is first.
                 final_features = raw_features + [amount]
            else:
                 # Fallback: Just try to use it, model might error if shape mismatch.
                 # Actually, let's just append amount if it looks like V1-V28.
                 final_features = raw_features
                 # Append amount if not in features (check if user included it?)
                 # The user spec says "features": [float], "amount": float.
                 # It strongly implies `amount` is separate.
                 # I'll stick to: Prepend 0 (Time) + Features + Append Amount.
                 pass

            # Prediction
            try:
                # Ensure we pass the right shape. 
                # Model expects [Time, V1..V28, Amount]
                # If the user sends [V1..V28] in `features`...
                if len(raw_features) == 29: # Time + V1..V28
                     input_vector = raw_features + [amount]
                elif len(raw_features) == 28: # V1..V28
                     input_vector = [0.0] + raw_features + [amount]
                else:
                     input_vector = raw_features # Hope for best

                fraud_prob = fraud_model.predict(input_vector)
            except Exception as e:
                 return Response({"error": f"Prediction failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            is_fraud = fraud_prob > 0.7

            # Save Transaction
            transaction = Transaction.objects.create(
                transaction_id=transaction_id,
                amount=amount,
                features=raw_features,
                fraud_probability=fraud_prob,
                is_fraud=is_fraud
            )

            response_data = {
                "transaction_id": transaction_id,
                "fraud_probability": round(fraud_prob, 4),
                "fraud_detected": is_fraud
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardStatsView(APIView):
    def get(self, request):
        total = Transaction.objects.count()
        fraud_count = Transaction.objects.filter(is_fraud=True).count()
        
        if total > 0:
            fraud_rate = (fraud_count / total) * 100
        else:
            fraud_rate = 0.0

        # Data for chart (fraud vs legit over last 30 days or recent)
        # For simplicity, returning just the counts for now or simple distribution
        
        return Response({
            "total_transactions": total,
            "fraud_transactions": fraud_count,
            "fraud_rate": round(fraud_rate, 2)
        })

class TransactionListView(APIView):
    def get(self, request):
        # Return last 20 transactions
        transactions = Transaction.objects.all().order_by('-created_at')[:20]
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
