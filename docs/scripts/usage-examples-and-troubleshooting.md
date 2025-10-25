# Usage Examples and Troubleshooting Guide

## Overview

This comprehensive guide provides practical usage examples, common workflows, and troubleshooting solutions for the BitCraft Map scripts ecosystem. It serves as a practical handbook for developers, system administrators, and contributors working with the data processing pipeline.

## Quick Start Guide

### Environment Setup
```bash
# 1. Clone the repository
git clone https://github.com/your-repo/bitcraftmap.git
cd bitcraftmap

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r scripts/requirements.txt

# 4. Verify installation
python -c "import requests, numpy, cv2, PIL; print('Dependencies installed successfully')"
```

### First Run - Basic Data Processing
```bash
# Generate basic map data (no external dependencies required)
python scripts/generate_grids_geojson.py
python scripts/generate_icons_manifest.py

# Verify outputs
ls -la assets/markers/grids.geojson
ls -la assets/images/manifest.js
```

## Common Workflows

### Complete Map Data Pipeline
```bash
#!/bin/bash
# complete_map_update.sh - Full data processing pipeline

echo "=== BitCraft Map Data Update Pipeline ==="
start_time=$(date +%s)

# Step 1: Asset Management
echo "[1/7] Processing assets..."
python scripts/generate_assets.py 2>/dev/null || echo "Note: Asset flattening requires source directory"
python scripts/generate_icons_manifest.py

# Step 2: API Data Processing (requires internet)
echo "[2/7] Fetching claims data..."
if python scripts/generate_claims_geojson.py; then
    echo "✓ Claims data updated"
else
    echo "⚠ Claims data failed - check internet connection"
fi

# Step 3: Jobs Data (requires internet)
echo "[3/7] Fetching jobs data..."
if python scripts/generate_jobs_geojson.py; then
    echo "✓ Jobs data updated"
else
    echo "⚠ Jobs data failed - check API availability"
fi

# Step 4: Static POI Processing
echo "[4/7] Processing POI data..."
if [ -f "assets/data/caves.json" ]; then
    python scripts/static_poi_to_geojson.py
    echo "✓ POI data processed"
else
    echo "⚠ POI data skipped - caves.json not found"
fi

# Step 5: Grid Generation
echo "[5/7] Generating map grids..."
python scripts/generate_grids_geojson.py

# Step 6: Terrain Processing (requires internet)
echo "[6/7] Processing terrain maps..."
if python scripts/generate_terrain_map.py; then
    echo "✓ Terrain maps generated"
else
    echo "⚠ Terrain processing failed - check internet connection"
fi

# Step 7: Road Networks (requires local API servers)
echo "[7/7] Generating road networks..."
if ./scripts/roads.sh 2>/dev/null; then
    echo "✓ Road networks updated"
else
    echo "⚠ Road generation skipped - requires local API servers"
fi

# Summary
end_time=$(date +%s)
duration=$((end_time - start_time))
echo "=== Pipeline completed in ${duration}s ==="

# Check outputs
echo "Generated files:"
find assets/markers -name "*.geojson" -exec basename {} \; | sort
```

### Incremental Updates Workflow
```bash
#!/bin/bash
# incremental_update.sh - Update only essential data

# Check what needs updating based on file ages
CACHE_HOURS=6
CURRENT_TIME=$(date +%s)
CACHE_SECONDS=$((CACHE_HOURS * 3600))

check_file_age() {
    local file=$1
    if [ -f "$file" ]; then
        local file_time=$(stat -f %m "$file" 2>/dev/null || stat -c %Y "$file")
        local age=$((CURRENT_TIME - file_time))
        if [ $age -lt $CACHE_SECONDS ]; then
            return 0  # File is fresh
        fi
    fi
    return 1  # File needs update
}

echo "=== Incremental Map Data Update ==="

# Claims data (updates frequently)
if ! check_file_age "assets/markers/claims.geojson"; then
    echo "Updating claims data..."
    python scripts/generate_claims_geojson.py
fi

# Jobs data (updates frequently)  
if ! check_file_age "jobs.geojson"; then
    echo "Updating jobs data..."
    python scripts/generate_jobs_geojson.py
fi

# Icon manifest (only when assets change)
if [ "assets/images/" -nt "assets/images/manifest.js" ]; then
    echo "Updating icon manifest..."
    python scripts/generate_icons_manifest.py
fi

echo "Incremental update complete"
```

