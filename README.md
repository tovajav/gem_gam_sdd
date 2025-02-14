# Camille - Grenoble Alpes Metropole Assistant

--- 
### Streamlit Version : [branch](https://github.com/tovajav/gem_gam_sdd/edit/Web_Integration)
- [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gem-gam-sdd.streamlit.app/)
- A Streamlit-based chatbot interface that provides information about waste management services in Grenoble Alpes Metropole.

### Local Version - Web Site Integration : [branch](https://github.com/tovajav/gem_gam_sdd/tree/Web_Integration)
- A local chatbot interface that provides information about waste management services in Grenoble Alpes Metropole.

---

## Features

- Interactive chat interface with Groq LLM models
- Persistent chat history with clear history option
- Only in French
- Specialized in waste management guidelines for Grenoble Alpes Metropole

## Requirements

- Python 3.12+
- Flask and flask_cors
- Groq Python SDK

## Installation
### 0.  Tree Structure

```
Web-Integration Branch
├── Gam_Chatbot                                                           # Main chatbot application folder
│   ├── img                                                               # Directory for image assets
│   │   ├── pictures.png                                                  # Help icon for AI functionalities
│   ├── app.py                                                            # Main Python application file for the chatbot and th local server
│   ├── config.py                                                         # Configuration settings for the chatbot
│   ├── index.html                                                        # HTML file for the chatbot's web interface
│   ├── scriptCamilleAIBot.js                                             # JavaScript file for interactive elements in the web interface
│   └── scriptCamilleAIBot.css                                            # CSS file for styling the web interface
└── Grenoble Alpes Métropole - Isère - Grenoble Alpes Métropole_files     # Folder containing assets and resources for a webpage
    └── ...                                                               # Other files (a lot)
└── Grenoble Alpes Métropole - Isère - Grenoble Alpes Métropole.html      # Main HTML document for the webpage about Grenoble Alpes Métropole which include the index.html
```

To test the chatbot, only the Gam_Chabot folder is required

### 1. Clone this repository
### 2. Install dependencies:
```sh
pip install groq geopy flask flask_cors
```
### 3. Set up Groq API Key:
Ensure you have an API key from Groq.
```
GROQ_API_KEY="your_groq_api_key_here"
```
### 4. Run the App: 
Navigate to the app's directory and run:
```sh
python run app.py
