'use strict';

const imageWidth = 2400;
const imageHeight = 2400;
const bitcraftWidth = 23040;  
const bitcraftHeight = 23040;
const bitcraftHeightWithOcean = 23040 * 1.1547005;

const s = 1.1547005; // horizontal stretch of the *world*; we squish input X by 1/s

const SquishXProjection = {
    project(latlng) {
        const x = latlng.lng;  // treat "lng" as your game X
        const y = latlng.lat;  // treat "lat" as your game Y
        const X = x;
        const Y = -y / s ;          // Leaflet's layer point Y goes down; negate to keep Y-up world
        return new L.Point(X, Y);
    },
    unproject(point) {
        const X = point.x;
        const Y = point.y;
        const x = X;
        const y = -Y * s;
        return new L.LatLng(y, x);
    },
    bounds: L.bounds([-Infinity, -Infinity], [Infinity, Infinity])
};

// 2) Build a CRS using that projection
const CRS_SquishX = L.extend({}, L.CRS.Simple, {
    projection: SquishXProjection,
    // No extra Transformation: we've baked the scaling/flip into project/unproject
    transformation: new L.Transformation(1, 0, 1, 0),
    scale(z) { return Math.pow(2, z); },
    infinite: false
});


const map = L.map('map', {
    crs: CRS_SquishX,
    minZoom: -6,
    maxZoom: 6,
    zoomSnap: 0.1,
    attributionControl: false, // Remove watermark
    zoomControl: false, // Remove the zoom control top left
    preferCanvas: true,
    boxZoom: false
});

//               N                     E
//              lat                   lgt
//           locationZ             locationX
//         bottom to top         left to right
//               v                     v

const mapBounds = [[0, 0], [bitcraftHeight, bitcraftWidth]];
const mapBoundsWithOcean = [[0, 0], [bitcraftHeightWithOcean, bitcraftWidth]];

L.imageOverlay('assets/maps/map.png', mapBoundsWithOcean).addTo(map);
map.fitBounds(mapBounds);


// Overwriting the default icon parameters
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    "iconUrl": iconsManifest['Hex_Logo'],
    "iconRetinaUrl": iconsManifest['Hex_Logo'],
    "iconSize": [32,32],
    "iconAnchor": [16,16],
    "popupAnchor": [0,-16],
    "tooltipAnchor": [-16,0],
    "shadowUrl": null,
    "shadowSize": null,
    "shadowAnchor": null,
    "shadowRetinaUrl": null
});

function createIcon(iconName = 'Hex_Logo', iconSize = [32,32]) {
    const [w = 32, h = 32] = iconSize || [];
    return L.icon({
        iconUrl: iconsManifest[iconName],
        iconSize: [w, h],
        iconAnchor: [w/2, h/2],
        popupAnchor: [0, -h/2],
        shadowUrl: null,
        shadowSize: null,
        shadowAnchor: null
    });
};

const caveIcons = [
createIcon('t1'),createIcon('t2'),createIcon('t3'),createIcon('t4'),createIcon('t5'),
createIcon('t6'),createIcon('t7'),createIcon('t8'),createIcon('t9'),createIcon('t10')
];

const claimIcons = [
createIcon('claimT0'),createIcon('claimT1'),createIcon('claimT2'),createIcon('claimT3'),createIcon('claimT4'),createIcon('claimT5'),
createIcon('claimT6'),createIcon('claimT7'),createIcon('claimT8'),createIcon('claimT9'),createIcon('claimT10')
];

const ruinedIcon = createIcon('ruinedCity');
const templeIcon = createIcon('temple');
const treeIcon = createIcon('travelerTree');

const treesLayer = L.layerGroup();
const ruinedLayer = L.layerGroup();
const templesLayer = L.layerGroup();
const banksLayer = L.layerGroup();
const marketsLayer = L.layerGroup();
const waystonesLayer = L.layerGroup();
const gridsLayer =  L.layerGroup();
const waypointsLayer = L.layerGroup();

