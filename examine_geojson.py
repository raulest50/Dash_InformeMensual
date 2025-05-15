import json

# Load the GeoJSON file
with open('colombiaMod.json', 'r', encoding='utf-8') as f:
    colombia_geojson = json.load(f)

# Print the type of the GeoJSON
print(f"GeoJSON type: {colombia_geojson['type']}")

# Print the number of features
print(f"Number of features: {len(colombia_geojson['features'])}")

# Print the properties of the first feature
if 'features' in colombia_geojson and len(colombia_geojson['features']) > 0:
    first_feature = colombia_geojson['features'][0]
    print("\nProperties of the first feature:")
    for key, value in first_feature['properties'].items():
        print(f"  {key}: {value}")