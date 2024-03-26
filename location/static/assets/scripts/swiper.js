var swiper = new Swiper(".mySwiper", {
    slidesPerView: 1,
    spaceBetween: 30,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    autoplay: {
      delay: 2500, // Delay in milliseconds before auto-switching to the next slide
      disableOnInteraction: false, // Continues autoplay after user interactions (swipe, click, etc.)
    },
  });


  var swiper = new Swiper('.swiper-container', {
    slidesPerView: 'auto',
    spaceBetween: 0, // No space between slides
    loop: false, // Removed loop to avoid warning if not enough slides
    speed: 2000, // Adjust speed for a slower or faster scrolling
    autoplay: {
      delay: 2500,
      disableOnInteraction: false,
    },
    freeMode: true, // Enables the continuous scroll
    freeModeMomentum: true,
  });