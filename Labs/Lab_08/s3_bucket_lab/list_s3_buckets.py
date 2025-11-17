#!/bin/env python3


import logging
import boto3
from botocore.exceptions import ClientError
import requests
import sys

def download_file(url, local_filename):
    try:
        print(f"Downloading file from {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"File downloaded successfully: {local_filename}")
        return local_filename
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        sys.exit(1)

def upload_to_s3(s3_client, local_file, bucket_name):
    try:
        print(f"Uploading {local_file} to s3://{bucket_name}/{local_file}...")
        s3_client.upload_file(local_file, bucket_name, local_file)
        print("Upload successful!")
        return local_file
    
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        sys.exit(1)

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 script_name.py <URL> <BUCKET_NAME> <EXPIRES_IN_SECONDS>")
        print("\nExample:")
        print("  python3 script_name.py https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif ds2002-f25-atr8ec 604800")
        sys.exit(1)
    
    file_url = sys.argv[1]
    bucket_name = sys.argv[2]
    
    try:
        expires_in = int(sys.argv[3])
    except ValueError:
        print("Error: EXPIRES_IN_SECONDS must be an integer")
        sys.exit(1)
    
    local_filename = file_url.split('/')[-1]
    if not local_filename or '.' not in local_filename:
        local_filename = 'downloaded_file.gif'
    
    download_file(file_url, local_filename)
    
    try:
        s3 = boto3.client('s3', region_name='us-east-1')
    except Exception as e:
        print(f"Error creating S3 client: {e}")
        sys.exit(1)
    
    object_name = upload_to_s3(s3, local_filename, bucket_name)
    
    print(f"Generating presigned URL (expires in {expires_in} seconds)...")
    presigned_url = generate_presigned_url(bucket_name, object_name, expires_in)
    
    if presigned_url is None:
        print("Error: Failed to generate presigned URL")
        sys.exit(1)
    
    print(f"\nPresigned URL (valid for {expires_in} seconds):")
    print(f"\n{presigned_url}\n")

if __name__ == "__main__":
    main()
  