const claimT0Layer = L.layerGroup();
const claimT1Layer = L.layerGroup();
const claimT2Layer = L.layerGroup();
const claimT3Layer = L.layerGroup();
const claimT4Layer = L.layerGroup();
const claimT5Layer = L.layerGroup();
const claimT6Layer = L.layerGroup();
const claimT7Layer = L.layerGroup();
const claimT8Layer = L.layerGroup();
const claimT9Layer = L.layerGroup();
const claimT10Layer = L.layerGroup();

const claimLayers = [
claimT0Layer, claimT1Layer, claimT2Layer, claimT3Layer, claimT4Layer, claimT5Layer,
claimT6Layer, claimT7Layer, claimT8Layer, claimT9Layer, claimT10Layer
];

const allClaims = L.layerGroup(claimLayers);
const searchGroup = L.layerGroup(claimLayers.concat(ruinedLayer));

const caveT1Layer = L.layerGroup();
const caveT2Layer = L.layerGroup();
const caveT3Layer = L.layerGroup();
const caveT4Layer = L.layerGroup();
const caveT5Layer = L.layerGroup();
const caveT6Layer = L.layerGroup();
const caveT7Layer = L.layerGroup();
const caveT8Layer = L.layerGroup();
const caveT9Layer = L.layerGroup();
const caveT10Layer = L.layerGroup();

const caveLayers = [
caveT1Layer, caveT2Layer, caveT3Layer, caveT4Layer, caveT5Layer,
caveT6Layer, caveT7Layer, caveT8Layer, caveT9Layer, caveT10Layer
];

const allCaves = L.layerGroup(caveLayers);

const genericToggle = {
"Wonders": treesLayer,
"Temples": templesLayer,
"Ruined Cities": ruinedLayer,
"Banks": banksLayer,
"Markets": marketsLayer,
"Waystones": waystonesLayer,
"Grids": gridsLayer,
"Waypoints": waypointsLayer,
};

const claimsToggle = {
"Claims": allClaims
};

const claimsTierToggle = {
"Claims T1": claimT1Layer,
"Claims T2": claimT2Layer,
"Claims T3": claimT3Layer,
"Claims T4": claimT4Layer,
"Claims T5": claimT5Layer,
"Claims T6": claimT6Layer,
"Claims T7": claimT7Layer,
"Claims T8": claimT8Layer,
"Claims T9": claimT9Layer,
"Claims T10": claimT10Layer
};

const cavesToggle = {
"Caves": allCaves
};

const cavesTierToggle = {
"Caves T1": caveT1Layer,
"Caves T2": caveT2Layer,
"Caves T3": caveT3Layer,
"Caves T4": caveT4Layer,
"Caves T5": caveT5Layer,
"Caves T6": caveT6Layer,
"Caves T7": caveT7Layer,
"Caves T8": caveT8Layer,
"Caves T9": caveT9Layer,
"Caves T10": caveT10Layer
};

const allLayers = {
treesLayer, templesLayer, ruinedLayer, banksLayer, marketsLayer, waystonesLayer, waypointsLayer,
claimT0Layer, claimT1Layer, claimT2Layer, claimT3Layer, claimT4Layer, claimT5Layer,
claimT6Layer, claimT7Layer, claimT8Layer, claimT9Layer, claimT10Layer,
caveT1Layer, caveT2Layer, caveT3Layer, caveT4Layer, caveT5Layer,
caveT6Layer, caveT7Layer, caveT8Layer, caveT9Layer, caveT10Layer
};

// This is leaflet.search plugin configuration
// This plugin need a "title" parameter in each marker to find stuff
const searchControlOptions = {
position:'topleft',		
layer: searchGroup,
initial: false,
marker: false,
firstTipSubmit: true,
zoom: 0
};
const searchControl = new L.Control.Search(searchControlOptions);

// Load the marker if it is no already on the map
searchControl.on('search:locationfound', function(marker) {
if (!map.hasLayer(marker.layer)) {
    map.addLayer(marker.layer);
}
});

