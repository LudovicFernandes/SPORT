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

CATEGORIES = ["🏋️‍♂️ Pecs", "📐 Dos", "🍗 Jambes", "🦅 Épaules", "💪 Biceps", "⚡ Triceps"]

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

# Initialisation de la liste des exercices par défaut (si vide sur le Cloud)
if 'initialise_sport' not in st.session_state:
    data_cloud = charger_donnees()
    
    if data_cloud and "exercices_sport" in data_cloud:
        st.session_state.exercices_sport = data_cloud["exercices_sport"]
    else:
        # Liste initiale propre et triée par défaut
        st.session_state.exercices_sport = [
            {"nom": "Développé couché", "categorie": "🏋️‍♂️ Pecs", "poids": 60.0, "reps": 10, "historique": []},
            {"nom": "Écarté poulie haute", "categorie": "🏋️‍♂️ Pecs", "poids": 25.0, "reps": 12, "historique": []},
            {"nom": "Tirage poitrine (Poulie)", "categorie": "📐 Dos", "poids": 50.0, "reps": 10, "historique": []},
            {"nom": "Soulevé de terre", "categorie": "📐 Dos", "poids": 90.0, "reps": 8, "historique": []},
            {"nom": "Squat Barre", "categorie": "🍗 Jambes", "poids": 80.0, "reps": 10, "historique": []},
            {"nom": "Presse à cuisses", "categorie": "🍗 Jambes", "poids": 140.0, "reps": 12, "historique": []},
            {"nom": "Développé militaire", "categorie": "🦅 Épaules", "poids": 40.0, "reps": 10, "historique": []},
            {"nom": "Élévations latérales", "categorie": "🦅 Épaules", "poids": 10.0, "reps": 15, "historique": []},
            {"nom": "Curl Barre (Z)", "categorie": "💪 Biceps", "poids": 30.0, "reps": 10, "historique": []},
            {"nom": "Extension poulie haute", "categorie": "⚡ Triceps", "poids": 20.0, "reps": 12, "historique": []},
        ]
        sauvegarder_donnees()
    st.session_state.initialise_sport = True

