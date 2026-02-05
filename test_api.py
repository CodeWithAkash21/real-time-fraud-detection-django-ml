import urllib.request
import json
import random

url = "http://127.0.0.1:8000/api/detect/"

# V1-V28 (28 features). 
# Model expects [Time, V1..V28, Amount]. 
# View adds Time=0 if missing. 
features = [random.uniform(-2, 2) for _ in range(28)]

payload = {
    "transaction_id": f"tx_{random.randint(1000,9999)}",
    "amount": 500.00,
    "features": features
}

print(f"Sending payload: {json.dumps(payload, indent=2)}")

req = urllib.request.Request(
    url, 
    data=json.dumps(payload).encode('utf-8'), 
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status: {response.getcode()}")
        print("Response:", response.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