### Development Workflow
```bash
#!/bin/bash
# dev_workflow.sh - Development and testing workflow

# Set development environment
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$(pwd)/scripts:$PYTHONPATH"

# Function to run script with error checking
run_script() {
    local script=$1
    local description=$2
    echo "Testing: $description"
    
    if python scripts/$script; then
        echo "✓ $script passed"
        return 0
    else
        echo "✗ $script failed"
        return 1
    fi
}

echo "=== Development Testing Workflow ==="

# Test scripts that don't require external dependencies
run_script "generate_grids_geojson.py" "Grid generation"
run_script "generate_icons_manifest.py" "Icon manifest creation"

# Test scripts with mock data
if [ -f "test_data/mock_caves.json" ]; then
    cp test_data/mock_caves.json assets/data/caves.json
    run_script "static_poi_to_geojson.py" "POI processing with mock data"
fi

# Validate outputs
echo "Validating GeoJSON outputs..."
for file in assets/markers/*.geojson; do
    if python -c "import json; json.load(open('$file'))"; then
        echo "✓ $file is valid JSON"
    else
        echo "✗ $file is invalid JSON"
    fi
done

echo "Development testing complete"
```

## Script-Specific Examples

### Claims Processing with Custom Parameters
```python
# custom_claims_processing.py - Enhanced claims processing
import sys
import time
import requests
import json
from scripts.generate_claims_geojson import generate_claims_json

# Custom configuration
CUSTOM_CONFIG = {
    'api_url': 'https://bitjita.com/api/claims/',
    'rate_limit': 0.2,  # Faster processing
    'batch_size': 200,  # Larger batches
    'user_agent': {'User-agent': 'CustomMapProcessor v1.0'},
    'timeout': 45,
    'max_retries': 3
}

def enhanced_claims_processing():
    """Enhanced claims processing with retry logic and progress tracking"""
    
    def fetch_with_retry(url, config, max_retries=3):
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    url, 
                    headers=config['user_agent'],
                    timeout=config['timeout']
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"Request failed (attempt {attempt + 1}), retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
    
    # Get initial metadata with retry
    initial_url = f"{CUSTOM_CONFIG['api_url']}?limit=1&page=1"
    data = fetch_with_retry(initial_url, CUSTOM_CONFIG)
    total_claims = int(data['count'])
    total_pages = math.ceil(total_claims / CUSTOM_CONFIG['batch_size'])
    
    print(f"Processing {total_claims} claims across {total_pages} pages")
    
    all_claims = []
    start_time = time.time()
    
    # Fetch all pages with progress tracking
    for page in range(1, total_pages + 1):
        page_url = f"{CUSTOM_CONFIG['api_url']}?limit={CUSTOM_CONFIG['batch_size']}&page={page}"
        
        page_data = fetch_with_retry(page_url, CUSTOM_CONFIG)
        all_claims.extend(page_data['claims'])
        
        # Progress reporting
        progress = (page / total_pages) * 100
        elapsed = time.time() - start_time
        eta = (elapsed / page) * (total_pages - page)
        
        print(f"Progress: {progress:.1f}% ({page}/{total_pages}) - ETA: {eta:.1f}s")
        
        time.sleep(CUSTOM_CONFIG['rate_limit'])
    
    print(f"Claims fetch completed in {time.time() - start_time:.1f}s")
    return all_claims

if __name__ == "__main__":
    try:
        claims = enhanced_claims_processing()
        print(f"Successfully processed {len(claims)} claims")
    except Exception as e:
        print(f"Processing failed: {e}")
        sys.exit(1)
```

### Terrain Processing with Custom Parameters
```python
# custom_terrain_processing.py - Advanced terrain processing
import numpy as np
import cv2
from PIL import Image
from scripts.generate_terrain_map import *

def process_terrain_with_custom_settings():
    """Process terrain with custom hexagon sizes and styles"""
    
    # Custom configuration
    configs = [
        {"name": "detailed", "hex_size": 4, "scale": 15, "suffix": "detailed"},
        {"name": "standard", "hex_size": 6, "scale": 10, "suffix": "standard"},  
        {"name": "overview", "hex_size": 12, "scale": 5, "suffix": "overview"}
    ]
    
    # Load base terrain image
    base_img = cv2.imread(f'{data_folder}TerrainMap.gwm.png')
    if base_img is None:
        print("Error: Base terrain image not found")
        return
    
    h, w = base_img.shape[:2]
    
    for config in configs:
        print(f"Generating {config['name']} terrain...")
        
        hex_size = config['hex_size']
        scale = config['scale']
        
        # Create output image
        out_h = int(h * scale)
        out_w = int(w * scale)
        result = np.zeros((out_h, out_w, 3), dtype=np.uint8)
        
        # Hexagon spacing
        dx = math.sqrt(3) * hex_size
        dy = 1.5 * hex_size
        
        total_hexagons = int((out_h / dy) * (out_w / dx))
        processed = 0
        
        # Generate hexagons with progress tracking
        for y in np.arange(0, out_h + dy, dy):
            for x in np.arange(0, out_w + dx, dx):
                offset = dx / 2 if int(y // dy) % 2 else 0
                cx = x + offset
                cy = y
                
                # Map to source image
                orig_x = int(cx / scale)
                orig_y = int(cy / scale)
                
                if 0 <= orig_x < w and 0 <= orig_y < h:
                    color = tuple(int(c) for c in base_img[orig_y, orig_x])
                    
                    # Generate hexagon vertices
                    pts = []
                    for i in range(6):
                        angle = math.pi / 6 + math.pi / 3 * i
                        px = int(cx + hex_size * math.cos(angle))
                        py = int(cy + hex_size * math.sin(angle))
                        pts.append([px, py])
                    
                    pts = np.array([pts], dtype=np.int32)
                    cv2.fillPoly(result, pts, color)
                
                processed += 1
                if processed % 1000 == 0:
                    progress = (processed / total_hexagons) * 100
                    print(f"  Progress: {progress:.1f}%")
        
        # Save with custom suffix
        output_file = f'{data_folder}TerrainMap_{config["suffix"]}.png'
        cv2.imwrite(output_file, result)
        print(f"✓ Saved {config['name']} terrain: {output_file}")

if __name__ == "__main__":
    process_terrain_with_custom_settings()
```