// -------------------------------------- //
// This is getting replaced
// -------------------------------------- //
async function loadTreesGeoJson() {
const file = await fetch('assets/markers/trees.geojson');
const geojsonData = await file.json();
L.geoJSON(geojsonData, {
    pointToLayer: function(feature, latlng) {
    
    const coords = readableCoordinates(latlng);
    const name = feature.properties.name + '<br>';
    const loc = 'N '+ coords[0] + ' E ' + coords[1];
    const popupText = name + loc;

    return L.marker(
        latlng,
        { icon: treeIcon }
    )
    .bindPopup(popupText)
    .addTo(treesLayer);
    }
});
};
async function loadTemplesGeoJson() {
const file = await fetch('assets/markers/temples.geojson');
const geojsonData = await file.json();
L.geoJSON(geojsonData, {
    pointToLayer: function(feature, latlng) {

    const coords = readableCoordinates(latlng);
    const name = feature.properties.name + '<br>';
    const loc = 'N '+ coords[0] + ' E ' + coords[1];
    const popupText = name + loc;

    return L.marker(
        latlng,
        { icon: templeIcon }
    )
    .bindPopup(popupText)
    .addTo(templesLayer);
    }
});
};
async function loadRuinedGeoJson() {
const file = await fetch('assets/markers/ruined.geojson');
const geojsonData = await file.json();
L.geoJSON(geojsonData, {
    pointToLayer: function(feature, latlng) {

    const coords = readableCoordinates(latlng);
    const name = feature.properties.name + '<br>';
    const loc = 'N '+ coords[0] + ' E ' + coords[1];
    const popupText = name + loc;

    return L.marker(
        latlng,
        { 
        title: feature.properties.name + ' N '+ coords[0] + ' E ' + coords[1],
        icon: ruinedIcon
        }
    )
    .bindPopup(popupText)
    .addTo(ruinedLayer);
    }
});
};
async function loadClaimsGeoJson() {
const file = await fetch('assets/markers/claims.geojson');
const geojsonData = await file.json();
L.geoJSON(geojsonData, {
    pointToLayer: function(feature, latlng) {

    const coords = readableCoordinates(latlng);
    const name = '<a href="' + 'https://bitjita.com/claims/' + feature.properties.entityId + '" target="_blank">' + feature.properties.name + '</a>';
    const tier = ' (T' + feature.properties.tier + ')' + '<br>';
    const loc = 'N '+ coords[0] + ' E ' + coords[1] + '<br>';
    const has_bank = 'Bank : ' + (feature.properties.has_bank ? 'Yes' : 'No') + '<br>';
    const has_market = 'Market : ' + (feature.properties.has_market ? 'Yes' : 'No') + '<br>';
    const has_Waystone = 'Waystone : ' + (feature.properties.has_waystone ? 'Yes' : 'No');
    const popupText = name + tier + loc + has_bank + has_market + has_Waystone;

    const marker = L.marker(
        latlng,
        {
        title: feature.properties.name + ' N '+ coords[0] + ' E ' + coords[1],
        icon: claimIcons[feature.properties.tier]
        }
    );

    marker.bindPopup(popupText)
    marker.addTo(claimLayers[feature.properties.tier]);

    if (feature.properties.has_bank) {
        marker.addTo(banksLayer)
    }
    if (feature.properties.has_market) {
        marker.addTo(marketsLayer)
    }
    if (feature.properties.has_waystone) {
        marker.addTo(waystonesLayer)
    }

    return marker;
    }
});
};
async function loadCavesGeoJson() {
const file = await fetch('assets/markers/caves.geojson');
const geojsonData = await file.json();
L.geoJSON(geojsonData, {
    pointToLayer: function(feature, latlng) {

    const coords = readableCoordinates(latlng);
    const name = feature.properties.name + '<br>';
    const loc = 'N '+ coords[0] + ' E ' + coords[1];
    const popupText = name + loc;

    return L.marker(
        latlng,
        { icon: caveIcons[feature.properties.tier-1] }
    )
    .bindPopup(popupText)
    .addTo(caveLayers[feature.properties.tier-1]);
    }
});
};
// -------------------------------------- //
// This is getting replaced
// -------------------------------------- //

// Function to convert to N E coordinate people know about
function readableCoordinates(latlng) {
    return [Math.round(latlng.lat / 3), Math.round(latlng.lng / 3)]; 
};

