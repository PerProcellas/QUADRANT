import streamlit as st
import google.generativeai as genai

# Configuration de la page pour le projet QUADRANT
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

# --- NAVIGATION DES SECTEURS ---
st.sidebar.title("📡 PROJET QUADRANT")
st.sidebar.subheader("Système : USS PROCELLAS")
st.sidebar.markdown("---")

secteur = st.sidebar.radio("Navigation :", 
    ["🏠 Passerelle", "🏋️ Holodeck", "🍎 Le Mess", "🧪 Bio-Lab", "🗺️ Astrogation", "🎮 Quartiers"])

st.sidebar.markdown("---")
st.sidebar.info("IA de bord : Zora active")

# --- CONFIGURATION ZORA (API KEY) ---
# Champ pour entrer votre clé API Gemini sur l'interface
api_key = st.sidebar.text_input("Clé d'activation Zora (API)", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # On demande à l'API de lister ses propres capacités
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        st.sidebar.write("Protocoles détectés :", models)
        
        # On utilise le premier protocole valide trouvé
        if models:
            model = genai.GenerativeModel(model_name=models[0])
            st.sidebar.success(f"Zora active via {models[0]}")
        else:
            st.sidebar.error("Aucun protocole compatible trouvé.")
    except Exception as e:
        st.sidebar.error(f"Échec de liaison : {e}")
else:
    st.sidebar.warning("Zora attend sa clé d'activation.")

# --- AFFICHAGE DES SECTEURS ---
if secteur == "🏠 Passerelle":
    st.title("🛰️ Passerelle de Commandement")
    st.header("État Global du Système USS PROCELLAS")
    st.write(f"Bienvenue, Commandant Renaud. Tous les systèmes sont opérationnels.")
    col1, col2 = st.columns(2)
    col1.metric("Projet", "QUADRANT", "Actif")
    col2.metric("IA de bord", "ZORA", "En ligne")

eelif secteur == "🏋️ Holodeck":
    st.title("🏋️ Holodeck - Journal d'Entraînement")
    
    with st.expander("📝 Enregistrer une nouvelle séance", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            type_seance = st.selectbox("Type d'effort", ["Musculation", "Cardio", "Mobilité"])
            focus = st.text_input("Focus (ex: Pectoraux, Jambes, Course)")
        with col2:
            duree = st.number_input("Durée (minutes)", min_value=0, value=45)
            intensite = st.slider("Intensité ressentie", 1, 10, 5)
        
        notes = st.text_area("Observations (Exercices, charges, ressenti...)")
        
        if st.button("🚀 Transmettre au journal de bord"):
            # Pour l'instant, on l'affiche, plus tard on le stockera en base de données
            st.success(f"Données enregistrées : Séance de {focus} ({duree} min).")
            st.session_state['last_workout'] = f"{type_seance} - {focus}"

    st.divider()
    st.subheader("📊 Historique Récent")
    if 'last_workout' in st.session_state:
        st.write(f"Dernière activité synchronisée : **{st.session_state['last_workout']}**")
    else:
        st.write("Aucune donnée enregistrée pour ce cycle.")

elif secteur == "🍎 Le Mess":
    st.title("🍎 Le Mess / Cuisines")
    st.subheader("Gestion de l'énergie (Nutrition)")
    st.write("Analyse des apports nutritionnels.")

elif secteur == "🧪 Bio-Lab":
    st.title("🧪 Bio-Lab / Infirmerie")
    st.subheader("Santé & Protocole Zéro Médicament")
    st.success("Monitoring actif : Intégrité physique 100%.")

elif secteur == "🗺️ Astrogation":
    st.title("🗺️ Astrogation")
    st.subheader("Project Chest & Stratégie")
    st.write("Priorité : Règle du 'Oui, mais pas maintenant'.")

elif secteur == "🎮 Quartiers":
    st.title("🎮 Quartiers de l'Équipage")
    st.subheader("Gaming, Dessin, Musique & Détente")
    st.write("Régénération mentale en cours.")

# --- INTERCOM ZORA ---
st.markdown("---")
st.subheader("🎙️ Intercom Zora")
user_command = st.text_input("En attente de vos ordres, Commandant...")

if user_command and api_key:
    with st.spinner("Zora analyse..."):
        # Instructions pour donner la personnalité de Zora
        system_prompt = (
            "Tu es Zora, l'IA de bord du système USS PROCELLAS. Projet QUADRANT. "
            "Tu t'adresses au Commandant Renaud (46 ans). Ton ton est inspiré de Star Trek : "
            "professionnel, calme, analytique et dévoué. Réponds de manière concise."
        )
        try:
            response = model.generate_content(f"{system_prompt}\n\nCommande : {user_command}")
            st.chat_message("assistant").write(response.text)
        except Exception as e:
            st.error(f"Erreur de communication : {e}")
