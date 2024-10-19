document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('nav ul li a');
    const sections = document.querySelectorAll('main section');

    // Function to show the desired section (home/links/etc)
    function showSection(section) {
        fetch(`${section}.html`)
            .then(response => response.text())
            .then(data => {
                document.getElementById('main-content').innerHTML = data;
            })
            .catch(error => console.error('Error loading section:', error));
    }

    // Check the current hash # and set the section
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



// night mode
let toggle_night = false;

function nightMode(){
    if (toggle_night === false){
        document.getElementById("body").style.color="#faebd7";
        document.getElementById("body").style.background="#4b544b";
        toggle_night = true;
    } else {
        document.getElementById("body").style.color="black";
        document.getElementById("body").style.background="#c7c7bb";
        toggle_night = false;
    }
};



document.addEventListener('DOMContentLoaded', function() {
    initializeGuestBook();
});

function initializeGuestBook() {
    const form = document.getElementById('chat-form');
    const messagesDiv = document.getElementById('chat-messages');

    if (!form) {
        console.error('Form element not found');
        return;
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const messageInput = document.getElementById('message');
        const messageText = messageInput.value.trim();

        if (messageText) {
            const now = new Date();
            const time = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
            const timestamp = `${time} >`;
            const messageElement = document.createElement('div');
            messageElement.innerHTML = `<strong>${timestamp}</strong> ${messageText}`;
            messagesDiv.prepend(messageElement);

            // Clear the input
            messageInput.value = '';
        }
    });
}



// Reinitialize Guest Book when content is dynamically loaded
function showSection(section) {
    fetch(`${section}.html`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('main-content').innerHTML = data;
            setTimeout(initializeGuestBook, 100); // Delay to ensure content loads
        })
        .catch(error => console.error('Error loading section:', error));
}






