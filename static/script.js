document.getElementById('send-button').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;
    if (userInput) {
        const chatOutput = document.getElementById('chat-output');
        
        // Display user question
        const userMessage = document.createElement('div');
        userMessage.textContent = 'User: ' + userInput;
        chatOutput.appendChild(userMessage);

        // Clear input field
        document.getElementById('user-input').value = '';

        // Send the question to the backend
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: userInput })
        })
        .then(response => response.json())
        .then(data => {
            // Display the assistant's response
            const assistantMessage = document.createElement('div');
            assistantMessage.textContent = 'Assistant: ' + data.response;
            chatOutput.appendChild(assistantMessage);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
