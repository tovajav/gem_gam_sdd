// === 📌 Contenu de `data.txt` ajouté directement dans le code ===
const fileContent = `

Les bons déchets dans la bonne poubelle
Dans la poubelle verte "Je trie" : les emballages (pots de yaourts, flacons et bouteilles en plastique...) et les papiers, en vrac, sans sac.
Dans la poubelle marron (disponible selon les secteurs) ou votre composteur : les déchets alimentaires (restes de repas, épluchures, marc de café…). Consultez notre carte pour trouver les points de retrait de sac biodégradables et de bioseaux.
Dans la poubelle grise: les ordures ménagères, autrement dit tous les déchets qui ne se trient pas (attention : pas de verre donc, ni de produits toxiques !). Ex : mouchoirs, essuie-tout, mégots, chewing-gum, couches bébé, allumette, coton-tige, coquillages, litière, stylos...
Dans les colonnes à verre : le verre, sans bouchon ni couvercle.
En déchèterie : les déchets spéciaux et volumineux. 

Les erreurs à éviter dans la poubelle verte "Je trie" !
Je ne jette pas dans la poubelle verte "Je trie" :
- des sacs poubelle pleins et/ou fermés : s’ils contiennent des ordures ménagères ces sacs vont dans la poubelle grise et s’ils contiennent des emballages et papiers, ils doivent être vidés directement dans la poubelle verte ;
- des bouteilles et bocaux en verre (pour être recyclés et ne pas blesser les agents, ils vont dans les colonnes à verre) ;
- les objets en plastique (jouets, cintres...), ce ne sont pas des emballages, ils sont donc à donner s'ils sont en état ou à jeter en déchèterie ;
- des déchets sanitaires (masques, couches, litières...) ils vont dans la poubelle grise ;
- des déchets électriques et électroniques (électroménager, batteries, câbles, etc.) ils doivent être rapportés dans un magasin ou déposés en déchèterie ;
- du textile (vêtement, sac, chaussures, coussin...), cela va dans les bornes de collecte textile ;
- des déchets de travaux et de bricolage (gravats, roues, pots de peintures...), direction la déchèterie !

N'oubliez pas de donner une seconde vie à vos objets !
Si vos objets sont encore en état, ils peuvent servir à quelqu'un d'autre ! Donnez-les dans l'une des donneries proposées par Grenoble Alpes Métropole ou auprès des acteurs du réemploi et de la réparation.
Pour vos matériaux de bricolage, là aussi, ils peuvent rendre service au lieu d'être jetés ! Amenez-les dans l'un des "Préaux des matériaux" proposés dans certaines déchèteries métropolitaines.

Grenoble Alpes Métropole vous aide à bien trier
Découvrez nos pages pratiques sur les différents types de déchets et leur traitement.
Visitez le centre de tri pour tout comprendre du tri des déchets.
En copropriété, la Métropole vous accompagne gratuitement pour améliorer la gestion de vos déchets.

Vous êtes enseignant, syndic, membre d'une association... ? Demandez l'intervention d'un messager du tri pour vous aider à bien communiquer sur le tri :
- en appelant au 0 800 500 027,
- ou via notre formulaire de contact.

Les bons déchets dans la bonne poubelle
Dans la poubelle verte "Je trie" : les emballages (pots de yaourts, flacons et bouteilles en plastique...) et les papiers, en vrac, sans sac.
Dans la poubelle marron (disponible selon les secteurs) ou votre composteur : les déchets alimentaires (restes de repas, épluchures, marc de café…).
Dans la poubelle grise: les ordures ménagères, autrement dit tous les déchets qui ne se trient pas (attention : pas de verre donc, ni de produits toxiques !).
Les poubelles sont ramassées les jours fériés, hormis les 25 décembre, 1er janvier et 1er mai. Pour ces jours-ci, utilisez notre moteur de recherche pour connaître les collectes de remplacement.

Est-ce que mes poubelles sont ramassées les jours fériés ?
Les poubelles sont ramassées les jours fériés suivants : lundi de Pâques, 8 mai, jeudi de l'Ascension, lundi de Pentecôte, 14 juillet, 15 août, 1er novembre et 11 novembre.
Les poubelles  ne sont pas ramassées les 25 décembre, 1er janvier et 1er mai. 
`;

