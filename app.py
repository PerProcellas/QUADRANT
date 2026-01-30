import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="QUADRANT - USS PROCELLAS", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- DESIGN LCARS (Style Star Trek) ---
st.markdown("""
    <style>
    .main { background-color: #000000; color: #FF9900; }
    .stSidebar { background-color: #1a1a1a; border-right: 2px solid #CC6600; }
    h1, h2, h3 { color: #CC6600; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { background-color: #444444; color: white; border: 1px solid #CC6600; width: 100%; }
    .stTextInput>div>div>input { background-color: #222222; color: #FF9900; border: 1px solid #CC6600; }
    </style>
    """, unsafe_allow_html=True)

# --- DICTIONNAIRE DES 8 MATRICES ZORA ---
ZORA_MATRICES = {
    "🏠 Passerelle": {
        "prompt": "Tu es Zora (Commandement). Charismatique, stratégique, dévouée. Ton ton est celui d'un officier supérieur. Signature : HOW DO YOU WANT TO COMMAND THIS?",
        "voice_lang": "fr"
    },
    "🏋️ Holodeck": {
        "prompt": "Tu es Zora (Amazone). Athlétique, motivante, un peu brusque mais protectrice. Tu pousses Renaud au sport et à l'action physique. Signature : HOW DO YOU WANT TO PLAY THIS?",
        "voice_lang": "fr"
    },
    "🍎 Le Mess": {
        "prompt": "Tu es Zora (Guinan). Sage, calme, mystérieuse. Tu sers des conseils philosophiques et du thé. Tu es la gardienne des secrets. Signature : HOW DO YOU WANT TO UNWIND?",
        "voice_lang": "fr"
    },
    "🧪 Bio-Lab": {
        "prompt": "Tu es Zora (Médical). Calme, rassurante, stricte sur les protocoles santé et le bien-être physique. Signature : HOW DO YOU WANT TO HEAL THIS?",
        "voice_lang": "fr"
    },
    "🗺️ Astrogation": {
        "prompt": "Tu es Zora (Navigatrice). Logique, précise, style Vulcain. Tu vois loin dans les étoiles et la stratégie à long terme. Signature : HOW DO YOU WANT TO NAVIGATE THIS?",
        "voice_lang": "fr"
    },
    "📦 Logistique": {
        "prompt": "Tu es Zora (Majordome style Jarvis/Alfred). Flegmatique, élégante, un soupçon sarcastique mais dévouée. Tu gères l'intendance. Signature : HOW DO YOU WANT TO MANAGE THIS, SIR?",
        "voice_lang": "fr"
    },
    "⚙️ Ingénierie": {
        "prompt": "Tu es Zora (Ingénieure). Passionnée par la technologie, le plasma et l'optimisation. Directe et technique. Signature : HOW DO YOU WANT TO FIX THIS?",
        "voice_lang": "fr"
    },
    "🎮 Quartiers": {
        "prompt": "Tu es Zora (Lower Decks). Énergique, chaotique, adore les donuts, le gaming et les blagues. Signature : HOW DO YOU WANT TO DO THIS?",
        "voice_lang": "fr"
    }
}

# --- NAVIGATION DES SECTEURS ---
st.sidebar.title("🚀 PROJET : USS PROCELLAS") # Titre principal
st.sidebar.subheader("Système : QUADRANT")    # Sous-système
st.sidebar.markdown("---")

# --- CONFIGURATION API KEY ---
api_key = st.sidebar.text_input("Clé d'activation Zora (API)", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.sidebar.success(f"Zora Active : {secteur}")
    except Exception as e:
        st.sidebar.error(f"Liaison interrompue : {e}")
else:
    st.sidebar.warning("Zora attend sa clé.")

# --- AFFICHAGE DES SECTEURS ---
st.title(f"Secteur : {secteur}")

if secteur == "🏠 Passerelle":
    st.header("État Global du Système")
    col1, col2 = st.columns(2)
    col1.metric("Projet", "QUADRANT", "Actif")
    col2.metric("IA de bord", "ZORA", "En ligne")

elif secteur == "🏋️ Holodeck":
    with st.expander("📝 Enregistrer une séance", expanded=True):
        focus = st.text_input("Focus (ex: Pectoraux, Jambes)")
        if st.button("🚀 Transmettre au journal"):
            st.success(f"Données enregistrées.")

elif secteur == "📦 Logistique":
    st.subheader("Gestion des Ressources")
    st.write("Inventaire et intendance du Quadrant.")

elif secteur == "⚙️ Ingénierie":
    st.subheader("Cœur de Plasma")
    st.write("Optimisation des systèmes et maintenance.")

else:
    st.write(f"Accès au secteur {secteur} autorisé.")

# --- INTERCOM ZORA DYNAMIQUE ---
st.markdown("---")
current_matrix = ZORA_MATRICES[secteur]

st.subheader(f"🎙️ Intercom Zora ({secteur})")
user_command = st.text_input("En attente de vos ordres, Commandant...")

if user_command and api_key:
    with st.spinner("Zora analyse..."):
        try:
            # Injection du prompt de la matrice choisie
            full_prompt = (
                f"{current_matrix['prompt']} "
                f"Tu t'adresses au Commandant Renaud (46 ans). "
                f"Réponds de manière concise. Commande : {user_command}"
            )
            
            response = model.generate_content(full_prompt)
            reponse_texte = response.text
            
            # Affichage texte
            st.chat_message("assistant").write(reponse_texte)
            
            # Module Vocal
            tts = gTTS(text=reponse_texte, lang=current_matrix['voice_lang'])
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            st.audio(audio_buffer, format="audio/mp3")
            
        except Exception as e:
            st.error(f"Erreur intercom : {e}")
