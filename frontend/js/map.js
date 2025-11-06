      // Create map and set initial position (latitude, longitude, zoom)
      const map = L.map('open-street-map').setView([33.6405, -117.8443], 13); // UCI coords

      // Add OpenStreetMap tiles
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
      }).addTo(map);

      // Add a marker
      L.marker([33.6405, -117.8443])
        .addTo(map)
        .bindPopup('University of California, Irvine 🐜')
        .openPopup();