from app import download_files as df
from app import convert as conv
from app import export as ex

if __name__ == "__main__":

    print("Starting the conversion process...")
    conv.convert_poverty_files()
    print("Starting to upload to S3...")
    ex.upload_csv_to_s3()
    print("Uploaded CSV files to S3")

    # Start the process of downloading files on web
    print("Starting the download process...")
    df.download_file_from_url()
    print("Pipeline completed successfully!")
