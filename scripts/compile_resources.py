import json
import csv

in_file = 'resource_desc.json'
out_file = 'resource_desc_small.json'
out_file_csv = 'resource_desc_small.csv'

remove_keys = ['despawn_time', 'max_health', 'on_destroy_yield', 'footprint', 'scheduled_respawn_time', 'ignore_damage', 'compendium_entry', 'not_respawning', 'scheduled_respawn_time', 'flattenable', 'description', 'spawn_priority', 'enemy_params_id', 'model_asset_name', 'rarity', 'on_destroy_yield_resource_id']

def remove_keys_from_dict(d, keys_to_remove):
    if isinstance(d, dict):
        return {k: remove_keys_from_dict(v, keys_to_remove) 
                for k, v in d.items() if k not in keys_to_remove}
    elif isinstance(d, list):
        return [remove_keys_from_dict(item, keys_to_remove) for item in d]
    else:
        return d


with open(in_file, 'r') as file:
    data = json.load(file)

new_json = remove_keys_from_dict(data, remove_keys)

with open(out_file, 'w') as file:
    json.dump(new_json, file, indent=4, separators=(',', ':'))

with open(out_file_csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=new_json[0].keys())
    writer.writeheader()
    writer.writerows(new_json)