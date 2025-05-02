document.addEventListener('DOMContentLoaded', function() {
  // Get the current URL
  const currentUrl = window.location.href;
  console.log("Checking URL:", currentUrl);
  
  // Send request to your API
  fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ url: currentUrl })
  })
  .then(response => response.json())
  .then(data => {
    console.log("API response:", data);
    
    // Create notification element
    const notification = document.createElement('div');
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.padding = '15px 20px';
    notification.style.borderRadius = '8px';
    notification.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    notification.style.fontFamily = 'Arial, sans-serif';
    notification.style.fontSize = '14px';
    notification.style.fontWeight = 'bold';
    notification.style.transition = 'all 0.3s ease';
    
    // Set styles based on prediction
    if(data.prediction === 'phishing') {
      notification.style.backgroundColor = '#FF4D4F';
      notification.style.color = 'white';
      notification.textContent = '⚠️ Warning: This site may be dangerous!';
    } else {
      notification.style.backgroundColor = '#52C41A';
      notification.style.color = 'white';
      notification.textContent = '✅ This site appears to be safe';
    }
    
    // Add to body when ready
    if(document.body) {
      document.body.appendChild(notification);
    } else {
      window.addEventListener('load', function() {
        document.body.appendChild(notification);
      });
    }
    
    // Remove after delay
    setTimeout(() => {
      notification.style.opacity = '0';
      setTimeout(() => {
        if(notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 300);
    }, 5000);
  })
  .catch(error => {
    console.error("Error checking site:", error);
  });
});

// Also run on navigation changes for SPAs
let lastUrl = location.href; 
new MutationObserver(() => {
  const url = location.href;
  if (url !== lastUrl) {
    lastUrl = url;
    console.log('URL changed to', url);
    // Re-run the same check
    // ... [Copy the fetch code from above]
  }
}).observe(document, {subtree: true, childList: true});