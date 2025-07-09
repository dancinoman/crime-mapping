from app import download_files as df
from app import convert_to_csv as cc
from app import export_csv as ec

if __name__ == "__main__":

    print("Starting the download process...")
    df.download_file_from_url()
    print("File downloaded now converting to CSV...")
    cc.execute_csv_creation()
    print("CSV files created, now uploading to S3...")
    ec.upload_csv_to_s3()
    print("Pipeline completed successfully!")
