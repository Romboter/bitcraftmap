# BitCraft Map API Reference

This document provides comprehensive reference for all APIs available in the BitCraft Map project, including backend endpoints, frontend JavaScript APIs, URL parameters, and custom GeoJSON properties.

## Table of Contents

1. [Backend API Endpoints](#backend-api-endpoints)
2. [Frontend JavaScript APIs](#frontend-javascript-apis)
3. [URL Parameters](#url-parameters)
4. [GeoJSON Custom Properties](#geojson-custom-properties)
5. [WebSocket API](#websocket-api)
6. [Layer Management API](#layer-management-api)
7. [Error Codes](#error-codes)
8. [Rate Limiting](#rate-limiting)

---

## Backend API Endpoints

The BitCraft Map backend provides REST endpoints for retrieving game data. All endpoints return GeoJSON format data.

### Base URL
```
https://api.bitcraftmap.com/
```

### Resource Data Endpoints

#### Get Resources by Region and Type
```http
GET /region{regionId}/resource/{resourceId}
```

**Parameters:**
- `regionId` (integer, 1-9): The region ID to query
- `resourceId` (integer): The resource type ID to retrieve

**Response Format:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "Resource Name",
        "tier": 1,
        "resource_type": "mining"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [15000, 15000]
      }
    }
  ]
}
```

**Example:**
```bash
curl https://api.bitcraftmap.com/region2/resource/123
```

### Enemy Data Endpoints

#### Get Enemies by Region and Type
```http
GET /region{regionId}/enemy/{enemyId}
```

**Parameters:**
- `regionId` (integer, 1-9): The region ID to query
- `enemyId` (integer): The enemy type ID to retrieve

**Response Format:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "Enemy Name",
        "tier": 3,
        "enemy_type": "hostile"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [12000, 8000]
      }
    }
  ]
}
```

---

## Frontend JavaScript APIs

The frontend provides several JavaScript APIs for interacting with the map and data.

### Coordinate Conversion

#### readableCoordinates(latlng)
Converts Leaflet LatLng to readable N/E coordinates.

**Parameters:**
- `latlng` (L.LatLng): Leaflet coordinate object

**Returns:**
- `Array<number>`: `[north, east]` coordinates in Small Hex format

**Example:**
```javascript
const coords = readableCoordinates(L.latLng(45000, 30000));
// Returns: [15000, 10000]
```

### Icon Management

#### createIcon(iconName, iconSize)
Creates a custom Leaflet icon from the icon manifest.

**Parameters:**
- `iconName` (string, optional): Icon identifier from [`manifest.js`](../../assets/images/manifest.js:1). Default: `'Hex_Logo'`
- `iconSize` (Array, optional): `[width, height]` in pixels. Default: `[32, 32]`

**Returns:**
- `L.Icon`: Leaflet icon instance

**Available Icon Names:**
Refer to [`manifest.js`](../../assets/images/manifest.js:1) for the complete list of available icons.

**Example:**
```javascript
const icon = createIcon('claimT5', [64, 64]);
const marker = L.marker([lat, lng], { icon: icon });
```

### GeoJSON Processing

#### validateGeoJson(untrustedString)
Validates and sanitizes user-provided GeoJSON strings.

**Parameters:**
- `untrustedString` (string): URL-encoded GeoJSON string

**Returns:**
- `Object`: Validated GeoJSON FeatureCollection

**Throws:**
- `Error`: If validation fails with descriptive message

**Validation Rules:**
- Must be valid JSON after URL decoding
- Must be a FeatureCollection (not array)
- Must contain features array
- HTML content is escaped in popupText
- Invalid iconNames default to 'waypoint'
- Invalid iconSizes default to [32, 32]

**Example:**
```javascript
try {
  const geoJson = validateGeoJson(encodedGeoJsonString);
  paintGeoJson(geoJson, targetLayer);
} catch (error) {
  console.error('GeoJSON validation failed:', error.message);
}
```

#### paintGeoJson(geoJson, layer, pan)
Renders validated GeoJSON to a Leaflet layer with custom styling.

**Parameters:**
- `geoJson` (Object): Validated GeoJSON FeatureCollection
- `layer` (L.Layer): Target Leaflet layer for rendering
- `pan` (boolean, optional): Whether to pan/zoom to features. Default: `true`

**Custom Rendering Features:**
- Point features become markers or CircleMarkers
- Polygon/LineString features get custom styling
- Popup binding with HTML escaping
- Automatic layer visibility control
- Camera control (flyTo/fitBounds)

---

## URL Parameters

The BitCraft Map supports various URL parameters for deep linking and data loading.

### Query Parameters

#### Resource and Enemy Loading
```
https://bitcraftmap.com/?regionId=2,3&resourceId=123,456&enemyId=789
```

**Parameters:**
- `regionId` (string): Comma-separated region IDs (1-9)
- `resourceId` (string): Comma-separated resource type IDs
- `enemyId` (string): Comma-separated enemy type IDs

**Validation:**
- Region IDs must match pattern: `^([1-9])(,([1-9]))*$`
- Resource/Enemy IDs must match pattern: `^([0-9]\d*)(,([0-9]\d*))*$`

#### GitHub Gist Integration
```
https://bitcraftmap.com/?gistId=8ecf9520d96e13908c060c871430ed37
```

**Parameters:**
- `gistId` (string): 32-character hexadecimal GitHub Gist ID

**Validation:**
- Must match pattern: `^[a-fA-F0-9]{32}$`

#### Live Player Tracking
```
https://bitcraftmap.com/?playerId=123456789
```

**Parameters:**
- `playerId` (string): Numeric player ID for WebSocket tracking

**Validation:**
- Must match pattern: `^[0-9]{0,32}$`

#### Feature Toggles
```
https://bitcraftmap.com/?heatmap=1
```

**Parameters:**
- `heatmap` (string): Any truthy value enables heatmap overlay

### URL Hash for GeoJSON
```
https://bitcraftmap.com/#%7B%22type%22%3A%22FeatureCollection%22...
```

The URL hash can contain URL-encoded GeoJSON for sharing custom waypoints. The system handles spaces and line breaks gracefully.

---

## GeoJSON Custom Properties

BitCraft Map extends standard GeoJSON with custom properties for enhanced map features.

### Point Feature Properties

#### Basic Display Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `popupText` | `string \| string[]` | — | Popup content. Arrays become multi-line with `<br>`. HTML is escaped. |
| `iconName` | `string` | `'waypoint'` | Icon identifier from icon manifest |
| `iconSize` | `[number, number]` | `[32, 32]` | Icon dimensions `[width, height]` in pixels |

#### Canvas Rendering Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `makeCanvas` | `boolean` | `false` | Render as CircleMarker instead of icon marker |
| `radius` | `number` | `1` | Circle radius in pixels (requires `makeCanvas: true`) |

#### Layer Control Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `turnLayerOn` | `string \| string[]` | — | Layer names to enable after rendering |
| `turnLayerOff` | `string \| string[]` | — | Layer names to disable after rendering |

**Available Layer Names:**
```javascript
[
  'treesLayer', 'templesLayer', 'ruinedLayer', 'banksLayer', 'marketsLayer',
  'waystonesLayer', 'waypointsLayer', 'claimT0Layer', 'claimT1Layer', 'claimT2Layer',
  'claimT3Layer', 'claimT4Layer', 'claimT5Layer', 'claimT6Layer', 'claimT7Layer',
  'claimT8Layer', 'claimT9Layer', 'claimT10Layer', 'caveT1Layer', 'caveT2Layer',
  'caveT3Layer', 'caveT4Layer', 'caveT5Layer', 'caveT6Layer', 'caveT7Layer',
  'caveT8Layer', 'caveT9Layer', 'caveT10Layer'
]
```

#### Camera Control Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `flyTo` | `[number, number]` | — | Small Hex coordinates for camera positioning |
| `zoomTo` | `number` | — | Leaflet zoom level (-6 to 6) |
| `noPan` | `boolean` | `false` | Disable automatic camera movement |

### Styling Properties (Polygons, Lines, Canvas)

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `color` | `string` | `'#3388ff'` | Stroke/border color (hex format) |
| `weight` | `number` | `3` | Stroke width in pixels |
| `opacity` | `number` | `1` | Stroke opacity (0-1) |
| `fillColor` | `string` | `'#3388ff'` | Fill color (hex format) |
| `fillOpacity` | `number` | `0.2` | Fill opacity (0-1) |

### Example GeoJSON with Custom Properties

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "popupText": ["Custom Waypoint", "Additional Info"],
        "iconName": "HexCoin3",
        "iconSize": [64, 64],
        "turnLayerOff": ["ruinedLayer", "treesLayer"],
        "flyTo": [15000, 15000],
        "zoomTo": 2
      },
      "geometry": {
        "type": "Point",
        "coordinates": [15000, 15000]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "makeCanvas": true,
        "radius": 100,
        "fillColor": "#ff0000ff",
        "fillOpacity": 0.3,
        "popupText": "Area of Interest"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [12000, 8000]
      }
    }
  ]
}
```

---

## WebSocket API

Real-time player tracking via WebSocket connection to external service.

### Connection Details
```javascript
const resubakaURL = "wss://craft-api.resubaka.dev/websocket";
const webSocket = new WebSocket(resubakaURL);
```

### Message Format

#### Subscribe to Player Updates
```json
{
  "t": "Subscribe",
  "c": {
    "topics": ["mobile_entity_state.{playerId}"]
  }
}
```

#### Player State Updates (Received)
```json
{
  "t": "MobileEntityState",
  "c": {
    "entity_id": 123456789,
    "location_x": 15000000,
    "location_z": 8000000,
    "destination_x": 16000000,
    "destination_z": 9000000
  }
}
```

**Coordinate Conversion:**
- Game coordinates are in thousandths (divide by 1000 for map coordinates)
- `location_x` → longitude, `location_z` → latitude
- Creates real-time player markers and movement trails

---

## Layer Management API

The [`library.js`](../../assets/js/library.js:1) provides a comprehensive layer registry system.

### Layer Registry Methods

#### createLayerRegistry(leafletMap)
Creates a new layer management instance.

**Returns:**
- `Object`: Layer registry with management methods

### Layer Management Methods

#### hasLayer(layerName)
Check if a layer exists in the registry.

**Parameters:**
- `layerName` (string): Unique layer identifier

**Returns:**
- `boolean`: True if layer exists

#### getLayer(layerName)
Retrieve a layer instance from the registry.

**Parameters:**
- `layerName` (string): Unique layer identifier

**Returns:**
- `L.Layer|null`: Leaflet layer instance or null

#### createLayer(layerName, layerType, options, addToMap)
Create or retrieve a layer.

**Parameters:**
- `layerName` (string): Unique layer identifier
- `layerType` (string, optional): Layer type. Default: `'group'`
- `options` (Object, optional): Layer-specific options
- `addToMap` (boolean, optional): Add to map immediately. Default: `true`

**Layer Types:**
- `'group'` → `L.layerGroup`
- `'feature'` → `L.featureGroup`
- `'geojson'` → `L.geoJSON`
- `'tile'` → `L.tileLayer`
- `'canvas'` → `L.canvas`
- `'svg'` → `L.svg`
- `'imageOverlay'` → `L.imageOverlay`

**Returns:**
- `L.Layer`: Created or existing layer

#### showLayer(layerName) / hideLayer(layerName)
Control layer visibility.

**Parameters:**
- `layerName` (string): Layer to show/hide

**Returns:**
- `boolean`: True if operation succeeded

#### toggleLayer(layerName)
Toggle layer visibility.

#### isLayerVisible(layerName)
Check if layer is currently visible.

### Example Usage

```javascript
const layerRegistry = createLayerRegistry(map);

