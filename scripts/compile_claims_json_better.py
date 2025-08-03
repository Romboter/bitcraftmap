import json

def generate_claims_json(json_key):

    has_bank = 0
    has_market = 0
    has_waystone = 0

    for building in json_key['buildings']:
        # 985246037 Town Bank
        # 934683282 Town Market
        # 205715693 Waystone
        if building['buildingDescriptionId'] == 985246037:
            has_bank = 1
        if building['buildingDescriptionId'] == 934683282:
            has_market = 1
        if building['buildingDescriptionId'] == 205715693:
            has_waystone = 1

    return {
        "type": "Feature",
        "properties": {
            "entityId": json_key['entityId'],
            "name": json_key['name'],
            "tier": json_key['tier'],
            "has_bank": has_bank,
            "has_market": has_market,
            "has_waystone": has_waystone
        },
        "geometry": {
            "type": "Point",
            "coordinates": [json_key['locationX'], json_key['locationZ']]
        }
    }

with open('assets/markers/claims.geojson', 'r', encoding='utf-8') as file:
    data = json.load(file)

claims_geojson = {
    "type": "FeatureCollection",
    "features": [generate_claims_json(key) for key in data]
}

with open('assets/markers/real_claims.geojson', 'w') as file:
    json.dump(claims_geojson, file)