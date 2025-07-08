import os
import pandas

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
download_path = os.path.join(project_root, "downloads")

for file_name in os.listdir(download_path):
    print(file_name)

with open(os.path.join(download_path, os.listdir(download_path)[0]), 'rb') as file:
    df = pandas.read_excel(file, engine='openpyxl')
    print(df.head())
