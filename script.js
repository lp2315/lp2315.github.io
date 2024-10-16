document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('nav ul li a');
    const sections = document.querySelectorAll('main section');

    links.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            sections.forEach(section => {
                section.style.display = section.id === targetId ? 'block' : 'none';
            });
        });
    });

    // Show the home section by default
    sections.forEach(section => {
        section.style.display = section.id === 'home' ? 'block' : 'none';
    });
});

// retrieves section value for section key,
// changes the attribute of document to section
function showSection(section) {
    const sectionData = document.querySelector(`#sections-data [data-section="${section}"]`).innerHTML;
    document.getElementById('main-content').innerHTML = sectionData;
}
