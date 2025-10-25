# generate_icons_manifest.py - Icon Manifest Creation

## Overview

[`generate_icons_manifest.py`](../../scripts/generate_icons_manifest.py:1) is a lightweight asset discovery utility that scans the project's icon directories and generates a JavaScript manifest file. This script enables efficient web application asset loading by providing a comprehensive catalog of available icons without requiring runtime directory traversal.

## Purpose

This script addresses web application asset management challenges by:
- Automatically discovering all icon assets in the project
- Generating a JavaScript manifest for efficient asset loading
- Eliminating the need for runtime directory scanning
- Providing a single source of truth for available icons
- Supporting multiple image formats in a unified interface

## Core Functionality

### Directory Scanning Configuration
The script uses configurable paths for flexible deployment:

```python
url_prefix = 'assets/images/'
icons_directory = Path(url_prefix)
manifest_file = 'assets/images/manifest.js'
```

**Configuration Parameters:**
- **[`url_prefix`](../../scripts/generate_icons_manifest.py:4)**: Base URL path for icon assets
- **[`icons_directory`](../../scripts/generate_icons_manifest.py:5)**: Source directory for icon scanning
- **[`manifest_file`](../../scripts/generate_icons_manifest.py:6)**: Output JavaScript file location

### Supported Image Formats
The script recognizes multiple image formats commonly used in web applications:

```python
extensions = {'.png', '.svg', '.jpg', '.jpeg', '.webp'}
```

**Supported Formats:**
- **PNG**: Raster images with transparency support
- **SVG**: Scalable vector graphics for crisp scaling
- **JPG/JPEG**: Compressed raster images for photographs
- **WebP**: Modern format with superior compression

### Recursive Asset Discovery
The core scanning algorithm uses Python's `pathlib` for robust file system traversal:

```python
for file in sorted(icons_directory.rglob("*")):
    if file.suffix.lower() in extensions and file.is_file():
        manifest[file.stem] = url_prefix + file.relative_to(icons_directory).as_posix()
```

**Discovery Process:**
1. **[Recursive Scan](../../scripts/generate_icons_manifest.py:11)**: `rglob("*")` traverses all subdirectories
2. **[Extension Filter](../../scripts/generate_icons_manifest.py:12)**: Only processes supported image formats
3. **[File Validation](../../scripts/generate_icons_manifest.py:12)**: Ensures discovered items are files, not directories
4. **[Path Mapping](../../scripts/generate_icons_manifest.py:13)**: Maps file stems to complete URL paths
5. **[Sorted Output](../../scripts/generate_icons_manifest.py:11)**: Deterministic ordering for consistent results

### JavaScript Manifest Generation
The script creates a JavaScript constant that can be directly imported:

```python
js_content = 'const iconsManifest = ' + json.dumps(manifest, indent=2) + ';'
```

**Output Structure:**
```javascript
const iconsManifest = {
  "claim": "assets/images/claim/claim.png",
  "claimT0": "assets/images/claim/claimT0.png", 
  "t1": "assets/images/ore/t1.png",
  "t2": "assets/images/ore/t2.png",
  "iconMining": "assets/images/wiki/iconMining.svg",
  "temple": "assets/images/other/temple.svg"
};
```

## File System Integration

### Directory Structure Support
The script handles nested directory structures automatically:

```
assets/images/
├── claim/
│   ├── claim.png
│   ├── claimT0.png
│   └── claimT1.png
├── ore/
│   ├── t1.png
│   ├── t2.png
│   └── t3.png
├── wiki/
│   ├── iconMining.svg
│   └── iconForestry.svg
└── manifest.js (generated)
```

### Path Normalization
The script uses `as_posix()` to ensure cross-platform URL compatibility:

```python
file.relative_to(icons_directory).as_posix()
```

**Benefits:**
- **Cross-Platform**: Works consistently on Windows, macOS, and Linux
- **Web Compatible**: Forward slashes in all URLs regardless of OS
- **Relative Paths**: Maintains directory structure in manifest

## Usage Examples

### Direct Execution
```bash
python scripts/generate_icons_manifest.py
```

