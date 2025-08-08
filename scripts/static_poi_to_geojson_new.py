from collections import defaultdict
import json

poi_json_file = 'assets/data/caves.json'
grouped = defaultdict(list)
geojson = {
    "type": "FeatureCollection",
    "features": []
}

properties = {
    'Ferralith': {"tier": 1, "iconName": "something"},
    'Pyrelite': {"tier": 2, "iconName": "something"},
    'Emarium': {"tier": 3, "iconName": "something"},
    'Elenvar': {"tier": 4, "iconName": "something"},
    'Luminite': {"tier": 5, "iconName": "something"},
    'Rathium': {"tier": 6, "iconName": "something"},
    'Aurumite': {"tier": 7, "iconName": "something"},
    'Celestium': {"tier": 8, "iconName": "something"},
    'Umbracite': {"tier": 9, "iconName": "something"},
    'Astralite': {"tier": 10, "iconName": "something"},

    'First': {"tier": 1, "iconName": "temple"},
    'Second': {"tier": 2, "iconName": "temple"},
    'Third': {"tier": 3, "iconName": "temple"},
    'Fourth': {"tier": 4, "iconName": "temple"},
    'Fifth': {"tier": 5, "iconName": "temple"},

    'Tree': {"tier": 1, "iconName": "travelerTree"},
}

def get_property_from_name(name):
    for keyword, property in properties.items():
        if keyword in name:
            return property.update({"popupText:": name})
        else:
            return {"tier": 1, "iconName": "ruinedCity", "popupText:": name}

def get_size_from_cave_name(name):
    return 2 if 'Large' in name else 1

with open(poi_json_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

for item in data:
    grouped[item["name"]].append([item["location"]["x"], item["location"]["z"]])

for name, coords in grouped.items():
    feature = {
        "type": "Feature",
        "properties": get_property_from_name(name),
        "geometry": {
            "type": "MultiPoint" if len(coords) > 1 else "Point",
            "coordinates": coords if len(coords) > 1 else coords[0]
        }
    }
    geojson["features"].append(feature)
print(json.dumps(geojson))