# BitCraft Map Development Notes

*This document contains research findings, feature ideas, technical considerations, and development roadmap for the BitCraft Map project.*

---

## 🔬 Technology Research & External Libraries

### Core Libraries Under Consideration
- **[MessagePack](https://msgpack.org/)** - Efficient binary serialization format for data compression
- **[GeoJSON](https://geojson.org/)** - Standard format for encoding geographic data structures
  - [GeoJSON Tutorial for Beginners](https://medium.com/@dmitry.sobolevsky/geojson-tutorial-for-beginners-ce810d3ff169)
  - [Leaflet GeoJSON Examples](https://leafletjs.com/examples/geojson/)
  - [GeoJSON Validator](https://geojsonlint.com/)
- **[H3 Geo](https://h3geo.org/)** - Hexagonal hierarchical geospatial indexing system
- **[Mapbox Geobuf](https://github.com/mapbox/geobuf)** - Compact binary encoding for geographic data

### Visualization & Mapping
- **[D3.js](https://d3js.org/)** - Data visualization library
  - [Hexbin Map Examples](https://d3-graph-gallery.com/graph/hexbinmap_geo_basic.html)
  - [Self-Organizing Maps with Hexagonal Layout](https://www.visualcinnamon.com/2013/07/self-organizing-maps-creating-hexagonal/)
  - [Adding Boundaries to Hexagonal Maps](https://www.visualcinnamon.com/2013/07/self-organizing-maps-adding-boundaries/)
- **[p5.js](https://p5js.org/)** - Creative coding library for interactive graphics
- **[Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/api/)** - Vector maps and WebGL rendering

### Advanced Features to Research Later
- **[Leaflet Plugins](https://leafletjs.com/plugins.html#layer-switching-controls)** - Additional layer switching controls
- **[Leaflet Search Plugin](https://github.com/stefanocudini/leaflet-search)** - Enhanced search functionality ([Demo](https://opengeo.tech/maps/leaflet-search/))
- **[FlatGeobuf](https://flatgeobuf.org/examples/leaflet/)** - High-performance binary geographic format
  - [Article: "Let's Be Binary"](https://pasq.fr/flatgeobuf-soyons-binaire)
  - [Performance Comparison](https://worace.works/2022/02/23/kicking-the-tires-flatgeobuf/)
- **[Mapbox GeoJSON Hint](https://www.npmjs.com/package/@mapbox/geojsonhint)** - GeoJSON validation utility

---

## 🚀 Feature Roadmap & Ideas

### 🎯 Priority Features
- **Coordinate System Enhancements**
  - Move coordinate finder to a more accessible location
  - Add mouse cursor coordinate display
  - Implement coordinate-to-biome calculator
  - Display chunk coordinates

### 🖥️ User Interface Improvements
- **Map Controls**
  - Master toggle for all waypoints (turn on/off all at once)
  - New interface following BitCraft's visual style
  - Drawing tools for user annotations on the map
  - User-controlled layer ordering (what icons appear on top)
  - Comprehensive legend system

- **Settings & Personalization**
  - Save user settings via cookies or localStorage
  - Share settings between users
  - Collapsible and movable menu panels
  - Pin menu to current position

### 👥 Player Data Features
- **Waystone Management**
  - Display player waystone locations
  - Show missing waystones for players
  - Calculate closest known waystone to any location
  
- **Player Analytics**
  - Player heat density visualization
  - Real-time player location tracking (if API available)
  - Live exploration level monitoring
  - *Wild idea*: Live player chat bubbles on map

### 💰 Market Integration
- **Economic Data Display**
  - Market data overlay for each waypoint
  - Best price analysis (1st, 5th, 10th percentile)
  - Market volume metrics:
    - Number of active orders
    - Total buy orders in hexcoins
    - Alternative volume calculation methods

### 🏰 Empire & Territory Features
- **Political Boundaries**
  - Empire border visualization
  - Watchtower locations and status
  - Watchtower expiration and war status tracking
  - Search functionality by empire name
  - Tower count per empire
  - Highlight empire capitals
  - Watchtower placement optimization algorithms

### 🗺️ Navigation & Pathfinding
- **Smart Routing System**
  - Input: Starting position or "locate me" by name
  - Input: Destination coordinates
  - Options:
    - Waystone usage preferences
    - Available energy
    - Inventory capacity considerations
    - Cargo transport requirements
  - Calculate water vs boat deployment efficiency
  - Display total travel time estimates

- **Navigation Overlay** *(Advanced)*
  - External overlay system showing directional arrows
  - Integration with BitCraft client for real-time guidance

### 🌍 World Data & Visualization
- **Geographic Information**
  - Region name overlays
  - Regional grid system
  - Chunk boundaries
  - Terrain elevation-based pathfinding
  - Walkable zone calculation (cart-accessible areas)

- **Resource Management**
  - Resource finder within specified range/shape
  - Resource screenshots lexicon
  - Tier-based filtering system
  - Professional category filters (Foraging, Hunting, Mining, etc.)

- **Dynamic Content**
  - BitCraft in-game time display
  - Traveler quest reset countdown
  - Active job locations
  - Dropped item tracking *(experimental)*

### 🎮 Advanced Features
- **3D Integration**
  - 3D scene rendering for resource visualization
  - Match in-game resource appearance

- **Map Segmentation**
  - Optional: Divide map into 9 sections for performance
  - Lazy loading of map segments

---

## 🛠️ Technical Implementation

### 🔒 Security Considerations

#### GeoJSON URL Hash Implementation
**Potential Vulnerabilities:**
- **DoS Attacks**: Excessive markers causing performance issues
- **XSS Risks**: Malicious script injection
- **Data Corruption**: Malformed GeoJSON strings

**Mitigation Strategies:**
- Input validation and sanitization
- Marker count limitations
- GeoJSON structure validation
- Content Security Policy enforcement

**Useful Tools:**
- [Remove Extra Spaces](https://www.text-utils.com/remove-extra-spaces/)
- [Base64 Encoding](https://www.base64encode.org/)

### 🎛️ Filter System Design

#### Global Filters
- **Geographic**: Filter by region or biome
- **Administrative**: Filter by empire or territory

#### Content-Specific Filters
- **Claims**: Tier-based filtering, name search functionality
- **Resources**: Tier-based organization
- **Caves**: Tier and size-based filtering
- **Professional Categories**: Foraging, Hunting, Mining, Forestry, Fishing

### 🎨 User Experience Design

#### Menu System
- **Collapsible Interface**: Space-efficient design
- **Drag-and-Drop**: Repositionable UI elements
- **Position Locking**: Pin interface to map location
- **Settings Management**: Load/save/share configurations

---

## 📊 Reference Data & Configuration

### 🎨 Tier Color Scheme
```javascript
const TIER_COLORS = {
    1: '#A0A0A0',  // Gray
    2: '#E8B57A',  // Bronze/Orange
    3: '#A0D2B2',  // Light Green
    4: '#3B60E4',  // Blue
    5: '#9C4A93',  // Purple
    6: '#B03A48',  // Red
    7: '#EEDD7A',  // Yellow
    8: '#4CA3A6',  // Teal
    9: '#3A3A3A',  // Dark Gray
    10: '#BFD4E0'  // Light Blue
};
```

### 📐 Bounding Box Implementation
**Research Resources:**
- [Dynamic Zoom Based on Bounding Box](https://gis.stackexchange.com/questions/76113/dynamically-set-zoom-level-based-on-a-bounding-box)
- [GeoJSON Bounding Box Concepts](https://www.google.com/search?q=what+is+a+bounding+box+geojson)
- [Leaflet Visible Map Bounds](https://stackoverflow.com/questions/22948096/get-the-bounding-box-of-the-visible-leaflet-map)

---

## 🎯 Development Priorities

### Phase 1: Core Improvements
- [ ] Rewrite project in TypeScript for better maintainability
- [ ] Implement database queries instead of relying on external APIs
- [ ] Add comprehensive filter count displays
- [ ] Improve coordinate system integration

### Phase 2: Data Integration
- [ ] Replace Bitjita API dependency with direct database access
- [ ] Implement caching mechanisms for improved performance
- [ ] Add real-time data synchronization

### Phase 3: Advanced Features
- [ ] Community vs spoiler map toggle for launch periods
- [ ] Advanced pathfinding algorithms
- [ ] Market data integration
- [ ] Player tracking systems

---

## 🎨 Design Inspiration

### Reference Projects
- **[New World Map](https://www.newworld-map.com/)** - Clean interface, comprehensive filtering
- **[Interactive Game Maps Collection](https://interactive-game-maps.github.io/)** - Various implementation approaches
- **[Albion Online 2D Map](https://albiononline2d.com/en/map/2202)** - Performance optimization techniques ([Source](view-source:https://albiononline2d.com/public/js/map.js))
- **[Genshin Impact Map](https://genshin-impact-map.appsample.com/?map=teyvat)** - User experience patterns
- **[HoYoLab Interactive Map](https://act.hoyolab.com/ys/app/interactive-map/index.html)** - Mobile-responsive design

### Technical References
- [Leaflet vs Mapbox Comparison](https://stackoverflow.com/questions/12262163/what-are-leaflet-and-mapbox-and-what-are-their-differences)

---

*Last updated: 2024 - This document serves as a living reference for BitCraft Map development and should be updated as the project evolves.*