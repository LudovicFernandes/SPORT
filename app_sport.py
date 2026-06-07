import streamlit as st
import pandas as pd
import datetime
import json
import requests

# Configuration de la page
st.set_page_config(page_title="Mon Coach Sportif", page_icon="💪", layout="wide")

# ==============================================================================
# SYSTÈME DE SAUVEGARDE CLOUD (JSONBIN.IO)
# ==============================================================================
# ⚠️ REMPLACEZ CES DEUX LIGNES PAR VOS CLÉS OBTENUES PRÉCÉDEMMENT ⚠️
API_KEY = "VOTRE_API_KEY_ICI" 
BIN_ID = "VOTRE_BIN_ID_ICI"

URL_JSONBIN = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

CATEGORIES = [
    "🍗 Jambes", 
    "🏋️‍♂️ Pecs", 
    "📐 Dos", 
    "🦅 Épaules", 
    "💪 Biceps", 
    "⚡ Triceps",
    "💪 Haltères / Banc"
]

def sauvegarder_donnees():
    """Sauvegarde l'état des exercices et de l'historique dans le Cloud"""
    donnees_a_sauvegarder = {
        "exercices_sport": st.session_state.exercices_sport
    }
    try:
        payload = json.dumps(donnees_a_sauvegarder)
        requests.put(URL_JSONBIN, data=payload, headers=HEADERS)
    except Exception as e:
        st.error(f"Erreur de sauvegarde Cloud : {e}")

def charger_donnees():
    """Charge les données depuis JSONBin"""
    try:
        req = requests.get(URL_JSONBIN, headers=HEADERS)
        if req.status_code == 200:
            return req.json().get("record")
    except:
        return None
    return None