### POI Processing with Validation
```python
# validated_poi_processing.py - POI processing with comprehensive validation
import json
import os
from collections import defaultdict
from scripts.static_poi_to_geojson import *

def validate_poi_data():
    """Comprehensive POI data validation"""
    
    # Check input file
    input_file = 'assets/data/caves.json'
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found")
        return False
    
    # Load and validate JSON structure
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {input_file}: {e}")
        return False
    
    if not isinstance(data, list):
        print("Error: Input data must be a list")
        return False
    
    # Validate individual POI records
    validation_stats = {
        'total_records': len(data),
        'valid_records': 0,
        'missing_name': 0,
        'missing_location': 0,
        'invalid_coordinates': 0,
        'categories': defaultdict(int)
    }
    
    for i, poi in enumerate(data):
        # Check required fields
        if not isinstance(poi, dict):
            continue
            
        if 'name' not in poi:
            validation_stats['missing_name'] += 1
            continue
            
        if 'location' not in poi:
            validation_stats['missing_location'] += 1
            continue
            
        location = poi['location']
        if 'x' not in location or 'z' not in location:
            validation_stats['missing_location'] += 1
            continue
        
        # Validate coordinates
        try:
            x, z = float(location['x']), float(location['z'])
            if not (-50000 <= x <= 50000) or not (-50000 <= z <= 50000):
                validation_stats['invalid_coordinates'] += 1
                continue
        except (ValueError, TypeError):
            validation_stats['invalid_coordinates'] += 1
            continue
        
        # Categorize POI
        name = poi['name']
        if 'Cave' in name:
            validation_stats['categories']['caves'] += 1
        elif 'Tree' in name:
            validation_stats['categories']['trees'] += 1
        elif 'Temple' in name:
            validation_stats['categories']['temples'] += 1
        else:
            validation_stats['categories']['ruined'] += 1
        
        validation_stats['valid_records'] += 1
    
    # Print validation results
    print("=== POI Data Validation Results ===")
    print(f"Total records: {validation_stats['total_records']}")
    print(f"Valid records: {validation_stats['valid_records']}")
    print(f"Missing name: {validation_stats['missing_name']}")
    print(f"Missing location: {validation_stats['missing_location']}")
    print(f"Invalid coordinates: {validation_stats['invalid_coordinates']}")
    print("\nCategory distribution:")
    for category, count in validation_stats['categories'].items():
        print(f"  {category}: {count}")
    
    success_rate = (validation_stats['valid_records'] / validation_stats['total_records']) * 100
    print(f"\nValidation success rate: {success_rate:.1f}%")
    
    return success_rate > 90  # Require 90% success rate

def process_poi_with_validation():
    """Process POI data with validation steps"""
    
    if not validate_poi_data():
        print("Validation failed - aborting POI processing")
        return False
    
    print("Validation passed - processing POI data...")
    
    try:
        # Run original POI processing
        exec(open('scripts/static_poi_to_geojson.py').read())
        
        # Validate outputs
        output_files = [
            'assets/markers/caves.geojson',
            'assets/markers/trees.geojson',
            'assets/markers/temples.geojson',
            'assets/markers/ruined.geojson'
        ]
        
        for file_path in output_files:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                print(f"✓ {os.path.basename(file_path)}: {len(data)} features")
            else:
                print(f"✗ {os.path.basename(file_path)}: Missing")
        
        print("POI processing completed successfully")
        return True
        
    except Exception as e:
        print(f"POI processing failed: {e}")
        return False

if __name__ == "__main__":
    process_poi_with_validation()
```

## Troubleshooting Common Issues

### Installation and Setup Issues

#### 1. Dependency Installation Failures

