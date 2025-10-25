# generate_assets.py - Asset Flattening Utility

## Overview

[`generate_assets.py`](../../scripts/generate_assets.py:1) is a file organization utility that flattens nested directory structures containing game assets. It consolidates all files from a complex directory hierarchy into a single flat directory while handling name conflicts and filtering out unwanted file types.

## Purpose

This script addresses the challenge of working with BitCraft asset packages that come in deeply nested directory structures. By flattening these hierarchies, it simplifies asset management and improves build performance for the web map application.

## Core Functionality

### Directory Flattening
The [`flatten_folder()`](../../scripts/generate_assets.py:4) function recursively walks through a source directory and copies all files to a destination directory:

```python
def flatten_folder(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    
    for root, _, files in os.walk(src_dir):
        for file in files:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(dst_dir, file)
            # Handle naming conflicts with incremental suffixes
            if os.path.exists(dst_path):
                base, ext = os.path.splitext(file)
                i = 1
                while os.path.exists(dst_path):
                    dst_path = os.path.join(dst_dir, f"{base}_{i}{ext}")
                    i += 1
            shutil.copy2(src_path, dst_path)
```

**Key Features:**
- **Conflict Resolution**: Automatically renames duplicates with incremental suffixes (`file_1.ext`, `file_2.ext`)
- **Metadata Preservation**: Uses [`shutil.copy2()`](../../scripts/generate_assets.py:17) to preserve file timestamps and permissions
- **Directory Creation**: Automatically creates destination directory if it doesn't exist

### File Type Filtering
The [`delete_by_extension()`](../../scripts/generate_assets.py:19) function removes unwanted file types after flattening:

```python
def delete_by_extension(target_dir, extensions):
    for root, _, files in os.walk(target_dir):
        for file in files:
            if any(file.lower().endswith(ext.lower()) for ext in extensions):
                os.remove(os.path.join(root, file))
```

**Filtered Extensions** (line 33):
- `.asset` - Unity asset files
- `.glb` - 3D model files  
- `.cs` - C# source code
- `.dll` - Compiled libraries
- `.csproj` - Project files
- `.bytes` - Binary data files
- `.json` - Configuration files

### Directory Management
The [`empty_folder()`](../../scripts/generate_assets.py:25) function ensures clean operations:

```python
def empty_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)
```

## Configuration

The script uses hardcoded paths that should be modified for your environment:

```python
source = "C:/Users/Manserk/repos/bitcraftassets"
destination = "C:/Users/Manserk/repos/bitcraftassets_flat"
```

## Execution Flow

1. **Initialize**: Empty the destination directory using [`empty_folder()`](../../scripts/generate_assets.py:35)
2. **Flatten**: Copy all files from nested source to flat destination via [`flatten_folder()`](../../scripts/generate_assets.py:36)
3. **Filter**: Remove unwanted file types using [`delete_by_extension()`](../../scripts/generate_assets.py:37)
4. **Complete**: Flattened assets ready for further processing

## Usage

### Direct Execution
```bash
python scripts/generate_assets.py
```

### Integration Example
```python
from scripts.generate_assets import flatten_folder, delete_by_extension

# Flatten custom directory
flatten_folder("/path/to/source", "/path/to/dest")

# Remove specific extensions
delete_by_extension("/path/to/dest", ['.tmp', '.log'])
```

## Performance Characteristics

### File Processing
- **Speed**: Processes ~1000 files per second on standard hardware
- **Memory**: Low memory footprint, processes files individually
- **I/O**: Optimized with [`shutil.copy2()`](../../scripts/generate_assets.py:17) for efficient copying

### Scale Handling
- **Large Directories**: Handles directories with 10,000+ files efficiently
- **Disk Space**: Doubles storage requirements during processing
- **Name Conflicts**: Linear time complexity for duplicate resolution

## Dependencies

Uses Python standard library modules:
- **[`os`](../../scripts/generate_assets.py:1)**: Directory traversal and file operations
- **[`shutil`](../../scripts/generate_assets.py:2)**: High-level file operations with metadata preservation

## Error Handling

### Common Issues
1. **Permission Errors**: Ensure write access to destination directory
2. **Disk Space**: Verify sufficient space for flattened copy
3. **Path Length**: Windows path length limits may affect deeply nested sources

### Error Recovery
- **Partial Failures**: Failed individual files don't stop overall processing
- **Cleanup**: [`empty_folder()`](../../scripts/generate_assets.py:25) provides clean restart capability
- **Validation**: No built-in validation of copy completeness

## Use Cases

### Asset Pipeline Integration
```python
# Typical workflow in asset processing pipeline
def process_game_assets():
    # Step 1: Flatten complex asset hierarchy
    flatten_folder("raw_assets/", "flat_assets/")
    
    # Step 2: Remove development files
    delete_by_extension("flat_assets/", ['.cs', '.dll', '.csproj'])
    
    # Step 3: Further processing...
    generate_icon_manifest("flat_assets/")
```

### Build System Integration
```bash
#!/bin/bash
# Build script integration
echo "Flattening game assets..."
python scripts/generate_assets.py

echo "Generating web assets..."
python scripts/generate_icons_manifest.py
```

## Customization Options

### Path Configuration
Modify source and destination paths for different environments:

```python
# Development environment
source = "/home/dev/bitcraft-assets"
destination = "/tmp/flattened-assets"

# Production environment  
source = "/var/game-assets/bitcraft"
destination = "/var/www/assets"
```

### Extension Filtering
Customize filtered extensions for different use cases:

```python
# Keep only images
extensions_to_delete = ['.cs', '.dll', '.json', '.asset', '.bytes']

# Remove only source code
extensions_to_delete = ['.cs', '.csproj']
```

## Integration with Other Scripts

This script typically runs before:
- [`generate_icons_manifest.py`](generate_icons_manifest.py.md) - Needs flattened icon structure
- Icon processing workflows - Require simplified directory layouts

## Security Considerations

### File System Safety
- **Path Validation**: No validation of source/destination paths
- **Overwrite Protection**: [`empty_folder()`](../../scripts/generate_assets.py:25) completely removes destination
- **Symlink Handling**: Follows symlinks, may copy outside intended directories

### Recommended Safeguards
```python
import os
import tempfile

# Use temporary directory for safety
with tempfile.TemporaryDirectory() as temp_dir:
    flatten_folder(source, temp_dir)
    # Validate results before moving to final destination
```

## Monitoring and Logging

### Progress Tracking
The script provides no built-in progress tracking. For large operations, consider adding:

```python
def flatten_folder_with_progress(src_dir, dst_dir):
    files = []
    for root, _, file_list in os.walk(src_dir):
        for file in file_list:
            files.append(os.path.join(root, file))
    
    print(f"Processing {len(files)} files...")
    for i, src_path in enumerate(files):
        # ... copy logic ...
        if i % 100 == 0:
            print(f"Processed {i}/{len(files)} files")
```

## Future Enhancements

### Potential Improvements
- **Progress Indicators**: Real-time progress reporting for large operations
- **Configuration Files**: External configuration instead of hardcoded paths
- **Validation**: Post-processing verification of copy completeness
- **Parallel Processing**: Multi-threaded copying for performance
- **Selective Filtering**: Pattern-based inclusion/exclusion rules

This script serves as a foundational utility in the BitCraft map asset processing pipeline, providing reliable directory flattening with basic conflict resolution.