// Bit of code to get the position at the mouse and display it
map.on('mousemove', function (e) {
    const coordDisplay = document.getElementById('coords');
    const coords = readableCoordinates(e.latlng);
    coordDisplay.innerText = 'N: ' + coords[0] + ' E: ' + coords[1];
});

function loadGeoJsonFromHash() {
    const hashFromUrl = location.hash.slice(1);
    if(!hashFromUrl) return;
    const geoJson = validateGeoJson(hashFromUrl);
    paintGeoJson(geoJson, waypointsLayer);
    map.addLayer(waypointsLayer);
};

async function getLatestGistRaw(gistId) {
    if (!/^[a-fA-F0-9]{32}$/.test(gistId)) {
        throw new Error('gistId is invalid');
    };
    const baseApi = 'https://api.github.com/gists/';
    let lastGistCommitVersion;
    try {
        const gistCommits = await fetch(baseApi + gistId + '/commits');
        const gistCommitsJson = await gistCommits.json();
        if (!Array.isArray(gistCommitsJson) || gistCommitsJson.length === 0) {
            throw new Error('No commits found for this gist');
        }
        lastGistCommitVersion = gistCommitsJson[0].version;
    } catch (error) { console.log(error); } 
    let lastGistRawUrl;
    try {
        const gistInfo = await fetch(baseApi + gistId + '/' + lastGistCommitVersion);
        const gistInfoJson = await gistInfo.json();
        const filesNames = gistInfoJson.files || {};
        if (filesNames.length === 0) {
            throw new Error('No files found in this gist');
        } 
        lastGistRawUrl = Object.values(filesNames)[0].raw_url;
    } catch (error) { console.log(error); }
    let gistContent;
    try {
        const gistContentRaw = await fetch(lastGistRawUrl);
        gistContent = await gistContentRaw.text();
    } catch (error) { console.log(error); }
    return gistContent;
};

async function loadGeoJsonFromGist() {
    const gistIdFromUrl = new URLSearchParams(window.location.search).get('gistId');
    if(!gistIdFromUrl) return;
    const gistContent = await getLatestGistRaw(gistIdFromUrl)
    const geoJson = validateGeoJson(gistContent);
    paintGeoJson(geoJson, waypointsLayer);
    map.addLayer(waypointsLayer);
};

async function loadGeoJsonFromFile(fileUrl) {
    const file = await fetch(fileUrl);
    const content = await file.text()
    const geoJson = validateGeoJson(content);
    paintGeoJson(geoJson, gridsLayer);
};