# Initialisation avec uniquement VOS exercices triés
if 'initialise_sport' not in st.session_state:
    data_cloud = charger_donnees()
    
    if data_cloud and "exercices_sport" in data_cloud:
        st.session_state.exercices_sport = data_cloud["exercices_sport"]
    else:
        st.session_state.exercices_sport = [
            {"nom": "Abductor", "categorie": "🍗 Jambes", "poids": 85.0, "reps": 12, "historique": []},
            {"nom": "Leg Press", "categorie": "🍗 Jambes", "poids": 140.0, "reps": 10, "historique": []},
            {"nom": "Leg Curl", "categorie": "🍗 Jambes", "poids": 55.0, "reps": 10, "historique": []},
            {"nom": "Leg Extension", "categorie": "🍗 Jambes", "poids": 55.0, "reps": 12, "historique": []},
            {"nom": "V Squat", "categorie": "🍗 Jambes", "poids": 25.0, "reps": 10, "historique": []},
            {"nom": "Prone Legs Curl", "categorie": "🍗 Jambes", "poids": 32.5, "reps": 12, "historique": []},
            {"nom": "Hack squat", "categorie": "🍗 Jambes", "poids": 40.0, "reps": 10, "historique": []},
            {"nom": "Bench barre (Développé couché)", "categorie": "🏋️‍♂️ Pecs", "poids": 80.0, "reps": 2, "historique": []},
            {"nom": "Développé couché Assisté", "categorie": "🏋️‍♂️ Pecs", "poids": 30.0, "reps": 10, "historique": []},
            {"nom": "Chest press", "categorie": "🏋️‍♂️ Pecs", "poids": 35.0, "reps": 10, "historique": []},
            {"nom": "Pectoral machine", "categorie": "🏋️‍♂️ Pecs", "poids": 20.0, "reps": 10, "historique": []},
            {"nom": "Pecs debout machine", "categorie": "🏋️‍♂️ Pecs", "poids": 50.0, "reps": 10, "historique": []},
            {"nom": "Poulie vis à vis Haut", "categorie": "🏋️‍♂️ Pecs", "poids": 10.0, "reps": 10, "historique": []},
            {"nom": "Poulie vis à vis Milieu", "categorie": "🏋️‍♂️ Pecs", "poids": 10.0, "reps": 10, "historique": []},
            {"nom": "Poulie vis à vis Bas", "categorie": "🏋️‍♂️ Pecs", "poids": 7.5, "reps": 10, "historique": []},
            {"nom": "Tirage horizontal", "categorie": "📐 Dos", "poids": 45.0, "reps": 10, "historique": []},
            {"nom": "Tirage horizontal 1 main", "categorie": "📐 Dos", "poids": 30.0, "reps": 10, "historique": []},
            {"nom": "Tirage vertical", "categorie": "📐 Dos", "poids": 55.0, "reps": 10, "historique": []},
            {"nom": "Pull Down", "categorie": "📐 Dos", "poids": 55.0, "reps": 10, "historique": []},
            {"nom": "Row machine", "categorie": "📐 Dos", "poids": 65.0, "reps": 10, "historique": []},
            {"nom": "Frontal pull-down (Fond)", "categorie": "📐 Dos", "poids": 40.0, "reps": 10, "historique": []},
            {"nom": "Low Row", "categorie": "📐 Dos", "poids": 80.0, "reps": 10, "historique": []},
            {"nom": "Épaule machine", "categorie": "🦅 Épaules", "poids": 25.0, "reps": 10, "historique": []},
            {"nom": "Shoulder press épaule", "categorie": "🦅 Épaules", "poids": 25.0, "reps": 10, "historique": []},
            {"nom": "Élévation latérale Machine", "categorie": "🦅 Épaules", "poids": 25.0, "reps": 10, "historique": []},
            {"nom": "Poulie vis à vis Haut / Triceps", "categorie": "⚡ Triceps", "poids": 27.5, "reps": 10, "historique": []},
            {"nom": "Poulie vis à vis Bas Bibi/Tri", "categorie": "⚡ Triceps", "poids": 20.0, "reps": 10, "historique": []},
            {"nom": "Poulie Triceps (nuque)", "categorie": "⚡ Triceps", "poids": 12.0, "reps": 10, "historique": []},
            {"nom": "Triceps Push Down corde", "categorie": "⚡ Triceps", "poids": 20.0, "reps": 10, "historique": []},
            {"nom": "Extension poulie triceps nuque", "categorie": "⚡ Triceps", "poids": 12.5, "reps": 10, "historique": []},
            {"nom": "Curl banc allongé (Haltères)", "categorie": "💪 Haltères / Banc", "poids": 30.0, "reps": 10, "historique": []},
            {"nom": "Assis épaule (Haltères)", "categorie": "💪 Haltères / Banc", "poids": 14.0, "reps": 10, "historique": []},
            {"nom": "Curl marteaux (Haltères)", "categorie": "💪 Haltères / Banc", "poids": 12.0, "reps": 10, "historique": []},
            {"nom": "Curl haltère assis", "categorie": "💪 Haltères / Banc", "poids": 12.0, "reps": 11, "historique": []},
            {"nom": "Élévation latérale (Haltères)", "categorie": "💪 Haltères / Banc", "poids": 10.0, "reps": 15, "historique": []},
            {"nom": "Curl Pupitre", "categorie": "💪 Haltères / Banc", "poids": 15.0, "reps": 15, "historique": []},
            {"nom": "Curl Pupitre Altère", "categorie": "💪 Haltères / Banc", "poids": 16.0, "reps": 10, "historique": []}
        ]
        sauvegarder_donnees()
    st.session_state.initialise_sport = True