// Create a new layer
const customLayer = layerRegistry.createLayer('myCustomLayer', 'group');

// Add markers to the layer
L.marker([lat, lng]).addTo(customLayer);

// Control visibility
layerRegistry.hideLayer('myCustomLayer');
layerRegistry.showLayer('myCustomLayer');

// Check state
if (layerRegistry.isLayerVisible('myCustomLayer')) {
  console.log('Layer is visible');
}
```

---

## Error Codes

### GeoJSON Validation Errors

| Error Message | Cause | Resolution |
|---------------|-------|------------|
| `"untrustedString be a string"` | Input is not a string | Ensure input is string type |
| `"Bad URI encoding"` | Invalid URL encoding | Check URL encoding format |
| `"Invalid JSON"` | JSON parsing failed | Validate JSON syntax |
| `"geoJson must not be an array"` | Root level is array | Wrap in FeatureCollection |
| `"geoJson doesnt have FeatureCollection"` | Missing type property | Set `type: "FeatureCollection"` |
| `"geoJson doesnt have features or features isnt array"` | Invalid features | Add `features` array |
| `"popupText must be string or array of strings"` | Invalid popupText type | Use string or string array |

### WebSocket Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| Connection failed | Network or server issues | Check network connectivity |
| Invalid playerId | Player ID validation failed | Use numeric player ID |

### API Request Errors

| Status Code | Meaning | Resolution |
|-------------|---------|------------|
| 400 | Bad Request | Check parameter format |
| 404 | Resource not found | Verify region/resource IDs |
| 429 | Rate limited | Implement request throttling |
| 500 | Server error | Retry request |

---

## Rate Limiting

### Backend API
- Current implementation uses KrakenD gateway
- Concurrent calls: 9 per endpoint
- No explicit rate limiting documented

### GitHub Gist API
- Subject to GitHub API rate limits
- 60 requests per hour for unauthenticated requests
- Use caching for frequently accessed gists

### WebSocket Connection
- One connection per player ID
- Automatic reconnection not implemented
- Handle connection drops gracefully

### Best Practices

1. **Cache Static Data**: Cache GeoJSON files and icons locally
2. **Batch Requests**: Combine multiple resource requests using comma-separated IDs
3. **Error Handling**: Always implement error handling for API calls
4. **Resource Management**: Clean up WebSocket connections when not needed

---

## Coordinate System Reference

### BitCraft Coordinate Systems

1. **Small Hex Coordinates**: Range 0-23040, used in game debug menu (F4)
2. **Small Floating Hex**: Fractional coordinates for precise positioning
3. **Map Coordinates**: Internal Leaflet coordinates after CRS transformation
4. **Display Coordinates**: N/E format shown to users (Small Hex ÷ 3)

### Conversion Examples

```javascript
// Game coordinates (from WebSocket) → Map coordinates
const mapLat = gameZ / 1000;
const mapLng = gameX / 1000;

