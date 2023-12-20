// map.js

// Create a Leaflet map centered on Austin
var map = L.map('map').setView([30.2500, -97.7500], 12);

// Add a tile layer (you can choose your preferred provider)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Define neighborhoods with polygon coordinates
var neighborhoods = [
    [[30.250, -97.770], [30.260, -97.770], [30.260, -97.750], [30.250, -97.750]],
    // Add more neighborhoods as needed
];

// Create neighborhood polygons and add them to the map
neighborhoods.forEach(coords => {
    L.polygon(coords, { color: 'blue', fillOpacity: 0.4 }).addTo(map);
});
