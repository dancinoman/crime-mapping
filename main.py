from app import download_files as df
from app import convert as conv
from app import export as ex

if __name__ == "__main__":

    print("Starting the download process...")
    df.download_file_from_url()
    print("File downloaded now converting to CSV...")
    conv.convert_poverty_files()
    print("CSV files created, now uploading to S3...")
    ex.upload_csv_to_s3()
    print("Uploaded CSV files to S3")
    print("Now converting JSON files to stackable data...")
    print("Downloading municipality polygon map...")
    df.download_json()
    conv.convert_geojson()
    ex.upload_json_to_s3()
    print("JSON files converted and uploaded to S3")
    print("Pipeline completed successfully!")
