import pandas as pd
import geopandas as gpd

sdg_data = pd.read_csv(
    "https://raw.githubusercontent.com/francheska-vicente/datapre-project/main_v2/data_output/combined_data.csv"
)
sdg_columns = sdg_data.columns[:-15]
sdg_data = sdg_data[sdg_columns]


sdg_score = pd.read_csv("data/sdg_target_score.csv")

sdg_info = pd.read_csv("data/sdg_infov3.csv")
region_info = pd.read_csv("data/region_infov1.csv")

sdg_regions_available = sdg_data["Geolocation"].unique()[1:]
sdg_indicators_available = sdg_data.columns[2:]

goals_name = sdg_info["Main SDG"].unique()

# gdf_shp = gpd.read_file('data/gadm_ph/regional_data.shp')
''' region = gpd.read_file('data/gadm_ph/gadm_regional.geojson').set_index('geolocation') '''