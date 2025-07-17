let map;
let marker;
let simulationInterval;
let routeCoordinates = [];
let routeIndex = 0;
let speed = 5000;

let distanceTravelled = 0;
let startTime = new Date();
let pricePerKm = 0.5;

function initMap() {
  requestLocation();
}

function requestLocation() {
  if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
          (position) => {
              const userLocation = {
                  lat: position.coords.latitude,
                  lng: position.coords.longitude,
              };
              initializeMap(userLocation);
          },
          (error) => {
              console.error("Error fetching location:", error.message);
              alert("Failed to get your location. Using default Glasgow location.");
              initializeMap({ lat: 55.8642, lng: -4.2518 });
          }
      );
  } else {
      alert("Geolocation is not supported by this browser.");
      initializeMap({ lat: 55.8642, lng: -4.2518 });
  }
}

function initializeMap(location) {
  map = L.map('map').setView([location.lat, location.lng], 15);
  
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  marker = L.marker([location.lat, location.lng]).addTo(map)
    .bindPopup("Starting Point")
    .openPopup();

  calculateRoute(location);
}

function calculateRoute(start) {
  const destination = getNearbyPoint(start);
  
  routeCoordinates = [
    { lat: start.lat, lng: start.lng },
    destination
  ];
  
  routeIndex = 0;
  startSimulation();
}

function startSimulation() {
  simulationInterval = setInterval(() => {
      if (routeIndex < routeCoordinates.length - 1) {
          const nextPosition = routeCoordinates[routeIndex];
          marker.setLatLng([nextPosition.lat, nextPosition.lng]);

          if (routeIndex > 0) {
              const lastPosition = routeCoordinates[routeIndex - 1];
              distanceTravelled += calculateDistance(lastPosition, nextPosition);
          }

          document.getElementById("distance").innerText = distanceTravelled.toFixed(2) + " km";
          document.getElementById("price").innerText = "$" + (distanceTravelled * pricePerKm).toFixed(2);
          const elapsedTime = Math.floor((new Date() - startTime) / 60000);
          document.getElementById("time").innerText = elapsedTime + " min";

          routeIndex++;
      } else {
          calculateRoute(routeCoordinates[routeCoordinates.length - 1]);
      }
  }, speed);
}

function getNearbyPoint(current) {
  const offsetLat = (Math.random() - 0.5) * 0.01;
  const offsetLng = (Math.random() - 0.5) * 0.01;
  return {
    lat: current.lat + offsetLat,
    lng: current.lng + offsetLng,
  };
}

function calculateDistance(pos1, pos2) {
  const R = 6371;
  const dLat = degreesToRadians(pos2.lat - pos1.lat);
  const dLng = degreesToRadians(pos2.lng - pos1.lng);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(degreesToRadians(pos1.lat)) *
    Math.cos(degreesToRadians(pos2.lat)) *
    Math.sin(dLng / 2) * Math.sin(dLng / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function degreesToRadians(degrees) {
  return degrees * (Math.PI / 180);
}
