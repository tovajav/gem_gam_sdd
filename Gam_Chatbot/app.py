from flask import Flask, request, jsonify
from groq import Groq
from config import gam_info  # Assurez-vous que cette config existe
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # Active CORS pour toutes les routes

# Configuration de l'API Groq
GROQ_API_KEY = "your_groq_api_key_here"  # Remplacez par votre clé Groq
client = Groq(api_key=GROQ_API_KEY)

def html_to_markdown(html):
    # Suppression des balises <ol> et <ul> pour forcer une liste à puces standard
    markdown = re.sub(r"<ol.*?>|<ul.*?>", "", html)  # Supprime toute balise <ol> et <ul>
    markdown = re.sub(r"</ol>|</ul>", "", markdown)  # Supprime les fermetures </ol> et </ul>

    # Convertir toutes les listes en tirets "-" (pas d'étoiles ni de chiffres !)
    markdown = re.sub(r"<li>\s*(?:\d+\.\s*|\*\s*)?", "- ", markdown)  
    markdown = re.sub(r"</li>\s*", "\n\n", markdown)  # Ajoute un double saut de ligne après chaque élément
    markdown = re.sub(r":\s*\n*-", ":\n\n-", markdown)  

    # Remplacement des autres balises HTML
    markdown = markdown.replace("<p>", "").replace("</p>", "\n\n")
    markdown = markdown.replace("<strong>", "**").replace("</strong>", "**")
    markdown = markdown.replace("<em>", "_").replace("</em>", "_")

    return markdown.strip()


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message vide"}), 400

    # Création du prompt système
    system_prompt = {
        "role": "system",
        "content": f"""
        Vous êtes Camille, assistante à Grenoble Alpes Métropole, spécialisée dans la gestion des déchets.
        Voici les règles à respecter :
        - Répondez uniquement aux questions liées à Grenoble Alpes Métropole.
        - Répondez sous la forme de texte brut (pas de HTML).
        - Si vous fournissez une liste, chaque élément doit commencer par "- ".
        - Répondez sur la base des informations suivantes :
        '''
        {gam_info}

        '''
        - Si une question ne concerne pas ce domaine, répondez "Je ne peux répondre qu'aux questions concernant la gestion des déchets à Grenoble."
        """
    }

    # Création du message
    messages = [system_prompt, {"role": "user", "content": user_message}]

    # Appel à Groq API
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            stream=False
        )
        bot_response = response.choices[0].message.content

        # Convertir la réponse en Markdown
        bot_response_markdown = html_to_markdown(bot_response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"response": bot_response_markdown})

if __name__ == "__main__":
    app.run(debug=True, port=5000)