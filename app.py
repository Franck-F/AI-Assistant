import openai
import streamlit as st
import time
import arxiv
from dotenv import load_dotenv
import os
import re
from PIL import Image

# Charger le fichier .env contenant la clé API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuration de la page
st.set_page_config(
    page_title="Bac2Futur - Assistant d'Orientation",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #E2E8F0;
    }

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px) saturate(180%);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 900px;
    }

    /* Header Styling */
    .stHeadingContainer h1 {
        font-weight: 800;
        letter-spacing: -0.025em;
        background: linear-gradient(135deg, #60A5FA 0%, #2563EB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }

    /* Chat Styling */
    .stChatMessage {
        background: rgba(30, 41, 59, 0.5) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
        transition: all 0.2s ease;
    }
    
    .stChatMessage:hover {
        border-color: rgba(255, 255, 255, 0.1);
        background: rgba(30, 41, 59, 0.7) !important;
    }
    
    /* Input Area Styling */
    .stChatInputContainer {
        border-radius: 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(16px) !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
    }

    /* Info Boxes */
    .stAlert {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #94A3B8;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 500;
        text-align: left;
        padding: 0.75rem 1rem;
    }
    .stButton > button:hover {
        background: rgba(37, 99, 235, 0.1);
        border-color: #3B82F6;
        color: #F8FAFC;
        transform: translateX(4px);
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des variables de session
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ---
with st.sidebar:
    # Logo
    try:
        st.image("B2MF_v4.svg", width=140)
    except:
        st.title("Bac2Futur")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Équipe")
    st.info("""
    Frank-Dilane FAMBOU  
    Luana GUALDI  
    Claude-Christian LETEMBET-AMBILY  
    Djouhra OULD-YOUNES  
    Fatoumata SARR
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Suggestions")
    suggestions = [
        "Rédaction de lettre de motivation Parcoursup",
        "Formations en Intelligence Artificielle",
        "Recherche d'alternance en marketing",
        "Comprendre le RNCP"
    ]
    for s in suggestions:
        if st.button(s, key=s, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": s})
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Réinitialiser la session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CONTENT ---
st.title("Bac2Futur")
st.markdown("##### Expert digital pour votre orientation stratégique.")

# Instructions initiales si pas de messages
if not st.session_state.messages:
    st.markdown("""
    <div style="background: rgba(30, 41, 59, 0.4); padding: 2.5rem; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.05); margin-top: 2rem;">
        <h2 style="color: #F8FAFC; margin-top: 0;">Bienvenue sur Bac2Futur</h2>
        <p style="color: #94A3B8; font-size: 1.1rem;">L'assistant intelligent dédié à l'accompagnement de vos parcours académiques et professionnels.</p>
        <div style="margin-top: 1.5rem;">
            <p style="color: #64748B; font-weight: 600; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.05em;">Capabilities</p>
            <ul style="color: #94A3B8; list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 0.5rem; display: flex; align-items: center;">
                    <span style="width: 6px; height: 6px; background: #3B82F6; border-radius: 50%; margin-right: 12px;"></span>
                    Analyse de catalogues de formation complexes
                </li>
                <li style="margin-bottom: 0.5rem; display: flex; align-items: center;">
                    <span style="width: 6px; height: 6px; background: #3B82F6; border-radius: 50%; margin-right: 12px;"></span>
                    Accompagnement stratégique Parcoursup
                </li>
                <li style="margin-bottom: 0.5rem; display: flex; align-items: center;">
                    <span style="width: 6px; height: 6px; background: #3B82F6; border-radius: 50%; margin-right: 12px;"></span>
                    Optimisation de dossiers de candidature
                </li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Affichage de l'historique du chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Gestion de l'input utilisateur
if prompt := st.chat_input("Décrivez votre besoin d'orientation..."):
    # Ajout du message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse de l'assistant
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system", 
                        "content": "Tu es Bac2Futur, un expert en orientation scolaire et professionnelle en France. Ton ton est professionnel, analytique et constructif. Évite les émojis. Fournis des réponses structurées avec des points clés."
                    },
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                stream=True,
            )
            
            for chunk in response:
                full_response += chunk.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▊")
            
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Une erreur système est survenue : {e}")
            full_response = "Le service rencontre actuellement une surcharge. Veuillez retenter votre requête d'ici quelques instants."
            message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
