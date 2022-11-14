import boto3
from dotenv import load_dotenv
from os import environ

load_dotenv()

sns_client = boto3.client("sns", aws_access_key_id=environ.get("AWS_ACCESS_KEY_ID"), 
                          aws_secret_access_key=environ.get("AWS_SECRET_ACCESS_KEY"), 
                          region_name=environ.get("AWS_REGION"))
