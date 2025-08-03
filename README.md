## 🗺️
https://bitcraftmap.com

## Things I found

- https://msgpack.org/
- https://geojson.org/
    - https://medium.com/@dmitry.sobolevsky/geojson-tutorial-for-beginners-ce810d3ff169
    - https://leafletjs.com/examples/geojson/
    - https://geojsonlint.com/
- https://h3geo.org/
- https://d3js.org/
    - https://d3-graph-gallery.com/graph/hexbinmap_geo_basic.html
    - https://www.visualcinnamon.com/2013/07/self-organizing-maps-creating-hexagonal/
    - https://www.visualcinnamon.com/2013/07/self-organizing-maps-adding-boundaries/
- https://p5js.org/
- https://docs.mapbox.com/mapbox-gl-js/api/
- https://github.com/mapbox/geobuf

## Check later
- https://leafletjs.com/plugins.html#layer-switching-controls
- https://github.com/stefanocudini/leaflet-search/tree/master / https://opengeo.tech/maps/leaflet-search/

## Wild ideas board

- Lazy loading of data
- Do everything for performace and ease of use
- New interface that follow bitcraft style
- Pathfinder using terrain elevation data
- Coordinates to biome calculator
- Rewrite to Typescript
- Query the database instead of getting data from bitjita
- Calculate walkable zones (ie where cart can go because there is no water)
- Do a community map instead of a spoiler map at launch
- When you search, searching doesnt search in other poi than claims (ruined cities, temple etc..) to fix

- Players data
    - Show player waystone
    - Show player missing waystones
    - Calculate player heat density zones
    - Show players on the map dynamically
    - See people exploration level in real time

- Market data
    - Show market data for each waypoints
    - Best prices for this market [1/5/10 percentile of prices]
    - Volume of the market calculated in number of orders, total buy order in hexcoins, other methods...

- Empires :
    - Show empire borders
    - Show watchtowers
    - More info about watchtowers (expiration / war...)

- Misc :
    - Show region names
    - Show regions grid
    - Show chunks grid


## Pass geoJson with the location.hash

- Possibles attacks : DOS (too many markers) / XSS / Unexpected behavior if malformed string
- https://www.text-utils.com/remove-extra-spaces/
- https://www.base64encode.org/



// Check later 

- https://worace.works/2022/02/23/kicking-the-tires-flatgeobuf/
- https://pasq.fr/flatgeobuf-soyons-binaire
- https://flatgeobuf.org/examples/leaflet/
- https://github.com/mapbox/geobuf