document.getElementById('userProfileForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Example of handling form data
    const formData = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        // Handle the profile picture file upload separately
    };

    console.log('Form Data:', formData);
    // Here, you would typically send the formData to the server via AJAX

    alert('Profile updated successfully!');
    // Additional feedback or actions upon successful update
});
