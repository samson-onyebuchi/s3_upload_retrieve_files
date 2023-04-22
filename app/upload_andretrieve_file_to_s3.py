import os
import boto3
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

s3 = boto3.client(
    's3',
    os.getenv('AWS_ACCESS_KEY_ID'),
    os.getenv('AWS_SECRET_ACCESS_KEY'),
    os.getenv('AWS_REGION')
)

@app.route('/download_file', methods=['GET'])
def download_file():
    bucket_name = request.args.get('bucket_name')
    file_name = request.args.get('file_name')

    try:
        with open(file_name, 'wb') as f:
            s3.download_fileobj(bucket_name, file_name, f)
    except Exception as e:
        return jsonify({'error': f'Error downloading {file_name} from {bucket_name}: {e}'})

    return jsonify({'message': f'{file_name} downloaded from {bucket_name}'})

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'error': 'Internal server error'}), 500



@app.route('/upload', methods=['POST'])
def upload_file():
    bucket_name = request.form.get('bucket_name')
    file = request.files['file']
    file_name = file.filename

    # Save file to disk
    file.save(file_name)

    # Upload file to S3 bucket
    try:
        with open(file_name, 'rb') as f:
            s3.upload_fileobj(f, bucket_name, file_name)
    except Exception as e:
        return jsonify({'error': f'Error uploading {file_name} to {bucket_name}: {e}'})

    # Delete file from disk
    os.remove(file_name)

    return jsonify({'message': f'{file_name} uploaded to {bucket_name}'})

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'error': 'Internal server error'}), 500
