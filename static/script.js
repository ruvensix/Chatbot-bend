document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const personaSelect = document.getElementById('persona-select');
    const loadingIndicator = document.getElementById('loading-indicator');

    const BACKEND_URL = "https://chatbot-backend-3xcv.onrender.com";

    function appendMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(`${sender}-message`);
        messageDiv.textContent = message;
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to bottom
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        const persona = personaSelect.value;

        if (message === "") return;

        appendMessage('user', message);
        userInput.value = ''; // Clear input
        sendButton.disabled = true; // Disable button
        loadingIndicator.style.display = 'block'; // Show loading

        try {
            const response = await fetch(`${BACKEND_URL}/chat`, { // Chamada para o endpoint do Flask
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message, persona: persona })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Erro do servidor: ${errorData.error || response.statusText}`);
            }

            const data = await response.json();
            appendMessage('bot', data.response); // Display bot's response
        } catch (error) {
            console.error('Erro ao enviar mensagem:', error);
            appendMessage('bot', `Erro: Não foi possível obter uma resposta. (${error.message})`);
        } finally {
            sendButton.disabled = false; // Re-enable button
            loadingIndicator.style.display = 'none'; // Hide loading
            userInput.focus(); // Focus back on input
        }
    }

    sendButton.addEventListener('click', sendMessage);

    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) { // Shift + Enter para nova linha
            event.preventDefault(); // Prevenir nova linha padrão do Enter
            sendMessage();
        }
    });

    // Limpar o histórico do chat quando a persona muda
    personaSelect.addEventListener('change', () => {
        chatWindow.innerHTML = '<div class="message bot-message">Olá! Como posso ajudar hoje?</div>';
        userInput.focus();
    });
});