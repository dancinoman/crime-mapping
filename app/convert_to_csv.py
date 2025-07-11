import os
import re
import pandas as pd

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

def remove_quotes(df):
    """Remove quotes from DataFrame column and values"""
    df.columns = [col.replace('"', '') for col in df.columns.tolist()]
    df.loc[:,"Catégorie"] = df["Catégorie"].map(lambda x: x.replace('"', '') if isinstance(x, str) else x)
    return df

def pivot(df):
    df_melted = df.melt( id_vars='Catégorie', var_name='Région', value_name='Value')
    df_pivoted = df_melted.pivot(index='Région', columns='Catégorie', values='Value').reset_index()
    return df_pivoted

def execute_csv_creation():
    """Execute the conversion of Excel files to CSV format."""

    # Process each file in the source directory
    for i,filename in enumerate(os.listdir(download_path_source)):

        # Extract duplicate columns
        with open(os.path.join(download_path_source, filename), 'rb') as file:
            df = pd.read_excel(file, engine='openpyxl')

            df_fixed = fix_values_shifted(df, 5)
            df_fixed = remove_quotes(df_fixed)

            #Filter the DataFrame with first file and filter the relevant columns for the others
            if i == 0:
                df_filtered = df_fixed.iloc[:, :-2]
                neighbour = "zcity"
            else:
                df_filtered = df_fixed.iloc[:, [0, -2, -1]]
                neighbour = re.search(r"_([^_.]+)\.[^.]+$", filename).group(1)

            df_pivoted = pivot(df_filtered)
            df_pivoted.to_csv(os.path.join(download_path_destination, f"poverty_family_structure_{neighbour}.csv"), index=False)
