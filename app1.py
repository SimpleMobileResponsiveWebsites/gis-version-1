import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static

# Load a sample dataset - Here we're using the world countries shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

def main():
    st.title("Simple GIS Viewer with Streamlit")

    # Sidebar for controls
    st.sidebar.header("GIS Options")
    zoom_level = st.sidebar.slider("Zoom Level", min_value=1, max_value=18, value=4)
    center_lat = st.sidebar.number_input("Latitude", value=50.0)
    center_lon = st.sidebar.number_input("Longitude", value=10.0)

    # Create a map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_level)

    # Add the world map to the folium map
    for _, row in world.iterrows():
        folium.GeoJson(row['geometry'], name=row['name']).add_to(m)

    # Adding a marker for the center
    folium.Marker([center_lat, center_lon], popup="Map Center").add_to(m)

    # Render the map in Streamlit
    folium_static(m)

    # Optional: Add more GIS functionalities like data upload, shapefile manipulation, etc.
    st.write("Here you could add more GIS functionalities like:")
    st.write("- Upload your own shapefiles")
    st.write("- Perform spatial analysis")
    st.write("- Display attribute data from selected regions")

if __name__ == "__main__":
    main()
