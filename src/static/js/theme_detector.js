// Function to detect color scheme
function detectColorScheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  
  // Function to send color scheme to the backend
  function sendColorSchemeToBackend(isDarkMode) {
    // Create an HTTP request
    var xhr = new XMLHttpRequest();
    
    // Prepare the request
    xhr.open('POST', '/set-color-scheme', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
  
    // Prepare the data to be sent
    var data = JSON.stringify({ isDarkMode: isDarkMode });
  
    // Send the request
    xhr.send(data);
  }
  
  // Detect color scheme and send it to the backend
  var isDarkMode = detectColorScheme();
  sendColorSchemeToBackend(isDarkMode);
  