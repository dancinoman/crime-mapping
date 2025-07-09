import boto3
import os

# ======== S3 settings ========
s3 = boto3.client('s3')
S3_BUCKET_NAME = 'crime-porverty-heatmap-data-analysis'
S3_OUTPUT_BUCKET_KEY = 'data/poverty/csv-files'
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
download_path_source = os.path.join(project_root, "downloads", "csv-files")

def upload_csv_to_s3():
    """Upload a CSV file to S3 bucket."""
    for filename in os.listdir(download_path_source):
        try:
            source = os.path.join(download_path_source, filename)
            s3.upload_file(source, S3_BUCKET_NAME, S3_OUTPUT_BUCKET_KEY + '/' + filename)
            print(f"File {filename} uploaded to S3 bucket {S3_BUCKET_NAME} at {S3_OUTPUT_BUCKET_KEY}.")
        except Exception as e:
            print(f"Error uploading file {filename} to S3: {e}")
