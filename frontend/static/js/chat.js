const BASE_URL = window.location.origin;
const API_URL = BASE_URL + '/api/chat';
let usuarioId = 'user_' + Math.random().toString(36).substr(2, 9);

function agregarMensaje(texto, tipo, mostrarFeedback, consultaId) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${tipo}-message`;
    
    const time = new Date().toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' });
    
    let feedbackHTML = '';
    if (mostrarFeedback && consultaId) {
        feedbackHTML = `
            <div class="feedback-container" id="feedback-${consultaId}">
                <p style="font-size: 0.85em;">¿Te fue util?</p>
                <button class="btn-feedback btn-pos" onclick="enviarFeedback(${consultaId}, 5)">👍 Si</button>
                <button class="btn-feedback btn-neg" onclick="enviarFeedback(${consultaId}, 1)">👎 No</button>
            </div>
        `;
    }
    
    messageDiv.innerHTML = `
        <div class="message-content">${texto.replace(/\n/g, '<br>')}${feedbackHTML}</div>
        <span class="message-time">${time}</span>
    `;
    
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function enviarMensaje() {
    const input = document.getElementById('user-input');
    const mensaje = input.value.trim();
    if (!mensaje) return;
    
    agregarMensaje(mensaje, 'user');
    input.value = '';
    
    const typing = document.createElement('div');
    typing.className = 'message bot-message';
    typing.id = 'typing';
    typing.innerHTML = '<div class="message-content">Escribiendo...</div>';
    document.getElementById('chat-box').appendChild(typing);
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mensaje, usuario: usuarioId })
        });
        const data = await response.json();
        document.getElementById('typing')?.remove();
        agregarMensaje(data.respuesta, 'bot', true, data.consulta_id);
    } catch (error) {
        document.getElementById('typing')?.remove();
        agregarMensaje('Error de conexion. Verifica que el servidor este activo.', 'bot');
    }
}

async function enviarFeedback(consultaId, calificacion) {
    try {
        await fetch('http://localhost:5000/api/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ consulta_id: consultaId, calificacion })
        });
        const c = document.getElementById(`feedback-${consultaId}`);
        if (c) c.innerHTML = '<p style="color:green; font-size:0.85em;">Gracias!</p>';
    } catch (e) { console.error(e); }
}

function enviarPreguntaRapida(pregunta) {
    document.getElementById('user-input').value = pregunta;
    enviarMensaje();
}
