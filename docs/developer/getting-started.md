
# Developer Getting Started Guide

This guide will help you set up a local development environment for the BitCraft Map project and understand the development workflow.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Project Structure](#project-structure)
4. [Local Development Setup](#local-development-setup)
5. [Development Workflow](#development-workflow)
6. [Data Generation](#data-generation)
7. [Testing](#testing)
8. [Common Development Tasks](#common-development-tasks)
9. [Troubleshooting](#troubleshooting)
10. [Next Steps](#next-steps)

## Prerequisites

### Required Software

- **Git** - For version control
- **Node.js** (v16+) - For package management and build tools
- **Python** (3.8+) - For data generation scripts
- **Docker** (optional) - For backend services
- **Modern Web Browser** - Chrome, Firefox, or Edge with developer tools

### Recommended Tools

- **Visual Studio Code** - With extensions:
  - Live Server
  - JavaScript ES6 code snippets
  - Python
  - Docker (if using)
- **Postman** or **Insomnia** - For API testing
- **Git Bash** (Windows) or Terminal (macOS/Linux)

### Knowledge Prerequisites

- Basic HTML, CSS, JavaScript
- Familiarity with [Leaflet.js](https://leafletjs.com/)
- Basic understanding of GeoJSON format
- Python basics (for data scripts)
- Docker basics (optional, for backend)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/bitcraftmap/bitcraftmap.git
cd bitcraftmap
```

### 2. Verify Project Structure

You should see the following key directories:

```
bitcraftmap/
├── assets/          # Frontend assets (CSS, JS, images)
├── backend/         # Backend services configuration
├── docs/            # Documentation (you're reading this!)
├── scripts/         # Data generation Python scripts
├── src/             # Source files
├── index.html       # Main application entry point
└── README.md        # Project overview
```

### 3. Set Up Python Environment (for data scripts)

```bash
# Navigate to scripts directory
cd scripts

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Start Local Development Server

The easiest way to run the application locally:

#### Option A: Using Python's Built-in Server
```bash
# From project root
python -m http.server 8000
```
Then open http://localhost:8000

#### Option B: Using Node.js http-server
```bash
# Install globally
npm install -g http-server

# From project root
http-server -p 8000
```

#### Option C: Using VS Code Live Server
1. Install the "Live Server" extension
2. Right-click on `index.html`
3. Select "Open with Live Server"

### 5. Verify Setup

Open your browser and navigate to your local server. You should see:
- ✅ BitCraft Map loads with base map image
- ✅ Map controls (zoom, layers) are functional
- ✅ No console errors in browser developer tools
- ✅ Coordinate display updates when moving mouse

## Project Structure

### Frontend Architecture

```
assets/
├── css/
│   └── map.css           # Main stylesheet
├── js/
│   ├── config.js         # Map configuration and options
│   ├── library.js        # Layer registry and utilities
│   ├── map.js           # Main application logic
│   ├── ui.js            # UI components (minimal)
│   └── utils.js         # Utility functions
├── images/              # Icons and images
│   ├── manifest.js      # Icon registry
│   └── [various icons]
├── leaflet/             # Leaflet library files
├── maps/                # Map tile images
├── markers/             # GeoJSON data files
└── search/              # Search plugin files
```

### Key Files Explained

| File | Purpose | Key Features |
|------|---------|--------------|
| [`index.html`](../../index.html:1) | Application entry point | CSP headers, asset loading |
| [`assets/js/config.js`](../../assets/js/config.js:1) | Configuration | Custom CRS, app options, styling |
| [`assets/js/map.js`](../../assets/js/map.js:1) | Main logic | Map initialization, data loading, event handling |
| [`assets/js/library.js`](../../assets/js/library.js:1) | Layer management | Registry pattern for layer control |
| [`assets/css/map.css`](../../assets/css/map.css:1) | Styling | Map-specific styles and responsive design |

### Backend Architecture

```
backend/
├── Caddyfile          # Caddy web server configuration
├── Krakend.json       # API gateway configuration
├── Dockerfile         # Container definition
└── [deployment scripts]
```

### Data Pipeline

```
scripts/
├── generate_assets.py          # Asset generation
├── generate_claims_geojson.py  # Claims data processing
├── generate_grids_geojson.py   # Grid overlay generation
├── generate_terrain_map.py     # Terrain processing
└── requirements.txt            # Python dependencies
```

## Local Development Setup

### Frontend Development

1. **File Watching** (optional but recommended):
   ```bash
   # Install nodemon for auto-refresh
   npm install -g nodemon
   
   # Watch for changes and restart server
   nodemon --watch assets --exec "python -m http.server 8000"
   ```

2. **Browser Developer Tools Setup**:
   - Open F12 Developer Tools
   - Go to Console tab to monitor JavaScript errors
   - Use Network tab to debug asset loading
   - Use Application tab to inspect local storage

3. **Content Security Policy (CSP)**:
   The project has strict CSP headers defined in [`index.html`](../../index.html:10). During development, you may need to temporarily relax these for debugging.

### Backend Development (Optional)

If you need to work with the backend services:

```bash
cd backend

# Build Docker image
docker build -t bitcraftmap-backend .

# Run with Docker Compose (if you create docker-compose.yml)
docker-compose up -d

# Or run individual services
docker run -p 9000:9000 bitcraftmap-backend
```

### Environment Variables

Create a `.env` file in the project root for local development:

```bash
# API Configuration
API_BASE_URL=https://api.bitcraftmap.com
GITHUB_API_URL=https://api.github.com

# Development settings
DEBUG_MODE=true
LOCAL_ASSETS=true
```

## Development Workflow

### Making Changes to the Map

1. **CSS Changes** ([`assets/css/map.css`](../../assets/css/map.css:1)):
   - Changes are reflected immediately with live reload
   - Test responsive behavior with browser dev tools
   - Verify contrast and accessibility

2. **JavaScript Changes**:
   - Edit files in [`assets/js/`](../../assets/js/)
   - Refresh browser to see changes
   - Check browser console for errors
   - Test with various URL parameters

3. **Configuration Changes** ([`assets/js/config.js`](../../assets/js/config.js:1)):
   - Modify map bounds, zoom levels, or styling
   - Test coordinate system changes carefully
   - Verify icon manifests and tier colors

### Adding New Features

1. **New Layer Types**:
   ```javascript
   // In map.js, add new layer group
   const newFeatureLayer = L.layerGroup()
   
   // Add to layer controls
   const genericToggle = {
     // ... existing layers
     "New Feature": newFeatureLayer
   }
   ```

2. **New GeoJSON Properties**:
   ```javascript
   // In paintGeoJson function, add new property handling
   if (feature.properties?.customProperty) {
     // Handle custom property
   }
   ```

3. **New Icon Types**:
   - Add icon file to [`assets/images/`](../../assets/images/)
   - Update [`manifest.js`](../../assets/images/manifest.js:1) (or regenerate)
   - Reference in GeoJSON or code

### Testing Changes

1. **Manual Testing Checklist**:
   - [ ] Map loads without errors
   - [ ] All layer controls work
   - [ ] Search functionality works
   - [ ] URL parameters are processed correctly
   - [ ] Custom waypoint loading works (hash and gist)
   - [ ] Mobile responsiveness
   - [ ] Cross-browser compatibility

2. **Test URLs**:
   ```
   # Base functionality
   http://localhost:8000/
   
   # With heatmap
   http://localhost:8000/?heatmap=1
   
   # With resource data
   http://localhost:8000/?regionId=2&resourceId=123
   
   # With custom GeoJSON
   http://localhost:8000/#%7B%22type%22%3A%22FeatureCollection%22...
   ```

## Data Generation

The [`scripts/`](../../scripts/) directory contains Python scripts for generating map data from game files.

### Setting Up Data Generation

1. **Install Dependencies**:
   ```bash
   cd scripts
   pip install -r requirements.txt
   ```

2. **Common Scripts**:
   
   **Generate Icons Manifest**:
   ```bash
   python generate_icons_manifest.py
   ```
   
   **Generate GeoJSON from Game Data**:
   ```bash
   python generate_claims_geojson.py
   python generate_grids_geojson.py
   ```
   
   **Generate Terrain Map**:
   ```bash
   python generate_terrain_map.py
   ```

### Understanding Data Flow

```
Game Files → Python Scripts → GeoJSON/Assets → Frontend Display
```

1. **Source Data**: Game files (coordinates, names, properties)
2. **Processing**: Python scripts transform and validate data
3. **Output**: GeoJSON files in [`assets/markers/`](../../assets/markers/)
4. **Consumption**: Frontend loads and renders GeoJSON

### Adding New Data Sources

1. Create new Python script in [`scripts/`](../../scripts/)
2. Follow existing patterns for data validation
3. Output to appropriate directory
4. Update frontend to load new data

Example script structure:
```python
import json
from pathlib import Path

def process_game_data(input_file):
    """Process game data and return GeoJSON"""
    # Data processing logic
    pass

def main():
    data = process_game_data('input.dat')
    output_path = Path('../assets/markers/new_data.geojson')
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    main()
```

## Testing

### Automated Testing (Recommended Setup)

While the project doesn't currently have automated tests, here's how to set them up:

1. **Install Testing Framework**:
   ```bash
   npm init -y
   npm install --save-dev jest puppeteer
   ```

2. **Basic Test Structure**:
   ```javascript
   // tests/basic.test.js
   describe('BitCraft Map', () => {
     test('loads without errors', async () => {
       // Test implementation
     });
   });
   ```

### Manual Testing Procedures

1. **Coordinate System Testing**:
   - Click various locations on map
   - Verify N/E coordinates display correctly
   - Test coordinate conversion functions

2. **GeoJSON Validation Testing**:
   - Test with valid GeoJSON
   - Test with malformed JSON
   - Test with security attack vectors
   - Verify HTML escaping in popups

3. **Layer Management Testing**:
   - Toggle all layer controls
   - Test layer combinations
   - Verify performance with many markers

4. **URL Parameter Testing**:
   - Test all parameter combinations
   - Test invalid parameter values
   - Test edge cases and boundary conditions

## Common Development Tasks

### Adding a New Map Layer

1. **Create Layer Group**:
   ```javascript
   // In map.js
   const myNewLayer = L.layerGroup()
   ```

2. **Add to Controls**:
   ```javascript
   const genericToggle = {
     // ... existing
     "My New Layer": myNewLayer
   }
   ```

3. **Load Data**:
   ```javascript
   async function loadMyNewData() {
     const file = await fetch('assets/markers/mynew.geojson')
     const geojsonData = await file.json()
     // Process and add to layer
   }
   ```

### Modifying the Coordinate System

**⚠️ Warning**: Coordinate system changes affect the entire map. Test thoroughly.

1. **Understand Current System** ([`config.js`](../../assets/js/config.js:32)):
   - Custom CRS extends `L.CRS.Simple`
   - Uses hexagonal grid with apothem calculations
   - Maps game coordinates (0-23040) to display

2. **Making Changes**:
   - Modify projection functions in `createMapOptions()`
   - Update bounds and transformations
   - Test coordinate display functions

3. **Testing Coordinate Changes**:
   - Verify existing markers appear in correct locations
   - Test coordinate display accuracy
   - Check zoom and pan behavior

### Adding Custom Icon Support

1. **Add Icon File**:
   - Place in appropriate [`assets/images/`](../../assets/images/) subdirectory
   - Use consistent naming convention

2. **Update Manifest**:
   - Add to [`manifest.js`](../../assets/images/manifest.js:1) or regenerate
   - Test icon loading

3. **Use in Code**:
   ```javascript
   const customIcon = createIcon('myNewIcon', [32, 32])
   L.marker([lat, lng], { icon: customIcon })
   ```

### Debugging Performance Issues

1. **Check Browser Developer Tools**:
   - Performance tab for rendering bottlenecks
   - Memory tab for memory leaks
   - Network tab for slow asset loading

2. **Common Performance Issues**:
   - Too many markers rendered simultaneously
   - Large GeoJSON files loaded at once
   - Inefficient layer management

3. **Optimization Strategies**:
   - Use canvas rendering for high-density markers
   - Implement lazy loading for large datasets
   - Use layer clustering for dense marker groups
   - Optimize GeoJSON file sizes
   - Cache frequently accessed data

### Working with the Custom CRS (Coordinate Reference System)

The BitCraft Map uses a custom coordinate system that maps BitCraft's hexagonal grid to Leaflet's display system.

1. **Key Components**:
   ```javascript
   // From config.js
   const apothem = 2 / Math.sqrt(3)  // Hexagon geometry
   const mapWidth = 23040            // Game world bounds
   const mapHeight = 23040           // Game world bounds
   ```

2. **Coordinate Transformations**:
   ```javascript
   // Game → Display coordinates
   function readableCoordinates(latlng) {
     return [Math.round(latlng.lat / 3), Math.round(latlng.lng / 3)]
   }
   
   // WebSocket coordinates → Map coordinates
   const mapLat = gameZ / 1000
   const mapLng = gameX / 1000
   ```

3. **Testing Coordinate Changes**:
   - Use known landmark locations to verify accuracy
   - Test edge cases (corners, center, boundaries)
   - Verify with F4 debug coordinates from game

## Troubleshooting

### Common Issues and Solutions

#### Map Doesn't Load
**Symptoms**: Blank screen, no map visible
**Possible Causes**:
- CORS issues with local development server
- Missing or corrupted map image files
- JavaScript errors blocking execution

**Solutions**:
```bash
# Check browser console for errors
# Use proper local server (not file:// protocol)
python -m http.server 8000

# Verify all assets are accessible
curl http://localhost:8000/assets/maps/map.png
```

#### Markers Don't Appear
**Symptoms**: Map loads but no markers show
**Possible Causes**:
- GeoJSON file loading failures
- Coordinate system mismatches
- Layer visibility settings

**Solutions**:
```javascript
// Debug GeoJSON loading in browser console
fetch('assets/markers/claims.geojson')
  .then(r => r.json())
  .then(data => console.log('GeoJSON loaded:', data))
  .catch(e => console.error('Failed to load:', e))

// Check layer visibility
console.log(map.hasLayer(claimT1Layer))
```

#### Coordinate Display Issues
**Symptoms**: Wrong coordinates shown, misaligned markers
**Possible Causes**:
- CRS configuration errors
- Coordinate conversion bugs
- Map bounds misconfiguration

**Solutions**:
1. Verify CRS settings in [`config.js`](../../assets/js/config.js:32)
2. Test coordinate conversion functions manually
3. Compare with known game coordinates

#### Performance Problems
**Symptoms**: Slow loading, laggy interactions
**Possible Causes**:
- Too many markers rendered at once
- Large GeoJSON files
- Memory leaks from event listeners

**Solutions**:
```javascript
// Monitor performance
console.time('layer-load')
loadClaimsGeoJson()
console.timeEnd('layer-load')

// Check memory usage in DevTools
// Implement marker clustering or pagination
```

#### CSP (Content Security Policy) Errors
**Symptoms**: Assets blocked, inline scripts failing
**Cause**: Strict CSP headers in [`index.html`](../../index.html:10)

**Solutions**:
```html
<!-- For development, temporarily relax CSP -->
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self' 'unsafe-inline';
  /* other directives */
">
```

### Debug Mode Setup

Add debug utilities to your development environment:

```javascript
// Add to browser console for debugging
window.debug = {
  layers: layerRegistry,
  map: map,
  showAllLayers: () => {
    Object.values(allLayers).forEach(layer => map.addLayer(layer))
  },
  hideAllLayers: () => {
    Object.values(allLayers).forEach(layer => map.removeLayer(layer))
  },
  logCoordinates: (latlng) => {
    console.log('Map coords:', latlng)
    console.log('Display coords:', readableCoordinates(latlng))
  }
}
```

### Getting Help

1. **Check Browser Console**: First line of defense for JavaScript errors
2. **Network Tab**: Debug asset loading and API calls
3. **Application Tab**: Inspect local storage and service workers
4. **GitHub Issues**: Search existing issues for similar problems
5. **Community**: Join BitCraft community forums for game-specific questions

### Development Environment Issues

#### Windows-Specific Issues
- Use Git Bash for consistent command-line experience
- Watch out for path separator differences (\ vs /)
- Some Python packages may require Visual C++ Build Tools

#### CORS Issues
- Always use a proper HTTP server for development
- File:// protocol will cause CORS issues
- Consider using browser flags for testing (not recommended for production)

#### Port Conflicts
```bash
# Check if port is in use
netstat -an | grep :8000

# Use different port
python -m http.server 8080
```

## Next Steps

### For New Developers

After completing this setup guide, continue with these resources:

1. **Read the Architecture Overview** - [`docs/developer/architecture-overview.md`] (when created)
   - Understand the complete system design
   - Learn about data flow and component relationships
   - Study design patterns used in the codebase

2. **Study the API Reference** - [`docs/api/api-reference.md`](../api/api-reference.md)
   - Learn all available APIs and their parameters
   - Understand GeoJSON custom properties
   - Practice with integration examples

3. **Explore the Codebase** - Start with these key files:
   - [`assets/js/map.js`](../../assets/js/map.js:1) - Core application logic
   - [`assets/js/config.js`](../../assets/js/config.js:1) - Configuration and CRS
   - [`assets/js/library.js`](../../assets/js/library.js:1) - Layer management system

### Suggested First Projects

Choose one of these projects to get familiar with the codebase:

#### Beginner Projects
1. **Add a new icon type**
   - Create new icon file
   - Update manifest
   - Test in GeoJSON waypoint

2. **Implement a simple feature toggle**
   - Add URL parameter support
   - Toggle UI element visibility
   - Update documentation

3. **Create a new map layer**
   - Add layer group
   - Load static GeoJSON data
   - Add to layer controls

#### Intermediate Projects
1. **Improve coordinate display**
   - Add different coordinate format options
   - Implement coordinate conversion tools
   - Add copy-to-clipboard functionality

2. **Enhance GeoJSON validation**
   - Add more custom property validation
   - Improve error messages
   - Add validation for new feature types

3. **Implement marker clustering**
   - Add clustering for dense marker areas
   - Optimize performance for large datasets
   - Maintain search functionality

#### Advanced Projects
1. **Add real-time features**
   - Implement WebSocket for live data
   - Add player tracking capabilities
   - Create real-time marker updates

2. **Implement advanced pathfinding** (from [`NOTES.md`](../../NOTES.md:21))
   - Add terrain elevation data support
   - Calculate walkable zones
   - Implement navigation algorithms

3. **Create mobile app features**
   - Implement offline map support
   - Add GPS integration
   - Create mobile-optimized UI

### Contributing Guidelines

1. **Code Style**:
   - Follow existing JavaScript patterns
   - Use meaningful variable names
   - Add comments for complex logic
   - Test changes thoroughly

2. **Commit Guidelines**:
   - Write descriptive commit messages
   - Keep commits focused and atomic
   - Reference issues when applicable

3. **Pull Request Process**:
   - Fork the repository
   - Create feature branch
   - Add tests if applicable
   - Update documentation
   - Submit PR with clear description

### Advanced Topics to Explore

1. **Custom Map Projections**
   - Study Leaflet CRS system in depth
   - Learn about coordinate transformations
   - Understand hexagonal grid mathematics

2. **Performance Optimization**
   - Canvas vs DOM rendering strategies
   - Memory management techniques
   - Network optimization patterns

3. **Data Pipeline Architecture**
   - Game data extraction methods
   - Data validation and sanitization
   - Automated data processing workflows

4. **Backend Integration**
   - API gateway patterns (Krakend)
   - Microservices architecture
   - Caching strategies

### Resources and References

#### Leaflet.js Resources
- [Leaflet Documentation](https://leafletjs.com/reference.html)
- [Leaflet Tutorials](https://leafletjs.com/examples.html)
- [Custom CRS Examples](https://leafletjs.com/examples/crs-simple/crs-simple.html)

#### GeoJSON Resources
- [GeoJSON Specification](https://datatracker.ietf.org/doc/html/rfc7946)
- [GeoJSON Validation](https://geojsonlint.com/)
- [GeoJSON Examples](https://geojson.org/)

#### BitCraft Game Resources
- BitCraft Official Website
- BitCraft Community Discord
- Game Documentation and APIs

#### Development Tools
- [Chrome DevTools Guide](https://developers.google.com/web/tools/chrome-devtools)
- [VS Code Extensions for Web Development](https://code.visualstudio.com/docs/nodejs/working-with-javascript)
- [Git Best Practices](https://github.com/git-tips/tips)

---

## Getting Support

- **Bug Reports**: Open GitHub issues with detailed reproduction steps
- **Feature Requests**: Discuss in GitHub discussions or community forums
- **Development Questions**: Use project discussions or community channels
- **Security Issues**: Report privately to maintainers

Welcome to the BitCraft Map development community! Start with small changes, ask questions, and gradually work your way up to more complex features. The codebase is well-structured and extensible, making it a great project for learning modern web mapping techniques.