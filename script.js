document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('nav ul li a');
    document.querySelectorAll('main section');
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



const serverUrl = 'https://19de-82-183-30-112.ngrok-free.app';

// Fetch messages on load
fetchMessages();

document.addEventListener('DOMContentLoaded', function() {
    initializeChat();
    fetchMessages();
});

function initializeChat() {
    const form = document.getElementById('chat-form');
    const messagesDiv = document.getElementById('chat-messages');

    if (!form) {
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
            const messageElement = document.createElement('li');
            messageElement.innerHTML = `<strong>${timestamp}</strong> ${messageText}`;
            messagesDiv.prepend(messageElement);

            fetch(serverUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: messageText }),
            }).then(response => {
                if (!response.ok) {
                    console.error('Failed to post message');
                }
            }).catch(error => {
                console.error('Error:', error);
            });

            messageInput.value = '';
        }
    });
}

function fetchMessages() {
    fetch(serverUrl)
        .then(response => response.json())
        .then(messages => {
            const messagesDiv = document.getElementById('chat-messages');
            messagesDiv.innerHTML = '';
            messages.reverse().forEach(message => {
                const messageElement = document.createElement('li');
                messageElement.innerHTML = `<strong>${message.timestamp} ></strong> ${message.text}`;
                messagesDiv.appendChild(messageElement);
            });
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            initializeChat(); // Reinitialize chat after fetching messages
        })
        .catch(error => console.error('Error:', error));
}

function showSection(section) {
    fetch(`${section}.html`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('main-content').innerHTML = data;
            setTimeout(() => {
                initializeChat();
                fetchMessages();
            }, 100);
        })
        .catch(error => console.error('Error loading section:', error));
}
``

// Call fetchMessages when the page loads
window.onload = fetchMessages;