### Integration with Build Process
```bash
#!/bin/bash
# Asset processing pipeline
echo "Flattening assets..."
python scripts/generate_assets.py

echo "Generating icon manifest..."  
python scripts/generate_icons_manifest.py

echo "Building web application..."
npm run build
```

### Web Application Integration
```javascript
// Import the generated manifest
import { iconsManifest } from './assets/images/manifest.js';

// Use icons by name
function getIconUrl(iconName) {
  return iconsManifest[iconName] || 'assets/images/default.png';
}

// Example usage in map markers
L.marker([x, y], {
  icon: L.icon({
    iconUrl: getIconUrl('claim'),
    iconSize: [32, 32]
  })
});
```

## Performance Characteristics

### Scanning Performance
- **File System I/O**: Single directory traversal pass
- **Memory Usage**: Minimal - only stores file paths in memory
- **Execution Time**: <100ms for typical icon directories (100-1000 files)
- **Scalability**: Linear O(n) complexity with file count

### Output Optimization
- **JSON Formatting**: 2-space indentation for readability
- **Deterministic Output**: Sorted keys for consistent file generation
- **File Size**: Typically 1-10KB for standard icon collections

## Dependencies

### Required Modules
- **[`pathlib.Path`](../../scripts/generate_icons_manifest.py:1)**: Modern file system path handling
- **[`json`](../../scripts/generate_icons_manifest.py:2)**: JSON serialization for manifest data

### No External Dependencies
Uses only Python standard library, ensuring maximum compatibility and minimal setup requirements.

## Error Handling and Edge Cases

### File System Robustness
```python
# Handles common edge cases automatically
if file.suffix.lower() in extensions and file.is_file():
    # Processes only valid image files
    # Skips directories, symlinks, and other file types
```

**Robust Handling:**
- **Case Insensitive**: `file.suffix.lower()` handles mixed case extensions
- **File Type Validation**: `is_file()` prevents directory inclusion
- **Missing Directories**: `Path()` gracefully handles non-existent paths

### Common Issues and Solutions

1. **Permission Errors**
   ```python
   # Add error handling for restricted directories
   try:
       for file in sorted(icons_directory.rglob("*")):
           # ... processing logic
   except PermissionError:
       print(f"Permission denied accessing {icons_directory}")
   ```

2. **Large Directory Performance**
   ```python
   # Progress reporting for large directories
   files = list(icons_directory.rglob("*"))
   for i, file in enumerate(sorted(files)):
       if i % 100 == 0:
           print(f"Processed {i}/{len(files)} files")
   ```

3. **Duplicate File Names**
   ```python
   # Handle duplicate stems in different directories
   if file.stem in manifest:
       print(f"Warning: Duplicate icon name '{file.stem}' - using {file}")
   ```

## Customization Options

### Format Extension Configuration
```python
# Custom format support
extensions = {'.png', '.svg', '.gif', '.bmp', '.tiff'}

# Web-optimized formats only
extensions = {'.png', '.svg', '.webp'}

# Development formats (including unoptimized)
extensions = {'.png', '.svg', '.jpg', '.jpeg', '.webp', '.gif', '.bmp'}
```

### Output Format Customization
```python
# TypeScript interface generation
ts_content = f"""
export interface IconsManifest {{
  [key: string]: string;
}}

export const iconsManifest: IconsManifest = {json.dumps(manifest, indent=2)};
"""

# ES6 module export
es6_content = f"export const iconsManifest = {json.dumps(manifest, indent=2)};"
```

### Path Configuration
```python
# Multi-directory scanning
icon_directories = [
    'assets/images/icons/',
    'assets/images/markers/', 
    'assets/images/ui/'
]

combined_manifest = {}
for directory in icon_directories:
    # Scan each directory and merge results
```

## Integration Patterns

### Build System Integration
```json
{
  "scripts": {
    "prebuild": "python scripts/generate_icons_manifest.py",
    "build": "webpack --mode production",
    "dev": "python scripts/generate_icons_manifest.py && webpack serve"
  }
}
```

