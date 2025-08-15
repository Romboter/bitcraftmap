function costPerSecond(tiles, stability = 1) {
  if (tiles < 1001)  { return tiles * 0.01   * stability * 60 } else
  if (tiles < 2001)  { return tiles * 0.0125 * stability * 60 } else
  if (tiles < 3001)  { return tiles * 0.02   * stability * 60 } else 
  if (tiles < 4001)  { return tiles * 0.025  * stability * 60 } else 
  if (tiles < 6001)  { return tiles * 0.03   * stability * 60 } else 
  if (tiles < 8001)  { return tiles * 0.035  * stability * 60 } else 
  if (tiles < 10001) { return tiles * 0.04   * stability * 60 } else 
  if (tiles < 13001) { return tiles * 0.05   * stability * 60 } else 
  if (tiles < 16001) { return tiles * 0.06   * stability * 60 } else
  {                    return tiles * 0.07   * stability * 60 }
}

map.on('click', function(e) {
  const latlng = e.latlng;
  const marker = L.marker([latlng.lat, latlng.lng])
  .addTo(map)
  .bindPopup(`Marker at ${latlng.lat.toFixed(0)}, ${latlng.lng.toFixed(0)}`);
  marker.on('contextmenu', function() {
    map.removeLayer(marker);
  });
});