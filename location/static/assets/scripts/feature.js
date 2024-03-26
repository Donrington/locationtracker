document.addEventListener('DOMContentLoaded', (event) => {
    const featureItems = document.querySelectorAll('.feature-item');
  
    featureItems.forEach(item => {
      item.addEventListener('mouseover', () => {
        // JavaScript can add classes or styles when hovering over the item
        const readMoreBtn = item.querySelector('.feature-read-more');
        readMoreBtn.style.backgroundColor = '#dc143c'; // Crimson color for the button background
        readMoreBtn.style.color = '#fff'; // White text color
      });
  
      item.addEventListener('mouseout', () => {
        // Reset the styles after a delay to create a delayed hover-off effect
        const readMoreBtn = item.querySelector('.feature-read-more');
        setTimeout(() => {
          readMoreBtn.style.backgroundColor = '';
          readMoreBtn.style.color = '';
        }, 300); // Delay in milliseconds
      });
    });
  });



  