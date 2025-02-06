from aiohttp import client
import openai
import streamlit as st
import time
import arxiv
from dotenv import load_dotenv
import os
import re
from PIL import Image
#import cv2
# Charger le fichier .env contenant la clé API
#load_dotenv()
#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = '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'
bac2futur_id = "aasst_RR0sWP4WKBLnDY17pywAUFbLs"
client = openai

# Initialisation des variables de session
if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="Bac2Futur", page_icon=":book:", layout="wide")

# Fonction pour nettoyer la réponse de l'IA
def clean_response(response):
    return re.sub(r' [\d+:\d+source]', " ", response)

# Fonction pour rechercher sur ArXiv
def search_arxiv(query):
    search = arxiv.Search(
        query=query,
        max_results=3,
        sort_by=arxiv.SortCriterion.Relevance
    )
    results = []
    for result in search.results():
        summary = ' '.join(result.summary.split()[:100]) + '...'
        results.append({
            'title': result.title,
            'summary': summary,
            'authors': [author.name for author in result.authors],
            'url': result.entry_id
        })
    return results

# Fonction principale pour gérer la conversation
def conversation_chat(query):
    st.session_state.messages.append({"role": "user", "content": query})

    with st.spinner("L'assistant réfléchit..."):
        response = client.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages],
            temperature=0.7
        )
        assistant_reply = response["choices"][0]["message"]["content"]

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply

# Initialisation de l'état de session
def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! 🤗"]
    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]

# Affichage de l'historique du chat
def display_chat_history():
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='chat_form', clear_on_submit=True):
            user_input = st.text_input("Question :", placeholder="Tapez votre message ici...", key='input')
            submit_button = st.form_submit_button(label='Envoyer')

            if submit_button and user_input:
                output = conversation_chat(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                st.chat_message("user").write(st.session_state["past"][i], avatar_style="thumbs")
                st.chat_message("assistant").write(st.session_state["generated"][i], avatar_style="fun-emoji")

# Interface principale de l'application
if st.sidebar.button("Démarrer une conversation 💬 🚀💻"):
    st.session_state.start_chat = True
    st.session_state.thread_id = "dummy_thread_id"
    st.session_state.messages = []  # Réinitialisation des messages

st.title("Bac2Futur 🎯 ")
st.write("Bienvenue sur Bac2Futur, un assistant pour vous aider à trouver la formation et l'orientation qui vous convient.")

# Quitter la conversation
if st.button("Quitter la conversation :x: "):
    st.session_state.messages = []
    st.session_state.start_chat = False
    st.session_state.thread_id = None

# Affichage de l'historique et gestion de la conversation
if st.session_state.start_chat:
    initialize_session_state()
    display_chat_history()