**Problem**: Package installation fails with compilation errors
```bash
# Error examples:
# "Microsoft Visual C++ 14.0 is required"
# "error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools""
# "Failed building wheel for opencv-python"
```

**Solutions**:
```bash
# Solution 1: Install pre-compiled wheels
pip install --only-binary=all opencv-python pillow numpy

# Solution 2: Use conda instead of pip
conda install -c conda-forge opencv pillow numpy matplotlib pandas requests

# Solution 3: Install Microsoft Visual C++ Build Tools (Windows)
# Download and install from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Solution 4: Use alternative packages
pip install opencv-python-headless  # Headless version
pip install Pillow-SIMD            # Optimized Pillow
```

#### 2. Python Version Compatibility

**Problem**: Scripts fail with Python version errors
```python
# Error: "SyntaxError: f-string is only available in Python 3.6+"
# Error: "AttributeError: module 'asyncio' has no attribute 'run'"
```

**Solutions**:
```bash
# Check Python version
python --version

# Install Python 3.8+ if needed
# Windows: Download from python.org
# macOS: brew install python@3.9
# Ubuntu: sudo apt install python3.9

# Use specific Python version
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Path and Import Issues

**Problem**: Module not found errors
```python
# Error: "ModuleNotFoundError: No module named 'scripts.generate_claims_geojson'"
# Error: "FileNotFoundError: [Errno 2] No such file or directory"
```

**Solutions**:
```bash
# Ensure correct working directory
cd /path/to/bitcraftmap
pwd  # Should show bitcraftmap directory

# Set PYTHONPATH if needed
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Use absolute paths in scripts
python /full/path/to/scripts/generate_claims_geojson.py

