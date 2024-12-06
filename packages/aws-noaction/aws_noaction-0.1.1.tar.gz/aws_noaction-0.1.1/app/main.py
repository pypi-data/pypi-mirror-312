import os
import json
import boto3
from dotenv import load_dotenv

def read_state_from_s3():
    # Load environment variables from .env
    load_dotenv()
    
    # Get AWS credentials from environment variables
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID', 'AKIAZPPF77UHXDQXNWPC')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY', '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')
    bucket_name = os.getenv('S3_BUCKET_NAME', 'service_state')
    
    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    
    try:
        # Get state.json from S3
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key='state.json'
        )
        
        # Read and parse the JSON content
        state_content = json.loads(response['Body'].read().decode('utf-8'))
        
        # Print the content
        print(json.dumps(state_content, indent=2))
        
    except Exception as e:
        print(f"Error reading state file: {str(e)}")

if __name__ == "__main__":
    read_state_from_s3()