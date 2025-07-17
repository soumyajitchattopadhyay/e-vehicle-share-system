let map;
let marker;
let simulationInterval;
let distanceTravelled = 0;
let pricePerKm = 0.5; 
let startTime = new Date();

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
        alert("Failed to get your location. Using a default location.");
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
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  marker = L.marker([location.lat, location.lng]).addTo(map)
    .bindPopup("Starting Point")
    .openPopup();

  startMovementSimulation(location);
}

function startMovementSimulation(startLocation) {
  let currentLocation = startLocation;

  simulationInterval = setInterval(() => {
   
    const nextLocation = getNearbyPoint(currentLocation);


    marker.setLatLng([nextLocation.lat, nextLocation.lng]);
    map.panTo([nextLocation.lat, nextLocation.lng]);


    const segmentDistance = calculateDistance(currentLocation, nextLocation);
    distanceTravelled += segmentDistance;


    document.getElementById("distance").innerText = distanceTravelled.toFixed(2) + " km";
    document.getElementById("price").innerText = "$" + (distanceTravelled * pricePerKm).toFixed(2);
    const elapsedTime = Math.floor((new Date() - startTime) / 60000);
    document.getElementById("time").innerText = elapsedTime + " min";


    currentLocation = nextLocation;
  }, 3000); 
}


function getNearbyPoint(current) {
  const offsetLat = (Math.random() - 0.5) * 0.001; 
  const offsetLng = (Math.random() - 0.5) * 0.001;
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


function leaveVehicle() {
  clearInterval(simulationInterval); 

  // Display final receipt
  document.getElementById("receiptDistance").innerText = distanceTravelled.toFixed(2) + " km";
  document.getElementById("receiptPrice").innerText = "$" + (distanceTravelled * pricePerKm).toFixed(2);
  document.getElementById("receiptTime").innerText = Math.floor((new Date() - startTime) / 60000) + " min";
  document.getElementById("receipt").style.display = "block";


  setTimeout(() => {
    window.location.href = "/vehiclerent"; 
  }, 3000);
}


document.getElementById("leaveVehicle").addEventListener("click", leaveVehicle);


initMap();

function leaveVehicle() {
  clearInterval(simulationInterval);

  const distance = distanceTravelled.toFixed(2);
  const price = (distanceTravelled * pricePerKm).toFixed(2);
  const time = Math.floor((new Date() - startTime) / 60000);

  
  document.getElementById("receiptDistance").innerText = `${distance} km`;
  document.getElementById("receiptPrice").innerText = `$${price}`;
  document.getElementById("receiptTime").innerText = `${time} min`;
  document.getElementById("receipt").style.display = "block";


  const currentBalance = parseFloat(localStorage.getItem("userBalance")) || 50; 
  const newBalance = (currentBalance - parseFloat(price)).toFixed(2);
  localStorage.setItem("userBalance", newBalance); 

  setTimeout(() => {
    window.location.href = "/vehiclerent/";
  }, 3000); 
}


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
