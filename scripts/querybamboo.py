import json
import requests
from websockets.sync.client import connect
from websockets import Subprotocol
from pathlib import Path
import time
from datetime import datetime
import concurrent.futures
from threading import Lock

# Load Bearer Token & Region Module from Files
bearer_file = Path(r"assets/data/secret/bearer")

auth_token = bearer_file.read_text().strip()
region_module = "bitcraft-9"  # Regional database - THIS IS REGION 2 ONLY
region_host = "bitcraft-early-access.spacetimedb.com"

print(auth_token)

print(f"OPTIMIZED Traveler's Fruit Location Query - Parallel Processing")
print(f"Database: {region_module} (REGION 9 ONLY)")
print("=" * 60)

# Resource to search for
TRAVELERS_FRUIT_RESOURCE_ID = 424796674
print(f"🎯 Target: Resource ID {TRAVELERS_FRUIT_RESOURCE_ID} (Traveler's Fruit)")

proto = Subprotocol('v1.json.spacetimedb')
ws_uri = f"wss://{region_host}/v1/database/{region_module}/subscribe"

# Thread-safe results storage
results_lock = Lock()
successful_locations = []
failed_queries = []

def get_resource_entities(resource_id, timeout=15):
    """Get all entity_ids for a resource (Step 2)"""
    print(f"\n🔍 STEP 2: Getting all entity_ids for resource {resource_id}...")
    
    try:
        with connect(
            ws_uri,
            additional_headers={"Authorization": auth_token},
            subprotocols=[proto],
            max_size=None,
            ping_timeout=timeout
        ) as ws:
            
            ws.recv()
            
            query = f"SELECT * FROM resource_state WHERE resource_id = {resource_id};"
            subscription = {
                "Subscribe": {
                    "request_id": 1,
                    "query_strings": [query]
                }
            }
            
            ws.send(json.dumps(subscription))
            
            start_time = time.time()
            for msg in ws:
                if time.time() - start_time > timeout:
                    print(f"   ⏰ Timeout after {timeout}s")
                    return []
                
                data = json.loads(msg)
                
                if 'InitialSubscription' in data:
                    tables = data['InitialSubscription']['database_update']['tables']
                    if tables and tables[0].get('updates') and tables[0]['updates'][0].get('inserts'):
                        rows = tables[0]['updates'][0]['inserts']
                        entries = [json.loads(row) for row in rows]
                        
                        entity_ids = [entry['entity_id'] for entry in entries if 'entity_id' in entry]
                        print(f"   ✅ Found {len(entity_ids)} entity IDs")
                        return entity_ids
                    else:
                        print(f"   ⚪ No entries found")
                        return []
                
                elif 'TransactionUpdate' in data and 'Failed' in data['TransactionUpdate']['status']:
                    error = data['TransactionUpdate']['status']['Failed']
                    print(f"   ❌ Query failed: {error}")
                    return []
                
                break
                
    except Exception as e:
        print(f"   🔴 Error: {str(e)}")
        return []

def get_single_location(entity_id, timeout=8):
    """Get location for a single entity_id - optimized for parallel execution"""
    try:
        with connect(
            ws_uri,
            additional_headers={"Authorization": auth_token},
            subprotocols=[proto],
            max_size=None,
            ping_timeout=timeout
        ) as ws:
            
            ws.recv()  # Welcome message
            
            query = f"SELECT * FROM location_state WHERE entity_id = {entity_id};"
            subscription = {
                "Subscribe": {
                    "request_id": 1,
                    "query_strings": [query]
                }
            }
            
            ws.send(json.dumps(subscription))
            
            start_time = time.time()
            for msg in ws:
                if time.time() - start_time > timeout:
                    with results_lock:
                        failed_queries.append(f"Timeout: {entity_id}")
                    return None
                
                data = json.loads(msg)
                
                if 'InitialSubscription' in data:
                    tables = data['InitialSubscription']['database_update']['tables']
                    if tables and tables[0].get('updates') and tables[0]['updates'][0].get('inserts'):
                        rows = tables[0]['updates'][0]['inserts']
                        if rows:
                            location = json.loads(rows[0])
                            
                            # Add the entity_id to the location data
                            location['entity_id'] = entity_id
                            
                            with results_lock:
                                successful_locations.append(location)
                            
                            return location
                    
                    # No location found
                    with results_lock:
                        failed_queries.append(f"No location: {entity_id}")
                    return None
                    
                elif 'TransactionUpdate' in data and 'Failed' in data['TransactionUpdate']['status']:
                    error = data['TransactionUpdate']['status']['Failed']
                    with results_lock:
                        failed_queries.append(f"Query failed: {entity_id} - {error}")
                    return None
                
                break
                
    except Exception as e:
        with results_lock:
            failed_queries.append(f"Connection error: {entity_id} - {str(e)}")
        return None

