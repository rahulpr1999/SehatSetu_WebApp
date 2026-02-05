import boto3
from utils.config import Config

def create_patients_table():
    """Create the Nabha_Patients DynamoDB table."""
    
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=Config.AWS_REGION,
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
    )
    
    table_name = 'Nabha_Patients'
    
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'patient_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'patient_id',
                    'AttributeType': 'S'  # String
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        # Wait for the table to be created
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        
        print(f"✅ Table '{table_name}' created successfully!")
        return True
        
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print(f"ℹ️  Table '{table_name}' already exists.")
        return True
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        return False

if __name__ == '__main__':
    create_patients_table()