// Map coordinates → Display coordinates (N/E)
const displayCoords = readableCoordinates(L.latLng(mapLat, mapLng));
// Returns [N, E] where N = lat/3, E = lng/3
```

### Coordinate Bounds

- **Game World**: 0 to 23040 in both dimensions
- **Map Display**: Scaled and projected through custom CRS
- **Leaflet Internal**: Transformed coordinates for rendering

---

## Integration Examples

### Adding Custom Markers via URL

```javascript
// Create GeoJSON
const customMarker = {
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "properties": {
      "popupText": "My Custom Location",
      "iconName": "HexCoin3"
    },
    "geometry": {
      "type": "Point",
      "coordinates": [15000, 15000]
    }
  }]
};

// Encode and add to URL
const encoded = encodeURIComponent(JSON.stringify(customMarker));
window.location.hash = encoded;
```

### Loading Dynamic Resource Data

```javascript
async function loadResourceData(regionIds, resourceIds) {
  const promises = [];
  
  for (const regionId of regionIds) {
    for (const resourceId of resourceIds) {
      const url = `https://api.bitcraftmap.com/region${regionId}/resource/${resourceId}`;
      promises.push(fetch(url).then(r => r.json()));
    }
  }
  
  const results = await Promise.all(promises);
  
  // Process and display results
  results.forEach(geoJson => {
    if (geoJson.features?.length > 0) {
      paintGeoJson(geoJson, waypointsLayer);
    }
  });
}
```

### Custom Layer Management

```javascript
// Create specialized layer for guild markers
const guildLayer = layerRegistry.createLayer('guildMarkers', 'feature');

// Add guild-specific styling
function addGuildMarker(guildData) {
  const marker = L.marker([guildData.lat, guildData.lng], {
    icon: createIcon('claimT10', [48, 48])
  }).bindPopup(`Guild: ${guildData.name}`);
  
  marker.addTo(guildLayer);
}

// Control guild layer visibility
document.getElementById('guildToggle').addEventListener('change', (e) => {
  if (e.target.checked) {
    layerRegistry.showLayer('guildMarkers');
  } else {
    layerRegistry.hideLayer('guildMarkers');
  }
});
```

---

*This API reference covers all public interfaces available in BitCraft Map. For implementation details, refer to the source files linked throughout this document.*