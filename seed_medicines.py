import sys
import os
import uuid
import random

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.aws_dynamo import DynamoDBClient

def seed_medicines():
    db = DynamoDBClient()
    
    medicines = [
        {"name": "Paracetamol (Dolo 650)", "category": "Fever/Pain", "price": 30, "stock": 500},
        {"name": "Azithromycin (Azithral 500)", "category": "Antibiotic", "price": 120, "stock": 100},
        {"name": "Amoxicillin (Mox 500)", "category": "Antibiotic", "price": 85, "stock": 150},
        {"name": "Metformin (Glycomet 500)", "category": "Diabetes", "price": 45, "stock": 300},
        {"name": "Atorvastatin (Atorva 10)", "category": "Heart/Cholesterol", "price": 90, "stock": 200},
        {"name": "Pantoprazole (Pan 40)", "category": "Gastritis", "price": 110, "stock": 400},
        {"name": "Cetirizine (Cetzine 10)", "category": "Allergy", "price": 20, "stock": 600},
        {"name": "Ibuprofen (Brufen 400)", "category": "Pain Relief", "price": 25, "stock": 250},
        {"name": "Aspirin (Ecosprin 75)", "category": "Heart/Blood Thinner", "price": 15, "stock": 500},
        {"name": "Amlodipine (Amlong 5)", "category": "Hypertension", "price": 40, "stock": 300},
        {"name": "Telmisartan (Telma 40)", "category": "Hypertension", "price": 60, "stock": 250},
        {"name": "Metoprolol (Metolar 25)", "category": "Heart", "price": 75, "stock": 150},
        {"name": "Glimepiride (Amaryl 1mg)", "category": "Diabetes", "price": 55, "stock": 200},
        {"name": "Montelukast (Montek LC)", "category": "Allergy/Asthma", "price": 130, "stock": 100},
        {"name": "Ranitidine (Rantac 150)", "category": "Gastritis", "price": 20, "stock": 350},
        {"name": "Diclofenac (Voveran 50)", "category": "Pain Relief", "price": 35, "stock": 200},
        {"name": "Ofloxacin (Zanocin 200)", "category": "Antibiotic", "price": 95, "stock": 120},
        {"name": "Vitamin C (Limcee 500)", "category": "Supplement", "price": 25, "stock": 400},
        {"name": "Calcium + Vit D3 (Shelcal 500)", "category": "Supplement", "price": 110, "stock": 300},
        {"name": "B-Complex (Becosules)", "category": "Supplement", "price": 45, "stock": 450}
    ]

    print("Starting Medicine Injection...")
    count = 0
    for med in medicines:
        item = {
            'id': str(uuid.uuid4()),
            'name': med['name'],
            'category': med['category'],
            'price': med['price'],
            'in_stock': True,
            'quantity': med['stock']
        }
        if db.add_medicine(item):
            print(f"  [+] Added: {med['name']}")
            count += 1
        else:
            print(f"  [-] Failed: {med['name']}")
            
    print(f"\nSuccessfully added {count} medicines to DynamoDB!")

if __name__ == "__main__":
    seed_medicines()
