import boto3


s3 = boto3.client('s3', aws_access_key_id='ACCESS_KEY', aws_secret_access_key='SECRET_KEY', region_name='REGION')


bucket_name = 'BUCKET_NAME'
file_name = 'FILE_NAME'

with open(file_name, 'rb') as f:
    s3.upload_fileobj(f, bucket_name, file_name)
