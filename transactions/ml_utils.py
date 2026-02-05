import joblib
import os
from django.conf import settings

class FraudModel:
    _instance = None
    _model = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance.load_model()
        return cls._instance

    def load_model(self):
        model_path = os.path.join(settings.BASE_DIR, 'ml_engine', 'fraud_model.pkl')
        print(f"Loading model from {model_path}...")
        try:
            self._model = joblib.load(model_path)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise e

    def predict(self, features):
        if self._model is None:
            raise Exception("Model not loaded")
        
        # Features should be shape (1, 30) => [Time, V1..V28, Amount]
        # Our pipeline expects a DataFrame or 2D array.
        # Ensure order matches training: Time, V1-V28, Amount?
        # WAIT. In train_model.py: `X = df.drop(columns=['Class'])`.
        # Initial columns: Time, V1...V28, Amount, Class.
        # X columns: "Time", "V1", ... "V28", "Amount". (Order matters!)
        return self._model.predict_proba([features])[0][1] # Return probability of class 1

# Singleton access
fraud_model = FraudModel.get_instance()
