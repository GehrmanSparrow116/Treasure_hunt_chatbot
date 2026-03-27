const BASE_URL = "http://127.0.0.1:8000";
let currentUserId = null;

// Remove window.onload = initUser; we don't auto-login anymore.

async function register() {
    const user = document.getElementById('username').value.trim();
    const pass = document.getElementById('password').value.trim();
    const msgBox = document.getElementById('auth-message');

    if (!user || !pass) {
        msgBox.innerText = "Username and password required.";
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/register?username=${user}&password=${pass}`, { method: 'POST' });
        const data = await response.json();
        
        if (data.id) {
            msgBox.innerText = "Registration successful! You may now login.";
            msgBox.style.color = "#00F0FF";
        } else {
            msgBox.innerText = "Username may already be taken.";
            msgBox.style.color = "#ef4444"; // Red error
        }
    } catch (e) {
        msgBox.innerText = "Backend offline.";
    }
}

async function login() {
    const user = document.getElementById('username').value.trim();
    const pass = document.getElementById('password').value.trim();
    const msgBox = document.getElementById('auth-message');

    if (!user || !pass) return;

    try {
        const response = await fetch(`${BASE_URL}/login?username=${user}&password=${pass}`, { method: 'POST' });
        const data = await response.json();
        
        if (data.user_id) {
            currentUserId = data.user_id;
            
            // Hide Auth screen, Show Game screen
            document.getElementById('auth-screen').style.display = "none";
            document.getElementById('game-screen').style.display = "flex";

            // FETCH THE SCENARIO AND START THE GAME!
            const startResponse = await fetch(`${BASE_URL}/start`);
            const startData = await startResponse.json();
            
            // Clear the chat box and print the scenario
            document.getElementById('chat-box').innerHTML = ""; 
            addMessageToChat(startData.scenario, "bot");

        } else {
            msgBox.innerText = "Invalid credentials.";
            msgBox.style.color = "#ef4444";
        }
    } catch (e) {
        msgBox.innerText = "Backend offline.";
    }
}
async function sendMessage() {
    const inputField = document.getElementById('user-input');
    const message = inputField.value.trim();
    if (!message) return;

    addMessageToChat(message, "user");
    inputField.value = ""; 
    await sendToBackend(message);
}

async function getHint() {
    if (!currentUserId) return;
    addMessageToChat("Requesting a hint...", "user");
    
    try {
        const response = await fetch(`${BASE_URL}/hint?user_id=${currentUserId}`, {
            method: 'POST',
            headers: { 'Accept': 'application/json' }
        });
        const data = await response.json();
        
        if (data.points !== undefined) {
            document.getElementById('points-value').innerText = data.points;
        }
        addMessageToChat(data.reply, "bot");
    } catch (error) {
        addMessageToChat("Guardian offline. Check backend connection.", "bot");
    }
}

async function sendToBackend(messageText) {
    if (!currentUserId) return;

    try {
        const response = await fetch(`${BASE_URL}/chat?user_id=${currentUserId}&message=${encodeURIComponent(messageText)}`, {
            method: 'POST',
            headers: { 'Accept': 'application/json' }
        });
        
        const data = await response.json();

        if (data.points !== undefined) {
            document.getElementById('points-value').innerText = data.points;
        }

        // CORRECTLY PLACED STATUS CHECK
        if (data.status === "correct" || data.status === "game_over" || data.status === "level_up" || data.status === "win") {
            addMessageToChat(data.message, "bot");
            if (data.status === "level_up") {
                addMessageToChat(`Next riddle: ${data.next_riddle}`, "bot");
            }
            if (data.status === "win") {
                document.getElementById('user-input').disabled = true;
            }
        } else if (data.status === "hint" || data.status === "wrong" || data.status === "chat") {
            addMessageToChat(data.reply, "bot");
        }

    } catch (error) {
        addMessageToChat("Guardian offline. Check backend connection.", "bot");
    }
}

function addMessageToChat(text, sender) {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.innerText = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight; 
}

document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});