// Stockage des messages pour l'historique du chatbot
let chatHistory = [
    { role: "system", content: "Tu es un assistant de Grenoble Métropole. **Ta mission : répondre UNIQUEMENT en citant des phrases EXACTES du texte ci-dessous.**" },
    { role: "system", content: "📌 **Instructions** :\n- **Tu n'interprètes pas**\n- **Tu ne reformules pas**\n- **Tu cites uniquement le texte fourni**" },
    { role: "system", content: "**Texte de référence** :\n\n" + fileContent }
];

// ============================
// FONCTIONS DU CHATBOT
// ============================

// Fonction pour ouvrir/fermer le chatbot
function toggleChatbot() {
    let chatbotContainer = document.getElementById("chatbot-container");
    chatbotContainer.style.display = (chatbotContainer.style.display === "block") ? "none" : "block";
}

// Fonction pour afficher les messages
function displayChatbotMessage(message, sender) {
    let chatbotBox = document.getElementById("chatbot-box");
    let messageElement = document.createElement("div");
    messageElement.className = sender === "user" ? "user-message" : "bot-message";
    messageElement.textContent = message;
    chatbotBox.appendChild(messageElement);
    chatbotBox.scrollTop = chatbotBox.scrollHeight;
}

// Fonction pour envoyer un message avec vérification stricte
function sendChatbotMessage() {
    let inputField = document.getElementById("chatbot-userInput");
    let userMessage = inputField.value.trim();
    
    if (userMessage === "") return;

    displayChatbotMessage(userMessage, "user");
    inputField.value = "";

    // Ajouter le message utilisateur à l'historique
    chatHistory.push({ role: "user", content: userMessage });

     // Préparer la requête pour LM Studio
     const jsonData = {
        model: "unsloth/llama-3.2-1b-instruct:2",
        messages: chatHistory,
        temperature: 1,
        max_tokens: 3500
      };

    // Appel à l'API LM Studio
    fetch("http://127.0.0.1:1234/v1/chat/completions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(jsonData)
    })
    .then(res => res.json())
    .then(apiData => {
        console.log("Réponse API :", apiData);
        let botResponse = apiData.choices?.[0]?.message?.content || "Désolé, je n'ai pas de réponse.";

        // 🔍 Vérification : La réponse doit contenir une phrase exacte du fichier
        let foundValidSentence = false;
        let extractedSentence = "";

        fileContent.split("\n").forEach(line => {
            if (line.trim() !== "" && botResponse.includes(line.trim())) {
                foundValidSentence = true;
                extractedSentence = line.trim();
            }
        });

        if (!foundValidSentence) {
            botResponse = "⚠ Je n'ai pas trouvé d'information exacte à ce sujet dans les règles officielles.";
        } else {
            botResponse = extractedSentence; // Assurer que la réponse est bien une citation exacte
        }

        // Ajouter la réponse de l'IA dans l'historique
        chatHistory.push({ role: "assistant", content: botResponse });

        displayChatbotMessage(botResponse, "bot");
    })
    .catch(error => {
        console.error("Erreur API :", error);
        displayChatbotMessage("❌ L'API ne répond pas.", "bot");
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById("chatbot-userInput");
    console.log(userInput);
    if (userInput) {
        userInput.addEventListener("keydown", function(event) {
            if (event.key === "Enter" || event.keyCode === 13) {
                event.preventDefault();
                sendChatbotMessage();
            }
        });
    } else {
        console.error("Element with ID 'chatbot-userInput' not found.");
    }
});

