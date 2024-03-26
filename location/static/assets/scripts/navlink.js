document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
  
    // Function to change the active link
    function changeActiveLink() {
      let current = '';
  
      // Check which section is in viewport
      sections.forEach((section) => {
        const sectionTop = section.offsetTop - 50; // Offset by 50px or navbar height
        if (scrollY >= sectionTop && scrollY < sectionTop + section.offsetHeight) {
          current = section.getAttribute('id');
        }
      });
  
      // Remove active class from all nav links
      navLinks.forEach((navLink) => {
        navLink.classList.remove('active');
      });
  
      // Add active class to the current nav link
      navLinks.forEach((navLink) => {
        if (navLink.getAttribute('href') === `#${current}`) {
          navLink.classList.add('active');
        }
      });
    }
  
    // Event listener for scrolling
    window.addEventListener('scroll', changeActiveLink);
  });