# Check file permissions
ls -la scripts/
chmod +x scripts/*.py
```

### Runtime Issues

#### 1. Network and API Problems

**Problem**: API requests fail or timeout
```python
# Error: "requests.exceptions.ConnectionError: HTTPSConnectionPool"
# Error: "requests.exceptions.Timeout: HTTPSConnectionPool"
# Error: "requests.exceptions.HTTPError: 429 Client Error: Too Many Requests"
```

**Solutions**:
```python
# Enhanced error handling in custom script
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_robust_session():
    session = requests.Session()
    
    # Retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

# Usage in scripts
session = create_robust_session()
response = session.get(url, timeout=(10, 300))  # (connect, read) timeout
```

```bash
# Check internet connectivity
ping google.com
curl -I https://bitjita.com/api/claims/

# Test API endpoints
curl -H "User-agent: BitCraftMap" "https://bitjita.com/api/claims/?limit=1"
```

#### 2. Memory Issues

**Problem**: Out of memory errors during processing
```python
# Error: "MemoryError: Unable to allocate array"
# Error: "Killed" (Linux OOM killer)
```

**Solutions**:
```python
# Monitor memory usage
import psutil
import gc

def monitor_memory():
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage: {memory_mb:.1f} MB")
    return memory_mb

# Implement memory management
def process_with_memory_management(large_dataset):
    chunk_size = 1000
    results = []
    
    for i in range(0, len(large_dataset), chunk_size):
        chunk = large_dataset[i:i+chunk_size]
        
        # Process chunk
        processed_chunk = process_chunk(chunk)
        results.extend(processed_chunk)
        
        # Clean up
        del chunk, processed_chunk
        gc.collect()
        
        if monitor_memory() > 1000:  # 1GB limit
            print("Memory limit reached, forcing cleanup")
            gc.collect()
    
    return results
```

```bash
# Increase system limits (Linux)
ulimit -v 4194304  # 4GB virtual memory limit

# Monitor system resources
htop  # Interactive process viewer
free -m  # Memory usage

# Use memory-efficient alternatives
python scripts/generate_terrain_map.py  # Use smaller batch sizes
```

#### 3. File I/O Problems

**Problem**: File access and permission errors
```python
# Error: "PermissionError: [Errno 13] Permission denied"
# Error: "FileNotFoundError: [Errno 2] No such file or directory"
# Error: "OSError: [Errno 28] No space left on device"
```

**Solutions**:
```bash
# Check disk space
df -h

# Check permissions
ls -la assets/
chmod 755 assets/
chmod 644 assets/markers/*.geojson

# Create missing directories
mkdir -p assets/{data,markers,images}

# Check file locks (Windows)
# Close other applications that might be using the files
```

### Data Processing Issues

#### 1. Invalid GeoJSON Output

**Problem**: Generated GeoJSON files are invalid
```javascript
// Error: "Unexpected token in JSON at position 0"
// Error: "Invalid GeoJSON: coordinates must be an array"
```

**Validation and fixes**:
```python
# geojson_validator.py
import json
import os

def validate_geojson_file(file_path):
    """Validate GeoJSON file structure"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Basic structure validation
        if isinstance(data, list):
            # Array of features
            for i, feature in enumerate(data):
                if not validate_feature(feature):
                    print(f"Invalid feature at index {i}")
                    return False
        elif isinstance(data, dict):
            # FeatureCollection
            if data.get('type') != 'FeatureCollection':
                print("Missing FeatureCollection type")
                return False
            
            features = data.get('features', [])
            for i, feature in enumerate(features):
                if not validate_feature(feature):
                    print(f"Invalid feature at index {i}")
                    return False
        else:
            print("Invalid GeoJSON root structure")
            return False
        
        print(f"✓ {file_path} is valid GeoJSON")
        return True
        
    except json.JSONDecodeError as e:
        print(f"✗ {file_path} contains invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"✗ Error validating {file_path}: {e}")
        return False

def validate_feature(feature):
    """Validate individual GeoJSON feature"""
    if not isinstance(feature, dict):
        return False
    
    if feature.get('type') != 'Feature':
        return False
    
    geometry = feature.get('geometry')
    if not geometry or not isinstance(geometry, dict):
        return False
    
    geom_type = geometry.get('type')
    coords = geometry.get('coordinates')
    
    if not geom_type or not coords:
        return False
    
    # Validate coordinate structure based on geometry type
    if geom_type == 'Point':
        return (isinstance(coords, list) and len(coords) >= 2 and
                all(isinstance(c, (int, float)) for c in coords[:2]))
    elif geom_type in ['LineString', 'MultiPoint']:
        return (isinstance(coords, list) and len(coords) > 0 and
                all(isinstance(point, list) and len(point) >= 2 for point in coords))
    # Add more geometry types as needed
    
    return True

# Validate all generated GeoJSON files
for file_path in ['assets/markers/caves.geojson', 'assets/markers/trees.geojson']:
    if os.path.exists(file_path):
        validate_geojson_file(file_path)
```

#### 2. Coordinate System Issues

**Problem**: POI locations appear in wrong places on map
```python
# Symptoms: Markers in ocean, coordinates out of bounds
# Cause: Coordinate system mismatch or transformation errors
```

**Debugging and fixes**:
```python
# coordinate_debugger.py
import json

def analyze_coordinates(geojson_file):
    """Analyze coordinate ranges in GeoJSON file"""
    with open(geojson_file, 'r') as f:
        data = json.load(f)
    
    coordinates = []
    features = data if isinstance(data, list) else data.get('features', [])
    
    for feature in features:
        geom = feature.get('geometry', {})
        coords = geom.get('coordinates')
        if coords and geom.get('type') == 'Point':
            coordinates.append(coords)
    
    if coordinates:
        x_coords = [c[0] for c in coordinates]
        z_coords = [c[1] for c in coordinates]
        
        print(f"=== Coordinate Analysis: {geojson_file} ===")
        print(f"Total points: {len(coordinates)}")
        print(f"X range: {min(x_coords):.2f} to {max(x_coords):.2f}")
        print(f"Z range: {min(z_coords):.2f} to {max(z_coords):.2f}")
        print(f"Sample coordinates: {coordinates[:3]}")
        
        # Check for common issues
        if any(abs(x) > 50000 for x in x_coords):
            print("⚠ Warning: X coordinates exceed expected range")
        if any(abs(z) > 50000 for z in z_coords):
            print("⚠ Warning: Z coordinates exceed expected range")
        
        # Check for coordinate system indicators
        if all(-180 <= x <= 180 for x in x_coords) and all(-90 <= z <= 90 for z in z_coords):
            print("📍 Appears to be geographic coordinates (lat/lon)")
        elif all(x >= 0 and z >= 0 for x in x_coords for z in z_coords):
            print("📍 Appears to be positive quadrant coordinates")
        else:
            print("📍 Appears to be game world coordinates")

# Analyze all coordinate files
for file_path in ['assets/markers/caves.geojson', 'assets/markers/claims.geojson']:
    if os.path.exists(file_path):
        analyze_coordinates(file_path)
```

### Performance Issues

#### 1. Slow Processing Times

**Problem**: Scripts take too long to complete
```python
# Symptoms: Hours to process data that should take minutes
# Common causes: Inefficient algorithms, memory swapping, network delays
```

**Performance optimization**:
```python
# performance_profiler.py
import time
import cProfile
import pstats
from functools import wraps

def profile_function(func):
    """Decorator to profile function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        pr.disable()
        
        print(f"Function {func.__name__} took {end_time - start_time:.2f} seconds")
        
        # Print top time consumers
        stats = pstats.Stats(pr)
        stats.sort_stats('cumulative')
        stats.print_stats(10)
        
        return result
    return wrapper

# Usage example
@profile_function
def process_claims_data():
    # Your processing logic here
    pass

# Optimization strategies
def optimize_api_requests():
    """Optimize API request patterns"""
    # Use session for connection reuse
    session = requests.Session()
    
    # Implement batch processing
    batch_size = 100
    
    # Use async requests for parallel processing
    import asyncio
    import aiohttp
    
    async def fetch_batch(session, urls):
        tasks = []
        for url in urls:
            tasks.append(session.get(url))
        responses = await asyncio.gather(*tasks)
        return responses
```

#### 2. Large File Handling

**Problem**: Processing large files causes system slowdown
```python
# Symptoms: System becomes unresponsive, swap usage increases
# Files: Large terrain maps, comprehensive POI datasets
```

**Streaming solutions**:
```python
# streaming_processor.py
import json
from collections.abc import Iterator

def stream_json_array(file_path: str, chunk_size: int = 1024) -> Iterator[dict]:
    """Stream large JSON arrays without loading entire file into memory"""
    with open(file_path, 'r', encoding='utf-8') as f:
        buffer = ""
        in_object = False
        brace_count = 0
        
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            
            buffer += chunk
            
            # Simple JSON object extraction
            i = 0
            while i < len(buffer):
                char = buffer[i]
                
                if char == '{' and not in_object:
                    in_object = True
                    brace_count = 1
                    start_pos = i
                elif in_object:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        
                        if brace_count == 0:
                            # Complete object found
                            obj_str = buffer[start_pos:i+1]
                            try:
                                obj = json.loads(obj_str)
                                yield obj
                            except json.JSONDecodeError:
                                pass  # Skip malformed objects
                            
                            in_object = False
                            buffer = buffer[i+1:]
                            i = -1
                
                i += 1

def process_large_file_streaming(file_path: str):
    """Process large files using streaming approach"""
    processed_count = 0
    
    for obj in stream_json_array(file_path):
        # Process individual object
        process_single_object(obj)
        
        processed_count += 1
        if processed_count % 1000 == 0:
            print(f"Processed {processed_count} objects...")

def chunk_file_processing(file_path: str, chunk_size: int = 10000):
    """Process files in chunks to manage memory usage"""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    total_items = len(data)
    results = []
    
    for i in range(0, total_items, chunk_size):
        chunk = data[i:i + chunk_size]
        
        # Process chunk
        chunk_results = process_data_chunk(chunk)
        results.extend(chunk_results)
        
        # Progress reporting
        progress = min(i + chunk_size, total_items)
        print(f"Progress: {progress}/{total_items} ({100 * progress / total_items:.1f}%)")
        
        # Memory cleanup
        del chunk, chunk_results
        gc.collect()
    
    return results
```

## Monitoring and Maintenance

### Health Check Scripts

```bash
#!/bin/bash
# health_check.sh - Comprehensive system health check

echo "=== BitCraft Map Scripts Health Check ==="
echo "Timestamp: $(date)"
echo

# Check Python environment
echo "--- Python Environment ---"
python --version
pip --version
echo "Virtual environment: ${VIRTUAL_ENV:-Not active}"
echo

# Check dependencies
echo "--- Dependencies ---"
missing_deps=0
for package in requests numpy opencv-python pillow pandas matplotlib; do
    if python -c "import ${package//-/_}" 2>/dev/null; then
        echo "✓ $package"
    else
        echo "✗ $package (missing)"
        ((missing_deps++))
    fi
done
echo

# Check directory structure
echo "--- Directory Structure ---"
for dir in assets assets/data assets/markers assets/images scripts; do
    if [ -d "$dir" ]; then
        echo "✓ $dir/"
    else
        echo "✗ $dir/ (missing)"
        mkdir -p "$dir" && echo "  Created $dir/"
    fi
done
echo

# Check output files
echo "--- Output Files ---"
files_found=0
total_files=0
for file in assets/markers/*.geojson assets/images/manifest.js; do
    ((total_files++))
    if [ -f "$file" ]; then
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file")
        echo "✓ $(basename "$file") (${size} bytes)"
        ((files_found++))
    else
        echo "✗ $(basename "$file") (missing)"
    fi
done
echo

# Check API connectivity
echo "--- API Connectivity ---"
if curl -s --max-time 10 "https://bitjita.com/api/claims/?limit=1" >/dev/null; then
    echo "✓ BitJita API accessible"
else
    echo "✗ BitJita API inaccessible"
fi

if curl -s --max-time 10 "https://maps.game.bitcraftonline.com/world-maps/" >/dev/null; then
    echo "✓ BitCraft terrain server accessible"
else
    echo "✗ BitCraft terrain server inaccessible"
fi
echo

# Check local API servers (for roads)
echo "--- Local API Servers ---"
local_apis_running=0
for port in {4001..4009}; do
    if curl -s --max-time 2 "http://localhost:$port/paved" >/dev/null 2>&1; then
        ((local_apis_running++))
    fi
done
echo "Local APIs running: $local_apis_running/9"
echo

# Summary
echo "=== Health Check Summary ==="
echo "Missing dependencies: $missing_deps"
echo "Output files found: $files_found/$total_files"
echo "Local APIs running: $local_apis_running/9"
echo

# Overall status
if [ $missing_deps -eq 0 ] && [ $files_found -gt 0 ]; then
    echo "✅ System status: HEALTHY"
    exit 0
else
    echo "⚠️  System status: ISSUES DETECTED"
    exit 1
fi
```

### Automated Testing

```python
# test_scripts.py - Automated testing for all scripts
import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock

class TestScriptFunctionality(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create test directory structure
        os.makedirs('assets/data', exist_ok=True)
        os.makedirs('assets/markers', exist_ok=True)
        os.makedirs('assets/images', exist_ok=True)
        
        # Create mock data files
        self.create_mock_data()
    
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def create_mock_data(self):
        """Create mock data files for testing"""
        # Mock caves.json
        mock_caves = [
            {"name": "Ferralith Cave", "location": {"x": 1000, "z": 2000}},
            {"name": "Large Pyrelite Cave", "location": {"x": 3000, "z": 4000}},
            {"name": "Ancient Tree", "location": {"x": 5000, "z": 6000}},
            {"name": "Temple of Wisdom", "location": {"x": 7000, "z": 8000}},
            {"name": "Ruined Settlement", "location": {"x": 9000, "z": 10000}}
        ]
        
        with open('assets/data/caves.json', 'w') as f:
            json.dump(mock_caves, f)
        
        # Mock image files
        os.makedirs('assets/images/ore', exist_ok=True)
        for i in range(1, 11):
            with open(f'assets/images/ore/t{i}.png', 'w') as f:
                f.write(f'mock_image_t{i}')
    
    def test_grid_generation(self):
        """Test grid generation script"""
        from scripts.generate_grids_geojson import main
        
        # This should not raise any exceptions
        main()
        
        # Check output file exists and has valid structure
        self.assertTrue(os.path.exists('assets/markers/grids.geojson'))
        
        with open('assets/markers/grids.geojson', 'r') as f:
            data = json.load(f)
        
        self.assertEqual(data['type'], 'FeatureCollection')
        self.assertGreater(len(data['features']), 0)
    
    def test_poi_processing(self):
        """Test POI processing script"""
        from scripts.static_poi_to_geojson import main
        
        # This should process our mock data
        main()
        
        # Check output files
        expected_files = [
            'assets/markers/caves.geojson',
            'assets/markers/trees.geojson',
            'assets/markers/temples.geojson',
            'assets/markers/ruined.geojson'
        ]
        
        for file_path in expected_files:
            self.assertTrue(os.path.exists(file_path), f"Missing {file_path}")
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            self.assertIsInstance(data, list)
    
    def test_icon_manifest_generation(self):
        """Test icon manifest generation"""
        from scripts.generate_icons_manifest import main
        
        main()
        
        # Check manifest file
        self.assertTrue(os.path.exists('assets/images/manifest.js'))
        
        with open('assets/images/manifest.js', 'r') as f:
            content = f.read()
        
        self.assertIn('const iconsManifest =', content)
        self.assertIn('t1', content)  # Should include our mock icons
    
    @patch('requests.get')
    def test_claims_processing_with_mock(self, mock_get):
        """Test claims processing with mocked API"""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'count': '2',
            'claims': [
                {
                    'entityId': 123,
                    'name': 'Test Town',
                    'tier': 3,
                    'locationX': 1000,
                    'locationZ': 2000
                },
                {
                    'entityId': 456,
                    'name': 'Another Town',
                    'tier': 5,
                    'locationX': 3000,
                    'locationZ': 4000
                }
            ]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # This test would require adapting the claims script to be testable
        # For now, we just verify the mock setup works
        response = mock_get('https://test.api/claims')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], '2')

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
```

### Performance Monitoring

```python
# performance_monitor.py - Monitor script performance over time
import time
import json
import psutil
import subprocess
from datetime import datetime, timedelta
from collections import defaultdict

class PerformanceMonitor:
    def __init__(self):
        self.metrics = defaultdict(list)
        self.log_file = 'performance_log.json'
        self.load_existing_metrics()
    
    def load_existing_metrics(self):
        """Load existing performance metrics"""
        try:
            with open(self.log_file, 'r') as f:
                self.metrics = json.load(f)
        except FileNotFoundError:
            pass
    
    def save_metrics(self):
        """Save performance metrics to file"""
        with open(self.log_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def run_script_with_monitoring(self, script_name, script_path):
        """Run a script and collect performance metrics"""
        print(f"Monitoring {script_name}...")
        
        start_time = time.time()
        start_memory = psutil.virtual_memory().used
        start_cpu = psutil.cpu_percent()
        
        try:
            # Run script
            result = subprocess.run(
                ['python', script_path],
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            
            end_time = time.time()
            end_memory = psutil.virtual_memory().used
            end_cpu = psutil.cpu_percent()
            
            # Calculate metrics
            execution_time = end_time - start_time
            memory_delta = end_memory - start_memory
            avg_cpu = (start_cpu + end_cpu) / 2
            
            # Record metrics
            metric = {
                'timestamp': datetime.now().isoformat(),
                'execution_time': execution_time,
                'memory_delta_mb': memory_delta / (1024 * 1024),
                'avg_cpu_percent': avg_cpu,
                'exit_code': result.returncode,
                'stdout_lines': len(result.stdout.splitlines()),
                'stderr_lines': len(result.stderr.splitlines())
            }
            
            self.metrics[script_name].append(metric)
            
            # Print results
            print(f"✓ {script_name} completed in {execution_time:.2f}s")
            print(f"  Memory delta: {memory_delta / (1024 * 1024):.1f} MB")
            print(f"  Average CPU: {avg_cpu:.1f}%")
            print(f"  Exit code: {result.returncode}")
            
            if result.returncode != 0:
                print(f"  STDERR: {result.stderr[:200]}...")
            
            return metric
            
        except subprocess.TimeoutExpired:
            print(f"✗ {script_name} timed out after 1 hour")
            return None
        except Exception as e:
            print(f"✗ {script_name} failed: {e}")
            return None
    
    def analyze_performance_trends(self, script_name, days=30):
        """Analyze performance trends for a script"""
        if script_name not in self.metrics:
            print(f"No metrics found for {script_name}")
            return
        
        # Filter recent metrics
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_metrics = [
            m for m in self.metrics[script_name]
            if datetime.fromisoformat(m['timestamp']) > cutoff_date
        ]
        
        if not recent_metrics:
            print(f"No recent metrics found for {script_name}")
            return
        
        # Calculate statistics
        execution_times = [m['execution_time'] for m in recent_metrics]
        memory_deltas = [m['memory_delta_mb'] for m in recent_metrics]
        
        print(f"=== Performance Analysis: {script_name} (last {days} days) ===")
        print(f"Runs: {len(recent_metrics)}")
        print(f"Execution time - avg: {sum(execution_times)/len(execution_times):.2f}s, "
              f"min: {min(execution_times):.2f}s, max: {max(execution_times):.2f}s")
        print(f"Memory usage - avg: {sum(memory_deltas)/len(memory_deltas):.1f}MB, "
              f"min: {min(memory_deltas):.1f}MB, max: {max(memory_deltas):.1f}MB")
        
        # Check for performance degradation
        if len(execution_times) >= 10:
            recent_avg = sum(execution_times[-5:]) / 5
            older_avg = sum(execution_times[-10:-5]) / 5
            
            if recent_avg > older_avg * 1.2:
                print("⚠️  Performance degradation detected (20% slower)")
            elif recent_avg < older_avg * 0.8:
                print("📈 Performance improvement detected (20% faster)")

def run_performance_monitoring():
    """Run comprehensive performance monitoring"""
    monitor = PerformanceMonitor()
    
    # Scripts to monitor
    scripts_to_test = [
        ('grid_generation', 'scripts/generate_grids_geojson.py'),
        ('icon_manifest', 'scripts/generate_icons_manifest.py'),
        ('poi_processing', 'scripts/static_poi_to_geojson.py'),
    ]
    
    # Run monitoring
    for script_name, script_path in scripts_to_test:
        if os.path.exists(script_path):
            monitor.run_script_with_monitoring(script_name, script_path)
        else:
            print(f"⚠️  Script not found: {script_path}")
    
    # Save metrics
    monitor.save_metrics()
    
    # Analyze trends
    for script_name, _ in scripts_to_test:
        monitor.analyze_performance_trends(script_name)

if __name__ == "__main__":
    run_performance_monitoring()
```

## Conclusion

This comprehensive guide provides the essential knowledge and tools needed to successfully work with the BitCraft Map scripts ecosystem. From basic setup to advanced troubleshooting, these examples and solutions cover the most common scenarios encountered during development and operation.

Key takeaways:
- **Start Simple**: Begin with basic scripts that don't require external dependencies
- **Validate Early**: Implement validation and error checking from the beginning
- **Monitor Performance**: Track script performance to identify issues before they become critical
- **Plan for Scale**: Design workflows that can handle growing datasets and changing requirements
- **Document Everything**: Maintain clear documentation and examples for future developers

The scripts ecosystem is designed to be modular and extensible. As the BitCraft game evolves and new data sources become available, these patterns and practices will help ensure the map system continues to provide accurate and timely information to players and developers alike.

For additional support and community contributions, refer to the individual script documentation and the project's main README file.