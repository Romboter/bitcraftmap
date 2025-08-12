      // Todo
      calculateExpiration = function(updatedAT, tiles, supplies) {
        suppliesPerMin = 0;

        if (tiles < 1001)  { suppliesPerMin = tiles * 0.01 * 60   } else
        if (tiles < 2001)  { suppliesPerMin = tiles * 0.0125 * 60 } else
        if (tiles < 3001)  { suppliesPerMin = tiles * 0.02 * 60   } else 
        if (tiles < 4001)  { suppliesPerMin = tiles * 0.025 * 60  } else 
        if (tiles < 6001)  { suppliesPerMin = tiles * 0.03 * 60   } else 
        if (tiles < 8001)  { suppliesPerMin = tiles * 0.035 * 60  } else 
        if (tiles < 10001) { suppliesPerMin = tiles * 0.04 * 60   } else 
        if (tiles < 13001) { suppliesPerMin = tiles * 0.05 * 60   } else 
        if (tiles < 16001) { suppliesPerMin = tiles * 0.06 * 60   }
        else { suppliesPerMin = tiles * 0.07 * 60 }

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



            function loadGeoJsonFromUrl() {
        try {

          if (!location.hash) return;

          const hash = 
            location.hash.slice(1)
            .replace(/%20/g, '')
            .replace(/%22/g, '"');

          if (!hash) return;
          console.log('Found hash: ' + hash)


          const geoJson = JSON.parse(hash);
          console.log('Found valid geoJson: ' + geoJson);

          if (Array.isArray(geoJson)) throw new Error("geoJson must not be an array");

          L.geoJSON(geoJson, {
            pointToLayer: function(feature, latlng) {

              const waypointIcon = L.icon({
                iconUrl: "assets/icons/waypoint.png",
                iconSize: [44, 44],
                iconAnchor: [22, 22],
                popupAnchor: [0, -22]
              });

              const bitcraftCoords = L.latLng(latlng.lat / 1.1547005, latlng.lng);
              console.log(bitcraftCoords);
              console.log('what ? ?');

              map.createPane("markerOnTop");
              map.getPane("markerOnTop").style.zIndex = 999;

              return L.marker(
                bitcraftCoords,
                { icon: waypointIcon, pane: "markerOnTop" }
              );
            },

            style: function(feature) {
              return {
                color: feature.properties?.color || "#3388ff",
                weight: feature.properties?.weight || 3,
                opacity: feature.properties?.opacity || 1,
                fillColor: feature.properties?.fillColor || "#3388ff",
                fillOpacity: feature.properties?.fillOpacity ?? 0.2
              };
            },

            onEachFeature: function(feature, layer) {
              if (feature.properties?.name) {
                layer.bindPopup(feature.properties.name);
              }
            }
          }).addTo(map);

          allClaims.addTo(map);

          if (geoJson['properties']['flyTo'] || geoJson['properties']['zoomTo']) {

            // Data validation
            if (!geoJson['properties']['flyTo']) {
              geoJson['properties']['flyTo'] = [3838 / 1.15, 3838];
            }

            if (!geoJson['properties']['zoomTo']) {
              geoJson['properties']['zoomTo'] = 0;
            }

            if (  geoJson['properties']['flyTo'][0] < 0 
              ||  geoJson['properties']['flyTo'][0] > 7800
              ||  geoJson['properties']['flyTo'][1] < 0
              ||  geoJson['properties']['flyTo'][1] > 7800
            ) {
              geoJson['properties']['flyTo'] = [3838 / 1.15, 3838];
            }

            if (geoJson['properties']['zoomTo'] < -10 || geoJson['properties']['zoomTo'] > 10) {
              geoJson['properties']['zoomTo'] = 0;
            }

            map.flyTo( 
              [geoJson['properties']['flyTo'][1] / 1.1547005, geoJson['properties']['flyTo'][0]],
              geoJson['properties']['zoomTo']
            );
          };

        } catch (error) {
          console.log(error);
          return;
        } 
      };

      loadGeoJsonFromUrl();