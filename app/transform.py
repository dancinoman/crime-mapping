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
    """
    Load crime with points and compare which distrcict they belong to.
    With that polygon on hand, we can calculate the centroid of each district.
    Dataset crime: new "nom_arr" column
    Dataset municipality: new "centroid_longidue" and "centroid_latitude" columns
    """
    path_source1 = Path("data", "crime", "crime")
    df_crime = pd.read_csv(path_source1.get_source_path() + "/crime_montreal_cleaned.csv")
    geometry = [Point(xy) for xy in zip(df_crime['LONGITUDE'], df_crime['LATITUDE'])]
    points_gdf = gpd.GeoDataFrame(df_crime, geometry=geometry, crs="EPSG:4326")

    # Load the GeoJSON file
    path_source2 = Path("data","municipality", "municipality")
    geojson = path_source2.get_source_path() + "/municipality_polygon_map.geojson"
    # Load municipality
    df_municipality = pd.read_csv(path_source2.get_source_path() + "/municipality_montreal_cleaned.csv")

    gdf = gpd.read_file(geojson)

    # Perform spatial join to associate points with districts
    district_gdf = gdf.to_crs(points_gdf.crs)
    joined_data = gpd.sjoin(points_gdf, district_gdf, how="inner", predicate="within")
    crime_districts = joined_data.drop(["geometry"], axis=1)

    # Remove null values in the 'nom_arr' column
    crime_districts = crime_districts.dropna(subset=["nom_arr"])

    # Calculate the centroid (average coordinate) of each polygon and add as new columns
    # To get accurate centroids, re-project to a projected CRS (e.g., EPSG:2950 for Montreal)
    # before calculating the centroid, and then re-project back to EPSG:4326 for output.
    district_centroids_projected = district_gdf.to_crs(epsg=2950) # Project to a local projected CRS
    district_centroids_projected['geometry_centroid'] = district_centroids_projected.geometry.centroid

    # Convert the centroids back to EPSG:4326 (latitude/longitude)
    district_centroids_latlon = district_centroids_projected.set_geometry('geometry_centroid', crs=2950)
    district_centroids_latlon = district_centroids_latlon.to_crs(epsg=4326)

    # Extract the longitude and latitude from the re-projected centroids
    district_centroids_latlon['centroid_longitude'] = district_centroids_latlon.geometry.x
    district_centroids_latlon['centroid_latitude'] = district_centroids_latlon.geometry.y

    # Group by to get one row per district
    centroids_for_merge = (
        district_centroids_latlon
        .groupby('nom_arr', as_index= False)[['centroid_longitude', 'centroid_latitude']]
        .first()
    )

    # This ensures each municipality record receive their district centroid matched
    municipaly_center = pd.merge(df_municipality, centroids_for_merge, left_on='district_name', right_on= 'nom_arr', how='left')

    # Save the result to a new CSV file
    path_destination_crime = path_source1.get_destination_path() + "/crime_montreal_district_cleaned.csv"
    path_destination_municipality = path_source2.get_destination_path() + "/municipality_montreal_centered_cleaned.csv"

    # Save results in dataframes
    pd.DataFrame(crime_districts).to_csv(path_destination_crime, index=False)
    pd.DataFrame(municipaly_center).to_csv(path_destination_municipality, index=False)