# ==============================================================================
# STYLE CSS RE-STYLISÉ
# ==============================================================================
st.markdown("""
<style>
    .stApp { background-color: #f1f3f5; }
    h1, h2, h3 { color: #1e293b; font-weight: 800; }
    [data-testid="stSidebar"] { background-color: #1a202c !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #ffffff !important; }
    .history-row { background-color: #f8fafc; padding: 8px 15px; border-radius: 6px; margin-top: 5px; font-size: 14px; border-left: 3px solid #10b981; }
    /* Ajustement des conteneurs natifs Streamlit (bordure) */
    [data-testid="stVerticalBlockBorderWrapper"] { background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# FONCTION REPRÉSENTATION DU MANNEQUIN EN SVG
# ==============================================================================
def dessiner_mannequin(categorie_active):
    color_pecs = "#cbd5e1"
    color_dos = "#cbd5e1"
    color_jambes = "#cbd5e1"
    color_epaules = "#cbd5e1"
    color_bras = "#cbd5e1"
    
    if "Pecs" in categorie_active: color_pecs = "#ef4444"
    elif "Dos" in categorie_active: color_dos = "#ef4444"
    elif "Jambes" in categorie_active: color_jambes = "#ef4444"
    elif "Épaules" in categorie_active: color_epaules = "#ef4444"
    elif "Biceps" in categorie_active or "Triceps" in categorie_active or "Haltères" in categorie_active: color_bras = "#ef4444"

    svg_code = f"""
    <svg width="100%" height="240" viewBox="0 0 300 240" style="background-color:#ffffff; border-radius:12px; box-shadow:0 4px 6px rgba(0,0,0,0.02); padding:10px;">
        <text x="50" y="20" font-size="12" font-weight="bold" fill="#64748b" text-anchor="middle">FACE</text>
        <circle cx="50" cy="45" r="12" fill="#cbd5e1" />
        <path d="M42 60 L58 60 L62 65 L38 65 Z" fill="#cbd5e1" />
        <rect x="34" y="65" width="32" height="15" rx="3" fill="{color_pecs}" />
        <rect x="36" y="82" width="28" height="25" rx="2" fill="#cbd5e1" />
        <path d="M22 65 L32 65 L26 110 L18 110 Z" fill="{color_bras}" />
        <path d="M68 65 L78 65 L74 110 L82 110 Z" fill="{color_bras}" />
        <path d="M36 110 L48 110 L46 190 L34 190 Z" fill="{color_jambes}" />
        <path d="M52 110 L64 110 L66 190 L54 190 Z" fill="{color_jambes}" />
        <rect x="30" y="62" width="40" height="6" rx="2" fill="{color_epaules}" />

        <text x="180" y="20" font-size="12" font-weight="bold" fill="#64748b" text-anchor="middle">DOS</text>
        <circle cx="180" cy="45" r="12" fill="#cbd5e1" />
        <path d="M172 60 L188 60 L192 65 L168 65 Z" fill="#cbd5e1" />
        <path d="M162 65 L198 65 L194 108 L166 108 Z" fill="{color_dos}" />
        <rect x="166" y="109" width="28" height="10" fill="#cbd5e1" />
        <path d="M152 65 L160 65 L156 110 L148 110 Z" fill="{color_bras}" />
        <path d="M200 65 L208 65 L204 110 L212 110 Z" fill="{color_bras}" />
        <path d="M166 121 L179 121 L177 190 L164 190 Z" fill="{color_jambes}" />
        <path d="M181 121 L194 121 L196 190 L183 190 Z" fill="{color_jambes}" />
        <rect x="160" y="62" width="40" height="6" rx="2" fill="{color_epaules}" />
    </svg>
    """
    return st.markdown(svg_code, unsafe_allow_html=True)

# ==============================================================================
# MENU LATÉRAL
# ==============================================================================
st.sidebar.title("🏃‍♂️ Mon Coach Gym")
st.sidebar.write("Sélectionnez la zone musculaire à travailler aujourd'hui :")
filtre_cat = st.sidebar.radio("Groupes Musculaires :", ["Tous"] + CATEGORIES)

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Zone d'administration")
with st.sidebar.expander("➕ Ajouter un nouvel exercice personnalisé"):
    nv_nom = st.text_input("Nom de l'exercice :", key="nv_exo_nom")
    nv_cat = st.selectbox("Catégorie :", CATEGORIES, key="nv_exo_cat")
    if st.button("Créer la fiche exercice 🛠️"):
        if nv_nom.strip():
            st.session_state.exercices_sport.append({
                "nom": nv_nom, "categorie": nv_cat, "poids": 0.0, "reps": 0, "historique": []
            })
            sauvegarder_donnees()
            st.success("Nouvel exercice enregistré !")
            st.rerun()

# ==============================================================================
# ZONE DE CONTENU PRINCIPALE
# ==============================================================================
col_gauche, col_droite = st.columns([1.3, 0.7])

with col_gauche:
    st.title("💪 Mes Exercices")
    
    # 🔍 BARRE DE RECHERCHE AJOUTÉE ICI
    recherche = st.text_input("🔍 Rechercher un exercice par nom (ex: Poulie, Curl...) :")
    
    # Filtrer les exercices selon le choix latéral ET la barre de recherche
    exercices_filtrés = st.session_state.exercices_sport
    if filtre_cat != "Tous":
        exercices_filtrés = [e for e in exercices_filtrés if e["categorie"] == filtre_cat]
        
    if recherche:
        exercices_filtrés = [e for e in exercices_filtrés if recherche.lower() in e["nom"].lower()]

    if not exercices_filtrés:
        st.info("Aucun exercice trouvé correspondant à vos critères.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Affichage de chaque exercice dans un "carré blanc" natif (container avec bordure)
    for idx, exo in enumerate(exercices_filtrés):
        index_reel = st.session_state.exercices_sport.index(exo)
        
        with st.container(border=True):
            st.markdown(f"<h3 style='margin-bottom:0;'>{exo['nom']} <span style='font-size:12px; font-weight:normal; background-color:#e2e8f0; padding:2px 8px; border-radius:10px; color:#475569; margin-left:10px;'>{exo['categorie']}</span></h3>", unsafe_allow_html=True)
            
            # Formulaire de modification DIRECTEMENT dans le carré
            c1, c2, c3 = st.columns([1.5, 1.5, 1.5])
            
            poids_saisi = c1.number_input("Poids (kg)", min_value=0.0, value=float(exo["poids"]), step=0.5, key=f"poids_{index_reel}")
            reps_saisie = c2.number_input("Répétitions", min_value=0, value=int(exo["reps"]), step=1, key=f"reps_{index_reel}")
            
            c3.write("") # Petit espacement pour aligner le bouton avec les champs
            c3.write("")
            if c3.button("Actualiser ⚡", key=f"btn_{index_reel}", use_container_width=True):
                if poids_saisi != exo["poids"] or reps_saisie != exo["reps"]:
                    date_aujourdhui = datetime.date.today().strftime("%d/%m/%Y")
                    
                    nouvelle_archive = {
                        "date": date_aujourdhui,
                        "poids": exo["poids"],
                        "reps": exo["reps"]
                    }
                    st.session_state.exercices_sport[index_reel]["historique"].append(nouvelle_archive)
                    
                    st.session_state.exercices_sport[index_reel]["poids"] = poids_saisi
                    st.session_state.exercices_sport[index_reel]["reps"] = reps_saisie
                    
                    sauvegarder_donnees()
                    st.success("Enregistré !")
                    st.rerun()
            
            # Historique et Suppression cachés dans un déroulant pour ne pas polluer l'interface
            with st.expander("📜 Voir l'historique & Options", expanded=False):
                if exo["historique"]:
                    for log in reversed(exo["historique"]):
                        st.markdown(f"""
                        <div class="history-row">
                            📅 <b>Le {log['date']}</b> : <b>{log['poids']:.1f} kg</b> sur <b>{log['reps']}</b> reps
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.caption("Aucun ancien historique.")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Supprimer l'exercice", key=f"del_{index_reel}"):
                    st.session_state.exercices_sport.pop(index_reel)
                    sauvegarder_donnees()
                    st.rerun()

with col_droite:
    st.markdown("<h2 style='text-align: center;'>Anatomie Ciblée</h2>", unsafe_allow_html=True)
    st.write("Le mannequin met en valeur la zone musculaire sélectionnée à gauche :")
    
    dessiner_mannequin(filtre_cat)
