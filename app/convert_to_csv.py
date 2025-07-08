import os
import pandas

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
download_path_source = os.path.join(project_root, "downloads", "xlsx-files")
download_path_destination = os.path.join(project_root, "downloads", "csv-files")

def fix_values_shifted(df, row_number):
    """Fix columns shifted by one row in the DataFrame."""
    # Fix the first column shifted by one row
    df.iloc[row_number,0] = str(df.iloc[row_number, 0]) + str(df.iloc[row_number, 1])

    # Fix all other columns shifted by one row
    for col in range(1, len(df.columns[1:])):
       df.iloc[row_number, col] = df.iloc[row_number, col +1]

    return df[df.columns[:-1]]  # Remove the last column which is now empty

for file_name in os.listdir(download_path_source):
    pass

# Extract duplicate columns
with open(os.path.join(download_path_source, os.listdir(download_path_source)[0]), 'rb') as file:
    df = pandas.read_excel(file, engine='openpyxl')

    df_fixed = fix_values_shifted(df, 5)

    index_cols = df_fixed.columns[1:].tolist()

    pivoted = df_fixed.pivot(
        index=index_cols,
        columns=df_fixed.columns[0],
        values=df_fixed.columns[-1]
    )

    print(pivoted)
