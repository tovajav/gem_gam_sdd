# Super Camille - Grenoble Alpes Metropole Assistant

A Streamlit-based chatbot interface that provides information about waste management services in Grenoble Alpes Metropole.

## Features

- Interactive chat interface with Groq LLM models
- Bilingual support (French/English)
- Specialized in waste management guidelines for Grenoble Alpes Metropole
- Streaming responses for better user experience
- Model selection from available Groq models
- Persistent chat history with clear history option

## Requirements

- Python 3.12+
- Streamlit
- Groq Python SDK

## Installation

### 1. Clone this repository
### 2. Install dependencies:
```sh
pip install streamlit groq
```
### 3. Set up Groq API Key:
Ensure you have an API key from Groq. This key should be stored securely using Streamlit's secrets management:
```sh
# .streamlit/secrets.toml
GROQ_API_KEY="your_groq_api_key_here"
```
### 4. Run the App: 
Navigate to the app's directory and run:
```sh
streamlit run app.py
