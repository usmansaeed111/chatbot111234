document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const userMessage = userInput.value;
        if (userMessage.trim() !== '') {
            appendMessage(userMessage, 'message', 'static/user.svg', 'user-img', 'message-text');
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'user_input=' + encodeURIComponent(userMessage),
            })
            .then(response => response.json())
            .then(data => {
                appendMessage(data.response, 'message', 'static/logo.jpg', 'user-img', 'message-text');
            });
            userInput.value = '';
        }
    }

    function appendMessage(message, className, imageSrc, imageClass, paragraphClass) {
        const messageDiv = document.createElement('div');
        const imageTag = document.createElement('img');
        imageTag.src = imageSrc;
        imageTag.alt = "Chat Icon";
        imageTag.classList.add(imageClass);
        messageDiv.appendChild(imageTag);
        
        const messageParagraph = document.createElement('p');
        messageParagraph.innerText = message;
        messageParagraph.classList.add(paragraphClass);
        messageDiv.appendChild(messageParagraph);
        
        messageDiv.classList.add(className);
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
