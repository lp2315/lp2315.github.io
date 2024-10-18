document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('nav ul li a');
    const sections = document.querySelectorAll('main section');

    // Function to show the desired section
    function showSection(section) {
        fetch(`${section}.html`)
            .then(response => response.text())
            .then(data => {
                document.getElementById('main-content').innerHTML = data;
            })
            .catch(error => console.error('Error loading section:', error));
    }

    // Check the current hash and set the section
    const currentHash = window.location.hash.substring(1);
    if (currentHash) {
        showSection(currentHash);
    } else {
        showSection('home'); // Default start section
    }

    // Navigation click handling
    links.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            window.location.hash = targetId;
            showSection(targetId);
        });
    });

    // Hash change handling
    window.addEventListener('hashchange', function() {
        const targetId = window.location.hash.substring(1);
        showSection(targetId);
    });
});
