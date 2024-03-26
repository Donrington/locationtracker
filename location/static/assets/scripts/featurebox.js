document.addEventListener('DOMContentLoaded', function() {
  // Select all feature boxes
  const featureBoxes = document.querySelectorAll('.feature-box');

  featureBoxes.forEach(box => {
    box.addEventListener('mouseenter', function() {
      // Find the icon and content containers of this feature box
      const icon = box.querySelector('.icon-container');
      const content = box.querySelector('.content-container');
      
      // Adjust styles for hover effect
      icon.style.top = '0%'; // Move the icon to the top
      content.style.transform = 'translate(-50%, -50%) scale(1)'; // Center and scale the content
      content.style.opacity = '1'; // Make content fully opaque
    });

    box.addEventListener('mouseleave', function() {
      // Reset styles when not hovering
      const icon = box.querySelector('.icon-container');
      const content = box.querySelector('.content-container');
      
      icon.style.top = '10%'; // Return icon to its initial position
      content.style.transform = 'translate(-50%, -50%) scale(0)'; // Hide content
      content.style.opacity = '0'; // Make content fully transparent
    });
  });
});


