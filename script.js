document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('nav ul li a');
    const sections = document.querySelectorAll('main section');

    // Initial display setup
    sections.forEach(section => {
        section.style.display = 'none';
    });
    if (window.location.hash) {
        const initialTargetId = window.location.hash.substring(1);
        const initialTargetSection = document.getElementById(initialTargetId);
        if (initialTargetSection) {
            initialTargetSection.style.display = 'block';
        }
    } else {
        sections[0].style.display = 'block'; // Show the first section by default
    }

    // Navigation click handling
    links.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            window.location.hash = targetId;
            sections.forEach(section => {
                section.style.display = section.id === targetId ? 'block' : 'none';
            });
        });
    });

    // Hash change handling
    window.addEventListener('hashchange', function() {
        const targetId = window.location.hash.substring(1);
        sections.forEach(section => {
            section.style.display = section.id === targetId ? 'block' : 'none';
        });
    });
});

// retrieves section value for section key,
// changes the attribute of document to section
function showSection(section) {
    fetch(`${section}.html`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('main-content').innerHTML = data;
        })
        .catch(error => console.error('Error loading section:', error));
}
