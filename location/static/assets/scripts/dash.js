document.getElementById('theme-toggle').addEventListener('click', function() {
    document.body.classList.toggle('dark-theme');

    // Toggle icons for theme switch
    const themeIcon = this.querySelector('i');
    if (themeIcon.classList.contains('fa-moon')) {
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    } else {
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
    }

    // Update the row hover color for dark mode
    document.querySelectorAll('.location-history tr').forEach(row => {
        row.addEventListener('mouseover', function() {
            this.style.backgroundColor = document.body.classList.contains('dark-theme') ? '#444' : '#f5f5f5';
        });
        row.addEventListener('mouseout', function() {
            this.style.backgroundColor = '';
        });
    });
});
