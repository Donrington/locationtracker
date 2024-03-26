document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('contactForm').addEventListener('submit', function(event) {
      event.preventDefault();
      
      // Validate each field
      var firstName = document.getElementById('firstName').value;
      var lastName = document.getElementById('lastName').value;
      var email = document.getElementById('email').value;
      var phone = document.getElementById('phone').value;
      var country = document.getElementById('country').value;
      var subject = document.getElementById('subject').value;
      
      if(firstName && lastName && validateEmail(email) && phone && country && subject) {
        // If all validations pass, submit the form
        this.submit();
      } else {
        // If validations fail, display an error message
        alert('Please fill in all required fields with valid information.');
      }
    });
  });
  
  // Helper function to validate email
  function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
  }
  