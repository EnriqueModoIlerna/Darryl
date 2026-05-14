// Creación del mensaje inicial
window.onload = async function() {

    const res = await fetch("/welcome");
    const data = await res.json();

    addMessage("Darryl", data.message);
};

async function sendMessage() {

    const input = document.getElementById("user-input");
    const message = input.value;

    if (message.trim() === "") return;

    // Mostrar mensaje del usuario
    addMessage("Tú", message);

    // Limpiar barra
    input.value = "";

    // Enviar al backend
    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    });

    const data = await response.json();

    // Mostrar respuesta del bot
    addMessage("Darryl", data.response);
}

function addMessage(sender, text) {
    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `
        <p><b>${sender}:</b> ${text}</p>
    `;

    // Auto scroll hacia abajo
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Funcion para poder enviar al hacer Enter y si hacemos Ctrl+Enter hacer un salto de linea
const input = document.getElementById("user-input");

// ENTER para enviar
input.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

// AUTO-RESIZE tipo ChatGPT
input.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = this.scrollHeight + "px";
});
// document.addEventListener("DOMContentLoaded", function () {

//     const input = document.getElementById("user-input");

//     input.addEventListener("keydown", function (event) {
//         if (event.key === "Enter" && !event.shiftKey) {
//             event.preventDefault();
//             sendMessage();
//         }
//     });

// });