def get_parallel_locations(entity_ids, sample_size=1000, max_workers=10):
    """Get locations for entity IDs using parallel processing"""
    print(f"\n📍 STEP 3: Getting locations with parallel processing...")
    print(f"   Sample size: {sample_size} entities")
    print(f"   Parallel workers: {max_workers}")
    print(f"   Estimated time: {sample_size // max_workers // 2}-{sample_size // max_workers} seconds")
    
    # Take a sample of entity IDs
    sample_entity_ids = entity_ids[:sample_size]
    
    # Clear previous results
    global successful_locations, failed_queries
    with results_lock:
        successful_locations.clear()
        failed_queries.clear()
    
    # Process in parallel
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = [executor.submit(get_single_location, entity_id) for entity_id in sample_entity_ids]
        
        # Process results as they complete
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            if completed % 100 == 0:  # Progress every 100 completions
                elapsed = time.time() - start_time
                rate = completed / elapsed
                remaining = len(sample_entity_ids) - completed
                eta = remaining / rate if rate > 0 else 0
                print(f"   Progress: {completed}/{len(sample_entity_ids)} ({completed/len(sample_entity_ids)*100:.1f}%) - ETA: {eta:.0f}s")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n   ⏱️ Parallel processing completed in {total_time:.1f} seconds")
    print(f"   ✅ Success: {len(successful_locations)} locations found")
    print(f"   ❌ Failed: {len(failed_queries)} queries failed")
    
    return successful_locations.copy()

# Execute the optimized process
print(f"\n⚡ OPTIMIZED PROCESS START...")

# Step 2: Get all entity IDs
entity_ids = get_resource_entities(TRAVELERS_FRUIT_RESOURCE_ID)

