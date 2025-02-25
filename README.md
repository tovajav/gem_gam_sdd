# Camille - Grenoble Alpes Metropole Assistant

--- 
### Streamlit Version : [branch](https://github.com/tovajav/gem_gam_sdd?tab=readme-ov-file)
- [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gem-gam-sdd.streamlit.app/)
- A Streamlit-based chatbot interface that provides information about waste management services in Grenoble Alpes Metropole.

### Web Site Integration Version : [branch](https://github.com/tovajav/gem_gam_sdd/tree/Web_Integration)
- A local chatbot interface that provides information about waste management services in Grenoble Alpes Metropole.
---

### Streamlit Version :
<p align="center">
<img src="https://github.com/tovajav/gem_gam_sdd/blob/main/img/demo.gif" />
</p>

## Features

- Interactive chat interface with Groq LLM models
- Model selection from available Groq models
- Persistent chat history with clear history option
- Bilingual support (French/English)
- Specialized in waste management guidelines for Grenoble Alpes Metropole
- Agent functionality provides real-time bin locations and directions
- Enhanced with computer vision capability

## Requirements

- Python 3.12+
- Streamlit
- Groq Python SDK

## Installation

### 1. Clone this repository
### 2. Install dependencies:
```sh
pip install streamlit groq geopy
```
### 3. Set up Groq API Key:
Ensure you have an API key from Groq. This key should be stored securely using Streamlit's secrets management:
https://docs.streamlit.io/develop/concepts/connections/secrets-management
```sh
# .streamlit/secrets.toml
GROQ_API_KEY="your_groq_api_key_here"
```
### 4. Run the App: 
Navigate to the app's directory and run:
```sh
streamlit run app.py