function paintGeoJson(geoJson, layer) {
L.geoJSON(geoJson, {
    pointToLayer: function(feature, latlng) {

    if (feature.properties?.type === 'tooltip') {
        return new L.popup(
            latlng,
            {autoPan: false, autoClose: false}
        ).setContent(feature.properties.popupText);
    }

    if (feature.properties?.makeCanvas) {
        if (feature.properties?.radius) {
            return new L.CircleMarker(latlng, {radius: feature.properties.radius});
        } else {
            return new L.CircleMarker(latlng, {radius: 1});
        } 
    }

    map.createPane('markerOnTop');
    map.getPane('markerOnTop').style.zIndex = 999;

    const waypointIcon = createIcon('waypoint');

    return L.marker(
        latlng,
        { icon: waypointIcon, pane: 'markerOnTop' }
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
    if (feature.properties?.popupText) {
        const popupText = feature.properties.popupText;
        let finalPopupText = '';

        if (Array.isArray(popupText)) {
        for (const line of popupText) {
            finalPopupText += line + '<br>';
        }
        } else {
        finalPopupText = popupText;
        }
        layer.bindPopup(finalPopupText);
    }

    if (feature.properties?.turnLayerOn) {
        if (Array.isArray(feature.properties.turnLayerOn)) {
        for (const layerName of feature.properties.turnLayerOn) {
            const layer = allLayers[layerName];
            if (layer) map.addLayer(layer);
        }
        } else {
        const layer = allLayers[feature.properties.turnLayerOn];
        if (layer) map.addLayer(layer);
        }
    }

    if (feature.properties?.turnLayerOff) {
        if (Array.isArray(feature.properties.turnLayerOff)) {
        for (const layerName of feature.properties.turnLayerOff) {
            const layer = allLayers[layerName];
            if (layer) map.removeLayer(layer);
        }
        } else {
        const layer = allLayers[feature.properties.turnLayerOff];
        if (layer) map.removeLayer(layer);
        }
    }

    if (feature.properties?.flyTo && feature.properties?.zoomTo) {
        map.flyTo(feature.properties.flyTo, feature.properties.zoomTo);
    } else if (layer?.getBounds && !feature.properties.noPan) {
        map.fitBounds(layer.getBounds());
    }
    }
}).addTo(layer);
};

// Default layer to show on map opening
treesLayer.addTo(map);
templesLayer.addTo(map);
ruinedLayer.addTo(map);
searchControl.addTo(map);

L.control.layers(null, genericToggle, { collapsed: false }).addTo(map);
L.control.layers(null, claimsToggle, { collapsed: false }).addTo(map);
L.control.layers(null, claimsTierToggle, { collapsed: false }).addTo(map);
L.control.layers(null, cavesToggle, { collapsed: false }).addTo(map);
L.control.layers(null, cavesTierToggle, { collapsed: false }).addTo(map);

function escapeHTML(string) {
    return string
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#x27;");
};

function validateGeoJson(untrustedString) {

    if (untrustedString.constructor.name !== 'String') {
        throw new Error('untrustedString be a string');
    }

    console.log(untrustedString)
    let decodedString;
    try { decodedString = decodeURIComponent(untrustedString); }
    catch { throw new Error('Bad URI encoding'); }

    let jsonFormString;
    console.log(decodedString)
    try { jsonFormString = JSON.parse(decodedString); }
    catch { throw new Error('Invalid JSON'); }

    if (Array.isArray(jsonFormString)) {
        throw new Error('geoJson must not be an array');
    }

    if (jsonFormString.type !== 'FeatureCollection') {
        throw new Error('geoJson doesnt have FeatureCollection');
    }

    if (!jsonFormString.features || !Array.isArray(jsonFormString.features)) {
        throw new Error('geoJson doesnt have features or features isnt array');
    }

    for (const feature of jsonFormString.features) {

        if (feature.properties?.iconName) {
            // iconName must be a string
            if (feature.properties.iconName.constructor.name !== 'String') {
                feature.properties.iconName = 'waypoint';
            }

            // iconName must be present in the iconsManifest list
            if (feature.properties.iconName in iconsManifest === false) {
                feature.properties.iconName = 'waypoint';
            }
        }

        if (feature.properties?.iconSize) {
            // Check if icon size is an array 
            if (!Array.isArray(feature.properties.iconSize)) {
                feature.properties.iconSize = [32,32];
            }

            // Icon size need to be an array of length 2
            if (feature.properties.iconSize.length !== 2) {
                feature.properties.iconSize = [32,32];
            }

            // Check if we have numbers in the array
            if (!feature.properties.iconSize.every(value => value.constructor.name === 'Number')) {
                feature.properties.iconSize = [32,32];
            }
        }

        if (feature.properties?.popupText) {
            if (
                Array.isArray(feature.properties.popupText)
                && feature.properties.popupText.every(
                    value => value.constructor.name === 'String'
                )
            ) {
                feature.properties.popupText = feature.properties.popupText.map(escapeHTML);
            } else if (feature.properties.popupText.constructor.name === 'String') {
                feature.properties.popupText = escapeHTML(feature.properties.popupText);
            } else {
                throw new Error('popupText must be string or array of strings');
            }
        }
    }
    return jsonFormString;
};

// Load files
loadTreesGeoJson();
loadTemplesGeoJson();
loadRuinedGeoJson();
loadCavesGeoJson();
loadClaimsGeoJson();

// Load from gist / load from hash / load from file
loadGeoJsonFromGist();
loadGeoJsonFromHash();
loadGeoJsonFromFile('assets/markers/grids.geojson');