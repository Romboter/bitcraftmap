from collections import defaultdict
import json

poi_json_file = 'assets/data/caves.json'
grouped = defaultdict(list)
geojson = {
    "type": "FeatureCollection",
    "features": []
}

properties = {
    'Ferralith': {"tier": 1, "iconName": "t1"},
    'Pyrelite': {"tier": 2, "iconName": "t2"},
    'Emarium': {"tier": 3, "iconName": "t3"},
    'Elenvar': {"tier": 4, "iconName": "t4"},
    'Luminite': {"tier": 5, "iconName": "t5"},
    'Rathium': {"tier": 6, "iconName": "t6"},
    'Aurumite': {"tier": 7, "iconName": "t7"},
    'Celestium': {"tier": 8, "iconName": "t8"},
    'Umbracite': {"tier": 9, "iconName": "t9"},
    'Astralite': {"tier": 10, "iconName": "t10"},

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