### Asset Pipeline Integration
```python
def update_asset_manifest():
    """Update manifest as part of larger asset processing"""
    # Generate icons manifest
    subprocess.run(['python', 'scripts/generate_icons_manifest.py'])
    
    # Validate manifest completeness
    validate_icon_manifest()
    
    # Update web application cache
    invalidate_icon_cache()
```

### Development Workflow
```python
# Watch mode for development
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class IconUpdateHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(('.png', '.svg', '.jpg')):
            print("Icon changed, regenerating manifest...")
            generate_manifest()

# Usage in development server
observer = Observer()
observer.schedule(IconUpdateHandler(), 'assets/images/', recursive=True)
observer.start()
```

## Quality Assurance

### Manifest Validation
```python
def validate_manifest():
    """Ensure all referenced icons exist and are accessible"""
    with open('assets/images/manifest.js', 'r') as f:
        content = f.read()
    
    # Extract manifest from JavaScript
    start = content.find('{')
    end = content.rfind('}') + 1
    manifest_json = content[start:end]
    manifest = json.loads(manifest_json)
    
    # Validate each icon exists
    for name, path in manifest.items():
        if not Path(path).exists():
            print(f"Warning: Icon {name} references missing file {path}")
```

### Automated Testing
```python
def test_manifest_generation():
    """Test manifest generation with known icon set"""
    # Create test directory structure
    test_dir = Path('test_icons')
    test_dir.mkdir(exist_ok=True)
    
    # Create test icons
    (test_dir / 'test.png').touch()
    (test_dir / 'icon.svg').touch()
    
    # Generate manifest
    generate_manifest_for_directory(test_dir)
    
    # Validate results
    assert Path('test_manifest.js').exists()
```

## Advanced Features

### Metadata Enhancement
```python
# Enhanced manifest with image metadata
def create_enhanced_manifest():
    manifest = {}
    for file in sorted(icons_directory.rglob("*")):
        if file.suffix.lower() in extensions and file.is_file():
            stat = file.stat()
            manifest[file.stem] = {
                'url': url_prefix + file.relative_to(icons_directory).as_posix(),
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'format': file.suffix.lower()
            }
    return manifest
```

### Optimization Integration
```python
# Integration with image optimization
def optimized_manifest():
    """Generate manifest after image optimization"""
    # Run image optimization first
    optimize_images()
    
    # Generate manifest with optimized files
    generate_icons_manifest()
    
    # Update service worker cache
    update_sw_cache()
```

## Security Considerations

### Path Safety
```python
# Prevent directory traversal attacks
def safe_relative_path(file_path, base_path):
    """Ensure file path is within base directory"""
    try:
        resolved = file_path.resolve()
        base_resolved = base_path.resolve()
        resolved.relative_to(base_resolved)
        return True
    except ValueError:
        return False
```

### File Validation
```python
# Additional security checks
def validate_image_file(file_path):
    """Verify file is actually an image"""
    try:
        from PIL import Image
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False
```

## Monitoring and Maintenance

### Health Checks
```bash
# Verify manifest freshness
MANIFEST_AGE=$(stat -c %Y assets/images/manifest.js)
ICONS_NEWEST=$(find assets/images -name '*.png' -o -name '*.svg' | xargs stat -c %Y | sort -nr | head -1)

if [ $MANIFEST_AGE -lt $ICONS_NEWEST ]; then
    echo "Warning: Icon manifest is outdated"
    python scripts/generate_icons_manifest.py
fi
```

### Automated Updates
```bash
# Cron job for regular manifest updates
0 */6 * * * cd /path/to/project && python scripts/generate_icons_manifest.py
```

## Future Enhancements

### Potential Improvements
- **Image Metadata**: Include file size, dimensions, and optimization status
- **Format Conversion**: Automatic WebP generation for modern browsers
- **Lazy Loading Support**: Generate manifests for different loading strategies
- **CDN Integration**: Support for external asset hosting
- **Cache Busting**: Include file hashes for browser cache management
- **Icon Sprites**: Automatic sprite sheet generation for performance

This utility provides essential asset discovery capabilities for the BitCraft map web application, ensuring efficient and reliable icon resource management.