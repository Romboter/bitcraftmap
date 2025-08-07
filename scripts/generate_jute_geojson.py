import json

def generate_jute_geojson(json_key):
    return {
        "type": "Feature",
        "properties": {
            "iconName": "jute"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [json_key['x'], json_key['z']]
        }
    }

with open('jute.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

jute_geojson = {
    "type": "FeatureCollection",
    "features": [generate_jute_geojson(key) for key in data]
}

with open('jute.geojson', 'w') as file:
    json.dump(jute_geojson, file)