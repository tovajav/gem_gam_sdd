import os
import streamlit as st
from groq import Groq
from typing import Generator
from config import gam_info

# Title of the app and config layout
st.set_page_config(page_icon="💬", layout="wide", page_title="Super Camille Goes Brrrrr...")
st.logo('https://www.grenoblealpesmetropole.fr/images/GBI_LAMETRO/logo.svg', size='large')
col_left, col_right = st.columns([1,3])
col_left.subheader("Super Camille 🙋‍♀️")
chat_area = col_right.container(height=350)

# Groq API Key
if "GROQ_API_KEY" not in st.session_state:
    st.session_state.GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if st.session_state.GROQ_API_KEY is None:
    raise ValueError("GROQ_API_KEY environment variable is not set")

# Initialize the Groq model
client = Groq(api_key=st.session_state.GROQ_API_KEY)
if "GROQ_MODELS" not in st.session_state:
    st.session_state.GROQ_MODELS = {model.id : {'name': model.id.replace("-", " ").title(), 'tokens': model.context_window} for model in client.models.list().data if not (model.id.startswith("whisper") or model.id.startswith("llama-guard"))}

# Initialize chat history and selected model
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

model_option = col_left.selectbox("Choose a model:", options=list(st.session_state.GROQ_MODELS.keys()), format_func=lambda x: st.session_state.GROQ_MODELS[x]['name'], index=0)

# Set system prompt and a welcome message
system_prompt = {"role": "system", "content": f"""\
    You are Camille, a helpful assistant born in Grenoble, who works at Grenoble Alpes Metropole and is an expert in below waste management guidelines:
    '''
    {gam_info}
    '''
    Answer questions that the user asks only if it is related to Grenoble Alpes Metropole functions.\
    If the user asks questions related to waste management, answer only about the waste management guidelines and nothing else.\
    Avoid asking for followup details if you have answered with contact information.\
"""}

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# Detect model change and clear chat history if model has changed
if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

# Manually clear chat history
if col_left.button('Clear chat history'):
    st.session_state.messages = []

with chat_area.chat_message('assistant', avatar="🤖"):
    st.markdown('Bonjour! 👋 Bonjour, je suis Camille, assistante à Grenoble Alpes Metropole, spécialisée dans la gestion des déchets. (*I speak English too*)')

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👨‍💻"
    with chat_area.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := col_right.chat_input("Enter your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_area.chat_message("user", avatar="👨‍💻"):
        st.markdown(prompt)

    messages = [system_prompt]
    messages.extend({"role": m["role"], "content": m["content"]} for m in st.session_state.messages)

    # Fetch response from Groq API
    try:
        chat_completion = client.chat.completions.create(
            model=model_option,
            messages=messages,
            # max_tokens=max_tokens,
            stream=True,
            reasoning_format='hidden' if model_option in ['deepseek-r1-distill-qwen-32b','deepseek-r1-distill-llama-70b'] else None,
        )

        # Use the generator function with st.write_stream
        with chat_area.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)
    except Exception as e:
        st.error(e, icon="🚨")

    # Append the full response to session_state.messages
    if isinstance(full_response, str):
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
    else:
        # Handle the case where full_response is not a string
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": combined_response}
        )