# frontpage
import streamlit as st

def set_bg_color(hex_color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {hex_color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Setting the background color to light blue
set_bg_color('#654321')

# Setting the background color to light blue
set_bg_color('brown')



from main import Botareaa
from streamlit_chat import message
import os
from general_bot import ChatBot
from custom_bot import CustomizedBot

class BotManager:
    def __init__(self):
        if 'bots' not in st.session_state:
            st.session_state['bots'] = {}

    def save_bot(self, name, details):
        st.session_state['bots'][name] = details

    def delete_bot(self, name):
        if name in st.session_state['bots']:
            del st.session_state['bots'][name]
    
    def display_bots(self):
        for name, details in list(st.session_state['bots'].items()):
            if st.sidebar.button(f"Click to start the {name} bot", key=f"start_{name}"):
                st.session_state['selected_bot_details'] = details
            if st.sidebar.button(f"Delete {name}", key=f"delete_{name}"):
                self.delete_bot(name)

botmanager = BotManager()


def st_centered_text(text: str):
        st.markdown(f"<h1 style='text-align: center; color: yellow;'><big><b>{text} </b></big></h1>", unsafe_allow_html=True)

def st_bigtext(text: str):
        st.markdown(f"<h1 style='text-align: left; color: grey;'<b>{text}</b></h1>", unsafe_allow_html=True)

with st.sidebar:
    st_centered_text('Bot Management')
    st_bigtext("Create your own Chatbot:")
    if st.button("Create New Bot"):
        st.session_state['show_create_bot_form'] = True

    if st.session_state.get('show_create_bot_form', False):
        bot_type = st.radio("Choose the bot :", ('General Bot', 'Custom Bot'))
        if bot_type == 'General Bot':
            with st.form(key='new_bot_form', clear_on_submit=True):
                name = st.text_input("Name:")
                model = st.selectbox("Model",["gpt-4", "gpt-3.5"])
                context_prompt = st.text_area("Prompt:")
                temperature = st.slider("Temperature Control- bot responses:", 0.0, 1.0, 0.5)
                submit_button = st.form_submit_button("Create Bot")
                if submit_button:
                    bot_details = {
                        'name':name,
                        'type':bot_type,
                        'model':model,
                        'prompt':context_prompt,
                        'temperature':temperature
                    }
                    botmanager.save_bot(name, bot_details)

        if bot_type == 'Custom Bot':
            with st.form("bot_creation_form", clear_on_submit=True):

                name = st.text_input("Name :")
                context_prompt = st.text_area("Prompt:")
                documents = st.file_uploader("Upload your document here:", accept_multiple_files=True)
                create_button = st.form_submit_button("Create Bot")
                if create_button:
                    if not name:
                        st.warning("recheck all the required fields.")
                    else:
                        if documents:
                            DATA_DIR = os.path.join('files', name)
                            if not os.path.exists(DATA_DIR):
                                os.makedirs(DATA_DIR)
                            for document in documents:
                                file_path = os.path.join(DATA_DIR, document.name)
                                with open(file_path, "wb") as f:
                                    f.write(document.getbuffer())
                            input_dir = DATA_DIR
                            bot_details = {'name': name, 'type': bot_type,'prompt':context_prompt, 'input_dir': input_dir}
                            botmanager.save_bot(name, bot_details)
                    st.session_state['show_create_bot_form'] = False
    botmanager.display_bots()

if 'selected_bot_details' in st.session_state:
    selected_bot_details = st.session_state['selected_bot_details']
    if selected_bot_details['type'] == 'General Bot':
        chat_bot = ChatBot(selected_bot_details['name'], selected_bot_details['model'], 
                        selected_bot_details['prompt'], selected_bot_details['temperature'])
    elif selected_bot_details['type'] == 'Custom Bot':
        # Assuming Customized Bot has different parameters or initialization
        chat_bot = CustomizedBot(selected_bot_details['name'],selected_bot_details['prompt'], selected_bot_details['input_dir'])
    chat_bot.run()