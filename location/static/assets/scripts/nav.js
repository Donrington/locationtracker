window.addEventListener('scroll', function() {
    const header = document.querySelector('.navbar');
    const scrollDistance = window.scrollY;
  
    if (scrollDistance > 0) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });
  

// // Function to add 'scrolled' class to navbar when scrolled
// function checkScroll() {
//   var startY = $('.navbar').height() * 2; // The point where the navbar changes in px

//   if($(window).scrollTop() > startY){
//       $('.navbar').addClass("scrolled");
//   }else{
//       $('.navbar').removeClass("scrolled");
//   }
// }

// // On Document Ready
// $(document).ready(function(){
//   // When the user scrolls the page, execute checkScroll 
//   $(window).on("scroll", checkScroll);
// });