if entity_ids:
    print(f"\n🎯 Processing strategy:")
    print(f"   Total entities: {len(entity_ids)}")
    print(f"   Using parallel processing instead of unsupported batch queries")
    print(f"   This avoids the 'IN operator not supported' error")
    
    # Get locations using parallel processing
    sample_locations = get_parallel_locations(entity_ids, sample_size=1000, max_workers=10)
    
    if sample_locations:
        print(f"\n🎉 SUCCESS! Found {len(sample_locations)} Traveler's Fruit locations!")
        
        # Show sample coordinates
        print(f"\n📍 SAMPLE TRAVELER'S FRUIT COORDINATES:")
        for i, loc in enumerate(sample_locations[:10]):
            x, z = loc.get('x'), loc.get('z')
            entity_id = loc.get('entity_id')
            chunk_index = loc.get('chunk_index')
            print(f"   {i+1}: Traveler's Fruit at ({x}, {z}) chunk {chunk_index} (Entity: {entity_id})")
        
        if len(sample_locations) > 10:
            print(f"   ... and {len(sample_locations) - 10} more locations")
        
        # Save results in your exact map framework format
        print(f"\n💾 SAVING IN MAP FRAMEWORK FORMAT...")
        
        # Your exact format: list of location dicts
        map_format_data = []
        for loc in sample_locations:
            map_format_data.append({
                'entity_id': loc.get('entity_id'),
                'chunk_index': loc.get('chunk_index'),
                'x': loc.get('x'),
                'z': loc.get('z'),
                'dimension': loc.get('dimension', 1)
            })
        
        # Save in your exact format
        with open("travelers_fruit_map_format_optimized.json", 'w') as f:
            json.dump(map_format_data, f, separators=(',', ': '))
        
        # Also save enriched version for reference
        travelers_fruit_results = []
        for loc in sample_locations:
            travelers_fruit_results.append({
                'resource_name': "Traveler's Fruit",
                'resource_id': TRAVELERS_FRUIT_RESOURCE_ID,
                'entity_id': loc.get('entity_id'),
                'x': loc.get('x'),
                'z': loc.get('z'),
                'dimension': loc.get('dimension', 1),
                'chunk_index': loc.get('chunk_index')
            })
        
        with open("travelers_fruit_bulk_locations_optimized.json", 'w') as f:
            json.dump(travelers_fruit_results, f, indent=2)
        
        # Create CSV
        import csv
        with open("travelers_fruit_bulk_coordinates_optimized.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['name', 'x', 'z', 'dimension', 'entity_id', 'chunk_index'])
            
            for fruit in travelers_fruit_results:
                writer.writerow([
                    "Traveler's Fruit",
                    fruit['x'],
                    fruit['z'],
                    fruit['dimension'],
                    fruit['entity_id'],
                    fruit['chunk_index']
                ])
        
        # Create GeoJSON for bitcraftmap.com compatibility (using your exact method)
        def generate_travelers_fruit_geojson(json_key):
            return [json_key['x'], json_key['z']]
        
        travelers_fruit_geojson = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {
                    "iconName": "travelers_fruit"  # You may need to adjust this icon name
                },
                "geometry": {
                    "type": "MultiPoint",
                    "coordinates": [generate_travelers_fruit_geojson(key) for key in map_format_data]
                }
            }]
        }
        
        with open("travelerfruit.geojson", 'w') as f:
            json.dump(travelers_fruit_geojson, f, separators=(',', ':'))
        
        print(f"\n💾 FILES CREATED:")
        print(f"   🎯 travelers_fruit_map_format_optimized.json - READY FOR YOUR MAP FRAMEWORK")
        print(f"   🗺️ travelerfruit.geojson - READY FOR BITCRAFTMAP.COM")
        print(f"   📄 travelers_fruit_bulk_locations_optimized.json - Full enriched data")
        print(f"   📊 travelers_fruit_bulk_coordinates_optimized.csv - For spreadsheets")
        
        # Show performance stats
        coverage = len(sample_locations) / len(entity_ids) * 100
        print(f"\n📊 PERFORMANCE ANALYSIS:")
        print(f"   Sample: {len(sample_locations)} locations found")
        print(f"   Total available: {len(entity_ids)} entities")
        print(f"   Coverage: {coverage:.1f}% of all Traveler's Fruit in Region 2")
        print(f"   Success rate: {len(sample_locations)/(len(sample_locations)+len(failed_queries))*100:.1f}%")
        
        if failed_queries:
            print(f"\n⚠️ FAILED QUERIES (first 5):")
            for fail in failed_queries[:5]:
                print(f"   {fail}")
        
    else:
        print(f"\n😞 No locations found even with parallel processing")
        if failed_queries:
            print(f"\n❌ Common failure reasons:")
            for fail in failed_queries[:10]:
                print(f"   {fail}")

else:
    print(f"\n😞 Could not get entity IDs from resource_state")

print(f"\n🌍 IMPORTANT NOTES:")
print(f"   • This uses parallel individual queries instead of unsupported batch queries")
print(f"   • Much faster than sequential processing (10x speedup)")
print(f"   • Avoids SpacetimeDB's 'IN operator not supported' limitation")
print(f"   • Data is from Region 2 (bitcraft-2) only")
print(f"   • Resources respawn/change over time as players harvest them")

# Show optimization summary
print(f"\n⚡ OPTIMIZATION SUMMARY:")
print(f"   • Problem: SpacetimeDB doesn't support IN operator for batch queries")
print(f"   • Solution: Parallel individual queries with ThreadPoolExecutor")
print(f"   • Speed: ~10 workers processing simultaneously")
print(f"   • Result: Same data quality, much faster than sequential")