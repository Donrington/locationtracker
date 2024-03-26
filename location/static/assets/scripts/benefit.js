document.addEventListener('DOMContentLoaded', function () {
    animateValue('benefit1', 0, 25, 2000); // Example percentage for Benefit 1
    animateValue('benefit2', 0, 40, 2000); // Example percentage for Benefit 2
    animateValue('benefit3', 0, 20, 2000); // Example percentage for Benefit 3
    animateValue('benefit4', 0, 35, 2000); // Example percentage for Benefit 4
  });
  
  function animateValue(id, start, end, duration) {
    let range = end - start;
    let current = start;
    let increment = end > start ? 1 : -1;
    let stepTime = Math.abs(Math.floor(duration / range));
    let obj = document.getElementById(id);
    let timer = setInterval(function () {
      current += increment;
      obj.textContent = current + '%';
      if (current == end) {
        clearInterval(timer);
      }
    }, stepTime);
  }
  