# ==============================================================================
# STYLE CSS RE-STYLISÉ (STYLE SALLE DE SPORT / ATHLÉTIQUE)
# ==============================================================================
st.markdown("""
<style>
    .stApp { background-color: #f1f3f5; }
    h1, h2, h3 { color: #1e293b; font-weight: 800; }
    [data-testid="stSidebar"] { background-color: #1a202c !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #ffffff !important; }
    .exercise-card { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-left: 5px solid #e2e8f0; margin-bottom: 15px; }
    .active-card { border-left: 5px solid #3b82f6 !important; background-color: #f8fafc; }
    .history-row { background-color: #f8fafc; padding: 8px 15px; border-radius: 6px; margin-top: 5px; font-size: 14px; border-left: 3px solid #10b981; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# FONCTION REPRÉSENTATION DU MANNEQUIN EN SVG
# ==============================================================================
def dessiner_mannequin(categorie_active):
    # Couleurs par défaut (gris neutre pour le corps)
    color_pecs = "#cbd5e1"
    color_dos = "#cbd5e1"
    color_jambes = "#cbd5e1"
    color_epaules = "#cbd5e1"
    color_bras = "#cbd5e1"
    
    # Allumage de la zone en rouge vif si sélectionnée
    if "Pecs" in categorie_active: color_pecs = "#ef4444"
    elif "Dos" in categorie_active: color_dos = "#ef4444"
    elif "Jambes" in categorie_active: color_jambes = "#ef4444"
    elif "Épaules" in categorie_active: color_epaules = "#ef4444"
    elif "Biceps" in categorie_active or "Triceps" in categorie_active: color_bras = "#ef4444"

    # Code SVG d'un mannequin stylisé face + dos
    svg_code = f"""
    <svg width="100%" height="240" viewBox="0 0 300 240" style="background-color:#ffffff; border-radius:12px; box-shadow:0 4px 6px rgba(0,0,0,0.02); padding:10px;">
        <text x="50" y="20" font-size="12" font-weight="bold" fill="#64748b" text-anchor="middle">FACE</text>
        <circle cx="50" cy="45" r="12" fill="#cbd5e1" /> <path d="M42 60 L58 60 L62 65 L38 65 Z" fill="#cbd5e1" /> <rect x="34" y="65" width="32" height="15" rx="3" fill="{color_pecs}" /> <rect x="36" y="82" width="28" height="25" rx="2" fill="#cbd5e1" /> <path d="M22 65 L32 65 L26 110 L18 110 Z" fill="{color_bras}" /> <path d="M68 65 L78 65 L74 110 L82 110 Z" fill="{color_bras}" /> <path d="M36 110 L48 110 L46 190 L34 190 Z" fill="{color_jambes}" /> <path d="M52 110 L64 110 L66 190 L54 190 Z" fill="{color_jambes}" /> <rect x="30" y="62" width="40" height="6" rx="2" fill="{color_epaules}" /> <text x="180" y="20" font-size="12" font-weight="bold" fill="#64748b" text-anchor="middle">DOS</text>
        <circle cx="180" cy="45" r="12" fill="#cbd5e1" /> <path d="M172 60 L188 60 L192 65 L168 65 Z" fill="#cbd5e1" /> <path d="M162 65 L198 65 L194 108 L166 108 Z" fill="{color_dos}" /> <rect x="166" y="109" width="28" height="10" fill="#cbd5e1" /> <path d="M152 65 L160 65 L156 110 L148 110 Z" fill="{color_bras}" /> <path d="M200 65 L208 65 L204 110 L212 110 Z" fill="{color_bras}" /> <path d="M166 121 L179 121 L177 190 L164 190 Z" fill="{color_jambes}" /> <path d="M181 121 L194 121 L196 190 L183 190 Z" fill="{color_jambes}" /> <rect x="160" y="62" width="40" height="6" rx="2" fill="{color_epaules}" /> </svg>
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
    st.title("💪 Liste des Exercices & Performances")
    
    # Filtrer les exercices selon le choix latéral
    exercices_filtrés = st.session_state.exercices_sport
    if filtre_cat != "Tous":
        exercices_filtrés = [e for e in st.session_state.exercices_sport if e["categorie"] == filtre_cat]

    if not exercices_filtrés:
        st.info("Aucun exercice créé dans cette catégorie pour le moment.")
    
    # Affichage de chaque exercice
    for idx, exo in enumerate(exercices_filtrés):
        # Trouver l'index réel dans la session_state globale
        index_reel = st.session_state.exercices_sport.index(exo)
        
        st.markdown(f"""
        <div class="exercise-card">
            <h3 style="margin:0 0 5px 0;">🏋️‍♂️ {exo['nom']}</h3>
            <span style="font-size:12px; background-color:#e2e8f0; padding:3px 8px; border-radius:15px; color:#475569;">{exo['categorie']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Formulaire de modification pour chaque exercice
        with st.expander("📝 Ajuster Poids & Répétitions / Voir l'historique", expanded=False):
            c1, c2, c3 = st.columns([2, 2, 2])
            
            # Inputs chargés avec les valeurs actuelles
            poids_saisi = c1.number_input("Poids actuel (kg)", min_value=0.0, value=float(exo["poids"]), step=2.5, key=f"poids_{index_reel}")
            reps_saisie = c2.number_input("Répétitions", min_value=0, value=int(exo["reps"]), step=1, key=f"reps_{index_reel}")
            
            # Détection d'un changement pour soumettre
            if c3.button("Actualiser la charge ⚡", key=f"btn_{index_reel}"):
                # Si le poids ou les répétitions changent, on archive l'ANCIENNE valeur dans l'historique
                if poids_saisi != exo["poids"] or reps_saisie != exo["reps"]:
                    date_aujourdhui = datetime.date.today().strftime("%d/%m/%Y")
                    
                    # On crée la ligne d'archive avec l'ancien poids avant écrasement
                    nouvelle_archive = {
                        "date": date_aujourdhui,
                        "poids": exo["poids"],
                        "reps": exo["reps"]
                    }
                    st.session_state.exercices_sport[index_reel]["historique"].append(nouvelle_archive)
                    
                    # On applique les nouvelles valeurs actuelles
                    st.session_state.exercices_sport[index_reel]["poids"] = poids_saisi
                    st.session_state.exercices_sport[index_reel]["reps"] = reps_saisie
                    
                    sauvegarder_donnees()
                    st.success("Performances mémorisées et historique mis à jour !")
                    st.rerun()
            
            # Affichage de l'historique de cet exercice en dessous
            st.markdown("**📜 Historique de vos charges précédentes :**")
            if exo["historique"]:
                # On affiche du plus récent au plus ancien
                for log in reversed(exo["historique"]):
                    st.markdown(f"""
                    <div class="history-row">
                        📅 <b>Le {log['date']}</b> : charge de <b>{log['poids']:.1f} kg</b> sur <b>{log['reps']}</b> répétitions
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("Aucun ancien historique pour le moment. Modifiez le poids et validez pour créer votre première archive.")
            
            # Option de suppression de l'exercice
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Supprimer cet exercice de la liste", key=f"del_{index_reel}"):
                st.session_state.exercices_sport.pop(index_reel)
                sauvegarder_donnees()
                st.rerun()

with col_droite:
    st.markdown("<h2 style='text-align: center;'>Anatomie Ciblée</h2>", unsafe_allow_html=True)
    st.write("Le mannequin ci-dessous met en valeur la zone de travail musculaire sélectionnée dans votre filtre de gauche :")
    
    # Dessin dynamique du mannequin en fonction de la catégorie filtrée
    dessiner_mannequin(filtre_cat)
    
    st.markdown("---")
    st.markdown("""
    ### 💡 Conseils d'utilisation :
    - Quand vous changez le poids d'une machine (ex: passage de 15kg à 20kg), le site garde automatiquement en mémoire **"Le [Date du jour] : j'ai fait 15kg"**.
    - Pour créer un nouvel exercice, ouvrez le volet dans la barre noire tout à gauche.
    """)
