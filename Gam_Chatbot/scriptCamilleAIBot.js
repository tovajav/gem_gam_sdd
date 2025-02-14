// Fonction d'affichage
function displayChatbotMessage(message, sender) {
  const chatbotBox = document.getElementById("chatbot-box");
  const messageElement = document.createElement("div");
  messageElement.className = sender === "user" ? "user-message" : "bot-message";
  // messageElement.innerHTML = message;  // Utiliser innerHTML pour interpréter les balises HTML
  messageElement.innerHTML = message
    .replace(/\n/g, "<br>")  // Conserve les sauts de ligne
    .replace(/- (.*?)(<br>|$)/g, "<ul><li>$1</li></ul>");  // Convertit les tirets "-" en une vraie liste HTML
  chatbotBox.appendChild(messageElement);
  chatbotBox.scrollTop = chatbotBox.scrollHeight;
}

// Fonction principale d'envoi
function sendChatbotMessage() {
  const inputField = document.getElementById("chatbot-userInput");
  const userMessage = inputField.value.trim();
  if (!userMessage) return;

  // Affichage du message utilisateur
  displayChatbotMessage(userMessage, "user");
  inputField.value = "";

  // Envoi du message à l'API Flask
  fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage })
  })
  .then(res => res.json())
  .then(data => {
      let botResponse = data.response || "Désolé, une erreur s'est produite.";
      displayChatbotMessage(botResponse, "bot");
  })
  .catch(error => {
      console.error("Erreur API :", error);
      displayChatbotMessage("❌ Erreur de connexion avec le serveur.", "bot");
  });
}

// Gestion de l'Enter
document.addEventListener('DOMContentLoaded', () => {
  const userInput = document.getElementById("chatbot-userInput");
  if (userInput) {
      userInput.addEventListener("keydown", (event) => {
          if (event.key === "Enter" || event.keyCode === 13) {
              event.preventDefault();
              sendChatbotMessage();
          }
      });
  }
});