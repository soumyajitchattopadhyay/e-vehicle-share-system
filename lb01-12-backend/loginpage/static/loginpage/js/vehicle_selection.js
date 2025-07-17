function fetchAvailableVehicles(vehicleType) {
    $.ajax({
      url: `/get-available-vehicles/${vehicleType}/`,
      method: 'GET',
      success: function(data) {
        const dropdownId = vehicleType === 'cycle' ? 'cycleDropdown' : 'scooterDropdown';
        const dropdown = document.getElementById(dropdownId);
        dropdown.innerHTML = '<option value="">Select an available ' + vehicleType + '</option>';
        
        if (data.length > 0) {
          data.forEach(vehicle => {
            const option = document.createElement('option');
            option.value = vehicle.id;
            option.textContent = vehicle.name;
            dropdown.appendChild(option);
          });
          dropdown.style.display = 'block';
        } else {
          alert('No ' + vehicleType + 's are currently available.');
        }
      },
      error: function(error) {
        console.log('Error:', error);
      }
    });
  }
 
  function redirectToLocationPage(dropdown) {
    const vehicleId = dropdown.value;
    if (vehicleId) {
      window.location.href = `/location/?vehicle_id=${vehicleId}`;
    }
  }
 