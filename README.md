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

## Roadmap

1 Finish the better coordinates system and clean up script
2 Finish the geojson sharing feature and release
3 make the higher resolution hexagon map with opencv and numpy (should be easy and high value)

## Wild ideas board

- Turn on / Turn off all waypoint
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




## Check later

- https://leafletjs.com/plugins.html#layer-switching-controls
- https://github.com/stefanocudini/leaflet-search/tree/master / https://opengeo.tech/maps/leaflet-search/
- https://worace.works/2022/02/23/kicking-the-tires-flatgeobuf/
- https://pasq.fr/flatgeobuf-soyons-binaire
- https://flatgeobuf.org/examples/leaflet/
- https://github.com/mapbox/geobuf


## List of possible filters
- Global filter
    - Filter by region
    - Filter by biome
- Claims
    - Filter by tier
    - Filter / Search by name

- Filter per profession
    - Foraging
    - Hunting
    - Mining
    - Forestry
    - Fishing

- Resources
    - Filter by tier

- Caves
    - Filter by tier
    - Filter by size

## Ui design
- Menu
    - Colapse
    - Move around
    - Pin to current position
    - Load settings
    - Save settings
    - Share settings

- Later
    - Resource Finder in range [circle or draw a shape]

## Some inspiration

- https://www.newworld-map.com/
- https://interactive-game-maps.github.io/
- https://stackoverflow.com/questions/12262163/what-are-leaflet-and-mapbox-and-what-are-their-differences
- (ablion map) view-source:https://albiononline2d.com/public/js/map.js https://albiononline2d.com/en/map/2202

- https://genshin-impact-map.appsample.com/?map=teyvat
- https://act.hoyolab.com/ys/app/interactive-map/index.html
