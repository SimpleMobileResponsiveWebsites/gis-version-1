import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# Title of the Application
st.title("Interactive GIS Application")

# Sidebar for File Upload
st.sidebar.header("Upload Spatial Data")
uploaded_file = st.sidebar.file_uploader("Upload a GeoJSON or Shapefile", type=["geojson", "zip"])

if uploaded_file:
    try:
        # Check if the uploaded file is a shapefile (zip) or GeoJSON
        if uploaded_file.name.endswith(".zip"):
            # Reading a zipped Shapefile
            gdf = gpd.read_file(f"zip://{uploaded_file.name}")
        else:
            # Reading a GeoJSON file
            gdf = gpd.read_file(uploaded_file)

        # Display the GeoDataFrame
        st.subheader("Uploaded Data Preview")
        st.write(gdf.head())

        # Filter options
        st.sidebar.header("Filter Data")
        columns = list(gdf.columns)
        if len(columns) > 0:
            filter_col = st.sidebar.selectbox("Select column to filter by", columns)
            unique_vals = gdf[filter_col].unique()
            filter_val = st.sidebar.selectbox("Select value to filter", unique_vals)
            
            # Apply filter
            filtered_gdf = gdf[gdf[filter_col] == filter_val]
        else:
            filtered_gdf = gdf

        # Map Visualization
        st.subheader("Map Visualization")
        m = folium.Map(location=[filtered_gdf.geometry.y.mean(), filtered_gdf.geometry.x.mean()], zoom_start=10)
        marker_cluster = MarkerCluster().add_to(m)

        for _, row in filtered_gdf.iterrows():
            if row.geometry.geom_type == "Point":
                folium.Marker(
                    location=[row.geometry.y, row.geometry.x],
                    popup=f"{row[filter_col]}: {filter_val}"
                ).add_to(marker_cluster)

        # Render the map in Streamlit
        st_folium(m, width=700, height=500)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a GeoJSON or Shapefile to start.")

# Footer
st.sidebar.markdown("Developed with ❤️ using Streamlit, GeoPandas, and Folium.")
