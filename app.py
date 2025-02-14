import json
import pandas as pd
import streamlit as st
from groq import Groq
from config import MAIN_PROMPT, BIN_TOOL, VISION_PROMPT, VISION_USER
from utils import INSTRUCT_MODELS, get_points_collecte_from_url, get_decheteries_from_url, sys_prompt, get_bin_location, gen_gmaps_url, encode_image

# Title of the app and config layout
st.set_page_config(page_icon="💬", layout="wide", page_title="Grenoble Alpes Métropole - Super Camille")
st.logo('https://www.grenoblealpesmetropole.fr/images/GBI_LAMETRO/logo.svg', size='large')
col_left, col_right = st.columns([1,3])
col_left.subheader("Super Camille 🙋‍♀️")
chat_area = col_right.container(height=350)
tool_use = col_left.toggle('Bin locator super power', value=True)
col_right_l, col_right_r = col_right.columns([5,1])

# Initialize the Groq model
if "GROQ_API_KEY" not in st.session_state:
    st.session_state.GROQ_API_KEY = st.secrets['GROQ_API_KEY']
if st.session_state.GROQ_API_KEY is None:
    raise ValueError("GROQ_API_KEY environment variable is not set")
client = Groq(api_key = st.secrets['GROQ_API_KEY'])

# Initialize streamlit session state variables
if "GROQ_MODELS" not in st.session_state:
    st.session_state.GROQ_MODELS = {model.id : {'name': model.id.replace("-", " ").title(), 'tokens': model.context_window} for model in client.models.list().data if model.id in INSTRUCT_MODELS}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "filtered_messages" not in st.session_state:
    st.session_state.filtered_messages = []
if "selected_model" not in st.session_state:
    st.session_state.selected_model = None
if "DF" not in st.session_state:
    # with st.spinner("Retrieving waste collection points...", show_time=True):
    #     df = get_points_collecte_from_url()
    # with st.spinner("Retrieving waste disposal points...", show_time=True):
    #     df2 = get_decheteries_from_url()
    # df = pd.concat([df, df2], ignore_index = True).reset_index(drop = True)
    df = pd.read_csv('gam_data.csv')
    st.session_state.DF = df

def messages_append(prompt):
    st.session_state.messages.append(prompt)
    st.session_state.filtered_messages.append(prompt)

def messages_clear():
    st.session_state.messages = []
    st.session_state.filtered_messages = []

def get_main_completion(messages, model='llama-3.3-70b-versatile', tools=None):
    reasoning = 'hidden' if model in ['deepseek-r1-distill-qwen-32b','deepseek-r1-distill-llama-70b'] else None
    response = client.chat.completions.create(
        model=model, 
        messages=messages, 
        stream=False, 
        reasoning_format=reasoning,
        tool_choice='auto',
        tools=tools
    )
    # Extract the response and any tool call responses
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        func = eval(tool_calls[0].function.name)
        args = json.loads(tool_calls[0].function.arguments)
        args['df'] = st.session_state.DF
        # Call function 'get_bin_location' that returns message prompt and location dict
        message, location = func(**args)
        response = client.chat.completions.create(model=model, messages=message, stream=False, reasoning_format=reasoning)
        completion = response.choices[0].message.content
    else:
        completion, location = response_message.content, None
    return (completion, location)

# Retrieve available models from Groq API
model_option = col_left.selectbox(
    "Choose a model:", 
    options=list(st.session_state.GROQ_MODELS.keys()), 
    format_func=lambda x: st.session_state.GROQ_MODELS[x]['name'], 
    index=4
)

# Detect model change and clear chat history if model has changed
if st.session_state.selected_model != model_option:
    st.session_state.selected_model = model_option
    messages_clear()

# Manually clear chat history
col_left.button('Clear chat history', on_click=messages_clear)

# Display welcome message and chat history on app rerun
with chat_area.chat_message('assistant', avatar="🤖"):
    st.markdown('Bonjour! 👋 Bonjour, je suis Camille, assistante à Grenoble Alpes Metropole, spécialisée dans la gestion des déchets. (*I speak English too*)')
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👨‍💻"
    with chat_area.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

######## VISION TEST
@st.dialog("Take a photo")
def vision_response():
    st.write('Use your camera')
    picture = st.camera_input("Take a picture")
    if st.button("Upload") and picture is not None:
        base64_image = encode_image(picture.getvalue())
        vision_completion = client.chat.completions.create(messages=VISION_PROMPT(base64_image), model="llama-3.2-11b-vision-preview")
        st.session_state.vision_response = vision_completion.choices[0].message.content
        vision_messages = [sys_prompt(MAIN_PROMPT)]
        vision_messages.append({"role": "user", "content": st.session_state.vision_response})
        vision_completion = get_main_completion(vision_messages, model_option)
        with chat_area.chat_message('assistant', avatar="🤖"):
            st.markdown(vision_completion[0])
        # Append user message to filtered messages only and system message to both
        st.session_state.filtered_messages.append({"role": "user", "content": st.session_state.vision_response})
        messages_append({"role": "assistant", "content": vision_completion[0]})
        st.rerun()

if "vision_response" not in st.session_state:
    if col_right_r.button("Take photo", use_container_width=True):
        vision_response()
else:
    if col_right_r.button("Remove photo", use_container_width=True):
        del st.session_state["vision_response"]
        st.rerun()


######## START OF CONVERSATION
if prompt := col_right_l.chat_input("Enter your message here..."):

    messages_append({"role": "user", "content": prompt})
    with chat_area.chat_message("user", avatar="👨‍💻"):
        st.markdown(prompt)

    # Set system prompt
    messages = [sys_prompt(MAIN_PROMPT)]
    
    # Use filtered_messages to avoid repetitive function calling
    messages.extend({"role": m["role"], "content": m["content"]} for m in st.session_state.filtered_messages)

    # Fetch response from Groq API
    try:
        chat_completion, location = get_main_completion(messages, model_option, [BIN_TOOL] if tool_use else None)
        with chat_area.chat_message("assistant", avatar="🤖"):
            st.markdown(chat_completion)
        
        # Append the full response to session_state.messages
        messages_append({"role": "assistant", "content": chat_completion})

        if location:
            location_user = location['user']
            location_bin = location['geo_point_2d']
            location_url = gen_gmaps_url(location_user, location_bin)
            with chat_area.chat_message('assistant', avatar="🤖"):
                st.link_button('Directions', location_url)
            st.session_state.filtered_messages.pop() # Remove function output message
            st.session_state.filtered_messages.pop() # Remove function triggering user message
    except Exception as e:
        st.error(e, icon="🚨")

# col_left.write(len(st.session_state.messages))
# col_left.write(len(st.session_state.filtered_messages))