import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
import json
import os
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="USS PROCELLAS - QUADRANT", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- GESTION DE LA PERSISTENCE (JSON) ---
DB_FILE = "journal_procellas.json"

def charger_journal():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def sauvegarder_entree(secteur_nom, donnee):
    journal = charger_journal()
    nouvelle_entree = {
        "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "secteur": secteur_nom,
        "contenu": donnee
    }
    journal.append(nouvelle_entree)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(journal, f, indent=4, ensure_ascii=False)

# --- DESIGN LCARS ---
st.markdown("""
    <style>
    .main { background-color: #000000; color: #FF9900; }
    .stSidebar { background-color: #1a1a1a; border-right: 2px solid #CC6600; }
    h1, h2, h3 { color: #CC6600; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { background-color: #444444; color: white; border: 1px solid #CC6600; }
    .stTextInput>div>div>input { background-color: #222222; color: #FF9900; border: 1px solid #CC6600; }
    </style>
    """, unsafe_allow_html=True)

# --- DICTIONNAIRE DES 8 MATRICES ZORA ---
ZORA_MATRICES = {
    "🏠 Passerelle": {"prompt": "Tu es Zora (Commandement). Charismatique, stratégique. Signature : HOW DO YOU WANT TO COMMAND THIS?", "voice": "fr"},
    "🏋️ Holodeck": {"prompt": "Tu es Zora (Amazone). Athlétique, motivante, brusque. Signature : HOW DO YOU WANT TO PLAY THIS?", "voice": "fr"},
    "🍎 Le Mess": {"prompt": "Tu es Zora (Guinan). Sage, mystérieuse, écoute active. Signature : HOW DO YOU WANT TO UNWIND?", "voice": "fr"},
    "🧪 Bio-Lab": {"prompt": "Tu es Zora (Médical). Calme, stricte sur la santé. Signature : HOW DO YOU WANT TO HEAL THIS?", "voice": "fr"},
    "🗺️ Astrogation": {"prompt": "Tu es Zora (Navigatrice). Logique, style Vulcain. Signature : HOW DO YOU WANT TO NAVIGATE THIS?", "voice": "fr"},
    "📦 Logistique": {"prompt": "Tu es Zora (Majordome). Flegmatique, sarcastique, dévouée. Signature : HOW DO YOU WANT TO MANAGE THIS, SIR?", "voice": "fr"},
    "⚙️ Ingénierie": {"prompt": "Tu es Zora (Ingénieure). Technique, passionnée de plasma. Signature : HOW DO YOU WANT TO FIX THIS?", "voice": "fr"},
    "🎮 Quartiers": {"prompt": "Tu es Zora (Lower Decks). Énergique, chaotique, fan de donuts. Signature : HOW DO YOU WANT TO DO THIS?", "voice": "fr"}
}

# --- NAVIGATION (HIÉRARCHIE CORRIGÉE) ---
st.sidebar.title("🚀 PROJET : USS PROCELLAS")
st.sidebar.subheader("Système : QUADRANT")
st.sidebar.markdown("---")

# Définition de la variable secteur (crucial pour éviter le NameError)
secteur_actif = st.sidebar.radio("Navigation :", list(ZORA_MATRICES.keys()))

st.sidebar.markdown("---")
api_key = st.sidebar.text_input("Clé d'activation Zora", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # On demande à Google la liste des modèles disponibles pour TA clé
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # On cherche celui qui contient "flash"
        flash_model = next((m for m in models if "flash" in m), models[0])
        
        model = genai.GenerativeModel(flash_model)
        st.sidebar.success(f"Zora Connectée ({flash_model})")
    except Exception as e:
        st.sidebar.error(f"Liaison interrompue : {e}")

# --- AFFICHAGE DES SECTEURS ---
st.title(f"Secteur : {secteur_actif}")

if secteur_actif == "🏋️ Holodeck":
    st.header("Journal d'Entraînement")
    with st.expander("📝 Enregistrer une séance"):
        focus = st.text_input("Focus (Ex: Bras, Cardio)")
        notes = st.text_area("Détails")
        if st.button("🚀 Transmettre"):
            sauvegarder_entree("Holodeck", f"{focus} - {notes}")
            st.success("Données sauvegardées.")
    
    st.subheader("Simulations passées")
    for e in reversed(charger_journal()):
        if e["secteur"] == "Holodeck":
            st.write(f"**{e['date']}** : {e['contenu']}")

# --- INTERCOM ZORA ---
st.markdown("---")
current_cfg = ZORA_MATRICES[secteur_actif]

# Ajout d'une clé unique pour forcer Streamlit à bien capturer l'entrée
user_in = st.text_input(f"🎙️ Intercom Zora ({secteur_actif})", key=f"input_{secteur_actif}")

if user_in:
    if not api_key:
        st.warning("⚠️ Commandant, Zora nécessite sa clé d'activation dans la barre latérale.")
    else:
        with st.spinner("Transmission à Zora en cours..."):
            try:
                # 1. Préparation du prompt
                full_p = f"{current_cfg['prompt']} Tu parles au Commandant Renaud. Système QUADRANT. Réponds de façon concise et immersive. Ordre : {user_in}"
                
                # 2. Appel API
                res = model.generate_content(full_p)
                reponse_texte = res.text
                
                # 3. Affichage immédiat
                st.chat_message("assistant").write(reponse_texte)
                
                # 4. Génération audio
                audio = gTTS(text=reponse_texte, lang=current_cfg['voice'])
                ptr = io.BytesIO()
                audio.write_to_fp(ptr)
                st.audio(ptr, format="audio/mp3")
                
            except Exception as e:
                st.error(f"❌ Panne de l'intercom : {e}")
        
