function initializeMap() {
  const NE = L.latLng(33.651154, -117.834919);
  const SW = L.latLng(33.641249, -117.850411);
  const bounds = L.latLngBounds(SW, NE);
  const map = L.map('map', {
    center: [33.645805, -117.842772],
    zoom: 18,
    minZoom: 18,
    maxZoom: 18,
    zoomControl: false,
    scrollWheelZoom: false,
    doubleClickZoom: false,
    boxZoom: false,
    maxBounds: bounds,
    maxBoundsViscosity: 1.0
  });

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  return map;
}

async function fetchAllEvents() {
  console.log('starting event log...');
  const res = await fetch('http://localhost:8000/events');
  const events = await res.json();
  console.log(events);
  return events;
}

async function fetchEventById(id) {
  const res = await fetch(`http://localhost:8000/events/${id}`);
  const event = await res.json();
  console.log(event);
  return event;
}

function showEventInfo(event) {
  const overlay = document.querySelector('#overlay');
  const eventInfo = document.querySelector('#event-info');
  overlay.classList.add('active');
  eventInfo.classList.add('active');
  eventInfo.innerHTML = `
  <button id="close-info">✖</button>
  <h2>${event.name}</h2>
  <p><b>Host:</b> ${event.host}</p>
  <p><b>Time:</b> ${event.time}</p>
  `;
  document.querySelector('#close-info').addEventListener('click', hideEventInfo);
}

function hideEventInfo() {
  const overlay = document.querySelector('#overlay');
  const eventInfo = document.querySelector('#event-info');
  overlay.classList.remove('active');
  eventInfo.classList.remove('active');
}

function showEventSubmit(coords) {
  const overlay = document.querySelector('#overlay');
  const eventForm = document.querySelector('#event-form-container');
  overlay.classList.add('active');
  eventForm.classList.add('active');
  document.querySelector('#event-location').value = JSON.stringify(coords);
}

function hideEventSubmit() {
  const overlay = document.querySelector('#overlay');
  const eventForm = document.querySelector('#event-form-container');
  overlay.classList.remove('active');
  eventForm.classList.remove('active');
}

document.addEventListener('DOMContentLoaded', async function() {
  // initialize map
  const map = initializeMap();
  const allEvents = await fetchAllEvents();

  // parse events into objects
  allEvents.forEach(event => {
    let marker = L.marker(JSON.parse(event.location));
    marker.on('click', (e) => {
      showEventInfo(event);
    });
    marker.addTo(map);
    console.log(`Event ${event.id} loaded!`);
  });

  let marker = null;
  
  map.on('dblclick', (e) => {
    console.log('event creation started...');
    marker = L.marker(e.latlng).addTo(map);
    showEventSubmit(e.latlng);
  });

  document.querySelector('#event-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    const res = await fetch('http://localhost:8000/events', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    const event = await res.json();
    if (marker) {
      marker.on('click', (e) => {
        showEventInfo(event);
      });
    }
    hideEventSubmit();
    console.log(`Event ${event.id} created!`);
  });

  document.querySelector('#event-form-cancel').addEventListener('click', (e) => {
    e.preventDefault();
    if (marker) {
      map.removeLayer(marker);
      marker = null;
    }
    hideEventSubmit();
    console.log('event creation cancelled');
  });
});