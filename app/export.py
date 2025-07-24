import boto3
import os
from config import Path

# ======== S3 settings ========
s3 = boto3.client('s3')
S3_BUCKET_NAME = 'crime-porverty-heatmap-data-analysis'

def upload_csv_to_s3():
    S3_OUTPUT_BUCKET_KEY = 'data/poverty/csv-files'
    path = Path("downloads", "csv-files")
    path_source = path.get_source_path()
    """Upload a CSV file to S3 bucket."""
    for filename in os.listdir(path_source):
        try:
            source = os.path.join(path_source, filename)
            s3.upload_file(source, S3_BUCKET_NAME, S3_OUTPUT_BUCKET_KEY + '/' + filename)
            print(f"File {filename} uploaded to S3 bucket {S3_BUCKET_NAME} at {S3_OUTPUT_BUCKET_KEY}.")
        except Exception as e:
            print(f"Error uploading file {filename} to S3: {e}")
"""
def upload_json_to_s3():
    S3_INPUT_FILE = 'downloads/json-files/polygon_map_translate.json'
    S3_OUTPUT_BUCKET_KEY = "data/municipality_polygon/polygon_map_translate.json"
    s3.upload_file(S3_INPUT_FILE, S3_BUCKET_NAME, S3_OUTPUT_BUCKET_KEY)
"""
