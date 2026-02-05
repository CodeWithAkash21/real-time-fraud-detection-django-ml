import pandas as pd
import os

# Path to dataset
DATA_PATH = os.path.join(os.getcwd(), 'data', 'creditcard.csv')

def get_fraud_sample():
    if not os.path.exists(DATA_PATH):
        print("Dataset not found.")
        return

    # Read only necessary columns to speed up
    df = pd.read_csv(DATA_PATH)
    
    # Filter for fraud
    fraud_df = df[df['Class'] == 1]
    
    if not fraud_df.empty:
        # Get first fraud sample
        sample = fraud_df.iloc[0]
        
        # Extract features V1-V28
        features = sample[[f'V{i}' for i in range(1, 29)]].values.tolist()
        amount = sample['Amount']
        
        with open('fraud_sample.txt', 'w') as f:
            f.write(f"{amount}\n")
            f.write(", ".join([f"{x:.4f}" for x in features]))
        
        print("Sample saved to fraud_sample.txt")
        
        print("Sample saved to fraud_sample.txt")
    else:
        print("No fraud samples found in dataset.")

if __name__ == "__main__":
    get_fraud_sample()
