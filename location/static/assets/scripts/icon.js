document.querySelectorAll('.download-btn').forEach(button => {
    button.addEventListener('mouseenter', () => {
      // Example: Animate icon on hover
      button.querySelector('i').style.transform = 'scale(1.2)';
    });
  
    button.addEventListener('mouseleave', () => {
      button.querySelector('i').style.transform = 'scale(1)';
    });
  });
  