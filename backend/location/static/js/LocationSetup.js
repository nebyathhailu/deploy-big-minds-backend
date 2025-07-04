import React from 'react';

function LocationButton() {
  const getLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(position => {
        fetch('/api/locations/', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            name: "Customer Name",
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            is_mama_mboga: false // or true, if Mama Mboga
          })
        })
        .then(response => response.json())
        .then(data => {
          alert("Location saved: " + JSON.stringify(data, null, 2));
        });
      }, error => {
        alert("Location permission denied or unavailable.");
      });
    } else {
      alert("Geolocation is not supported by this browser.");
    }
  };

  return <button onClick={getLocation}>Allow Location</button>;
}

export default LocationButton;