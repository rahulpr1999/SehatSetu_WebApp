import sys
import os
import uuid

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.aws_dynamo import DynamoDBClient

def seed_doctors():
    db = DynamoDBClient()
    
    doctors = [
        {"name": "Dr. Harpreet Singh", "department": "General Medicine", "specialization": "Internal Medicine", "experience": 15},
        {"name": "Dr. Manpreet Kaur", "department": "Pediatrics", "specialization": "Child Health", "experience": 10},
        {"name": "Dr. Gurpreet Singh Bains", "department": "Orthopedics", "specialization": "Bone & Joint Surgery", "experience": 12},
        {"name": "Dr. Jaspreet Kaur Sandhu", "department": "Gynecology", "specialization": "Women's Health", "experience": 14},
        {"name": "Dr. Amarjeet Singh Dhillon", "department": "Cardiology", "specialization": "Heart Specialist", "experience": 18},
        {"name": "Dr. Kuldeep Singh Randhawa", "department": "ENT", "specialization": "Ear, Nose & Throat", "experience": 8},
        {"name": "Dr. Simranjeet Kaur", "department": "Dermatology", "specialization": "Skin Specialist", "experience": 11},
        {"name": "Dr. Balwinder Singh Gill", "department": "Surgery", "specialization": "General Surgery", "experience": 20},
        {"name": "Dr. Navpreet Kaur Grewal", "department": "Ophthalmology", "specialization": "Eye Specialist", "experience": 9},
        {"name": "Dr. Rajveer Singh Virk", "department": "Neurology", "specialization": "Brain & Nerve Specialist", "experience": 16},
        {"name": "Dr. Prabhjot Kaur Sidhu", "department": "Psychiatry", "specialization": "Mental Health", "experience": 13}
    ]

    print("Starting Doctor Injection...")
    count = 0
    for doc in doctors:
        item = {
            'id': f'doc-{str(uuid.uuid4())[:8]}',
            'name': doc['name'],
            'department': doc['department'],
            'specialization': doc['specialization'],
            'experience_years': doc['experience'],
            'available': True,
            'consultation_fee': 500,
            'schedule': {}
        }
        if db.add_doctor(item):
            print(f"  [+] Added: {doc['name']} - {doc['department']}")
            count += 1
        else:
            print(f"  [-] Failed: {doc['name']}")
            
    print(f"\nSuccessfully added {count} doctors to DynamoDB!")

if __name__ == "__main__":
    seed_doctors()
