import os
import re
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
# Import custom modules
from config import Path



def convert_poverty_files():

    path = Path("downloads", "xlsx-files", "csv-files")
    path_source = path.get_source_path()
    path_destination = path.get_destination_path()

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

    def execute_poverty_creation():
        """Execute the conversion of Excel files to CSV format."""

        extract_duplicate_columns = True

        # Process each file in the source directory
        for i,filename in enumerate(os.listdir(path_source)):

            # Extract duplicate columns
            with open(os.path.join(path_source, filename), 'rb') as file:
                df = pd.read_excel(file, engine='openpyxl')

                df_fixed = fix_values_shifted(df, 5)
                df_fixed = remove_quotes(df_fixed)

                #Filter the DataFrame with first file and filter the relevant columns for the others
                if extract_duplicate_columns:
                    df_filtered = df_fixed.iloc[:, :-2]
                    neighbour = "city"
                    df_pivoted = pivot(df_filtered)
                    df_pivoted.to_csv(os.path.join(path_destination, f"poverty_family_structure_{neighbour}.csv"), index=False)
                    extract_duplicate_columns = False

                df_filtered = df_fixed.iloc[:, [0, -2, -1]]
                neighbour = re.search(r"_([^_.]+)\.[^.]+$", filename).group(1)

                df_pivoted = pivot(df_filtered)
                df_pivoted.to_csv(os.path.join(path_destination, f"poverty_family_structure_{neighbour}.csv"), index=False)

    # Execute the conversion process
    execute_poverty_creation()

def associate_points_with_districts():
    """Associate points with regions based on geographical data."""

    # Load the CSV file with points
    path_source1 = Path("data", "crime", "crime")
    df = pd.read_csv(path_source1.get_source_path() + "/crime_montreal_cleaned.csv")
    geometry = [Point(xy) for xy in zip(df['LONGITUDE'], df['LATITUDE'])]
    points_gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    # Load the GeoJSON file
    path_source2 = Path("data","municipality", "crime")
    geojson = path_source2.get_source_path() + "/municipality_polygon_map.geojson"
    gdf = gpd.read_file(geojson)

    # Perform spatial join to associate points with districts
    district_gdf = gdf.to_crs(points_gdf.crs)
    joined_data = gpd.sjoin(points_gdf, district_gdf, how="inner", predicate="within")
    crime_districts = joined_data.drop(["geometry"], axis=1)

    # Save the result to a new CSV file
    path_destination = path_source1.get_destination_path() + "/crime_montreal_with_districts.csv"
    pd.DataFrame(crime_districts).to_csv(path_destination, index=False)
