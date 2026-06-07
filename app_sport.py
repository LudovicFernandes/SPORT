import streamlit as st
import streamlit.components.v1 as components # NOUVEAU : Pour l'affichage pro du mannequin
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

# Définition des catégories
CAT_JAMBES = "🍗 Jambes"
CAT_PECS = "🏋️‍♂️ Pecs"
CAT_DOS = "📐 Dos"
CAT_EPAULES = "🦅 Épaules"
CAT_BICEPS = "💪 Biceps"
CAT_TRICEPS = "⚡ Triceps"
CAT_HALTERES = "💪 Haltères / Banc"

CATEGORIES = [CAT_JAMBES, CAT_PECS, CAT_DOS, CAT_EPAULES, CAT_BICEPS, CAT_TRICEPS, CAT_HALTERES]

def sauvegarder_donnees():
    """Sauvegarde les données sécurisées (Invalid JSON fix included)"""
    transactions_json = json.loads(st.session_state.transactions.to_json(orient="records"))
    exercices_json = json.loads(pd.DataFrame(st.session_state.exercices_sport).to_json(orient="records"))
    
    donnees_a_sauvegarder = {
        "comptes": st.session_state.comptes,
        "suivi_fixes": st.session_state.suivi_fixes,
        "transactions": transactions_json,
        "objectifs_budget": st.session_state.objectifs_budget,
        "recettes": st.session_state.recettes,
        "menu_semaine": st.session_state.menu_semaine,
        "exercices_sport": exercices_json
    }
    try:
        payload = json.dumps(donnees_a_sauvegarder)
        requests.put(URL_JSONBIN, data=payload, headers=HEADERS)
    except Exception as e:
        st.error(f"Erreur de synchronisation Cloud : {e}")

def charger_donnees():
    """Charge les données depuis le Cloud via JSONBin"""
    try:
        req = requests.get(URL_JSONBIN, headers=HEADERS)
        if req.status_code == 200:
            return req.json().get("record")
    except:
        return None
    return None

# Initialisation des données (Budget + Sport)
if 'initialise_complet' not in st.session_state:
    donnees = charger_donnees()
    
    # --- PARTIE BUDGET ---
    comptes_defaut = {"Compte Courant": 0.0, "Revolut (Crypto)": 0.0, "Mon Livret A": 0.0, "Livret Jeune": 0.0, "BoursoBank": 0.0, "PEE": 0.0}
    # Initialisation des variables Budget (inchangé)
    if donnees and "comptes" in donnees:
        st.session_state.comptes = donnees.get("comptes", comptes_defaut)
        st.session_state.suivi_fixes = donnees.get("suivi_fixes", {})
        trans_data = donnees.get("transactions", [])
        st.session_state.transactions = pd.DataFrame(trans_data) if trans_data else pd.DataFrame(columns=["Mois", "Date", "Type", "Catégorie", "Montant", "Compte"])
        st.session_state.objectifs_budget = donnees.get("objectifs_budget", {})
        st.session_state.recettes = donnees.get("recettes", [])
        st.session_state.menu_semaine = donnees.get("menu_semaine", {})
    else:
        st.session_state.comptes = comptes_defaut
        st.session_state.suivi_fixes = {}
        st.session_state.transactions = pd.DataFrame(columns=["Mois", "Date", "Type", "Catégorie", "Montant", "Compte"])
        st.session_state.objectifs_budget = {}
        st.session_state.recettes = []
        st.session_state.menu_semaine = {}
        
    # --- PARTIE SPORT (VOS EXERCICES) ---
    if donnees and "exercices_sport" in donnees:
        st.session_state.exercices_sport = donnees["exercices_sport"]
    else:
        # Votre liste complète triée
        st.session_state.exercices_sport = [
            {"nom": "Abductor", "categorie": CAT_JAMBES, "poids": 85.0, "reps": 12, "historique": []},
            {"nom": "Leg Press", "categorie": CAT_JAMBES, "poids": 140.0, "reps": 10, "historique": []},
            {"nom": "Leg Curl", "categorie": CAT_JAMBES, "poids": 55.0, "reps": 10, "historique": []},
            {"nom": "Leg Extension", "categorie": CAT_JAMBES, "poids": 55.0, "reps": 12, "historique": []},
            {"nom": "V Squat", "categorie": CAT_JAMBES, "poids": 25.0, "reps": 10, "historique": []},
            {"nom": "Prone Legs Curl", "categorie": CAT_JAMBES, "poids": 32.5, "reps": 12, "historique": []},
            {"nom": "Hack squat", "categorie": CAT_JAMBES, "poids": 40.0, "reps": 10, "historique": []},
            {"nom": "Bench barre (Développé couché)", "categorie": CAT_PECS, "poids": 80.0, "reps": 2, "historique": []},
            {"nom": "Développé couché Assisté", "categorie": CAT_PECS, "poids": 30.0, "reps": 10, "historique": []},
            {"nom": "Chest press", "categorie": CAT_PECS, "poids": 35.0, "reps": 10, "historique": []},
            {"nom": "Pectoral machine", "categorie": CAT_PECS, "poids": 20.0, "reps": 10, "historique": []},
            {"nom": "Pecs debout machine", "categorie": CAT_PECS, "poids": 50.0, "reps": 10, "historique": []},
            {"nom": "Poulie vis à vis Haut", "categorie": CAT_PECS, "poids": 10.0, "reps": 10, "historique": []},
            {"nom": "Poulie vis à vis Milieu", "categorie": CAT_PECS, "poids": 10.0, "reps": 10, "historique": []},
            {"nom": "Poulie vis à vis Bas", "categorie": CAT_PECS, "poids": 7.5, "reps": 10, "historique": []},
            {"nom": "Tirage horizontal", "categorie": CAT_DOS, "poids": 45.0, "reps": 10, "historique": []},
            {"nom": "Tirage horizontal 1 main", "categorie": CAT_DOS, "poids": 30.0, "reps": 10, "historique": []},
            {"nom": "Tirage vertical", "categorie": CAT_DOS, "poids": 55.0, "reps": 10, "historique": []},
            {"nom": "Pull Down", "categorie": CAT_DOS, "poids": 55.0, "reps": 10, "historique": []},
            {"nom": "Row machine", "categorie": CAT_DOS, "poids": 65.0, "reps": 10, "historique": []},
            {"nom": "Frontal pull-down (Fond)", "categorie": CAT_DOS, "poids": 40.0, "reps": 10, "historique": []},
            {"nom": "Low Row", "categorie": CAT_DOS, "poids": 80.0, "reps": 10, "historique": []},
            {"nom": "Épaule machine", "categorie": CAT_EPAULES, "poids": 25.0, "reps": 10, "historique": []},
            {"nom": "Shoulder press épaule", "categorie": CAT_EPAULES, "poids": 25.0, "reps": 10, "historique": []},
            {"nom": "Élévation latérale Machine", "categorie": CAT_EPAULES, "poids": 25.0, "reps": 10, "historique": []},
            {"nom": "Poulie vis à vis Haut / Triceps", "categorie": CAT_TRICEPS, "poids": 27.5, "reps": 10, "historique": []},
            {"nom": "Poulie vis à vis Bas Bibi/Tri", "categorie": CAT_TRICEPS, "poids": 20.0, "reps": 10, "historique": []},
            {"nom": "Poulie Triceps (nuque)", "categorie": CAT_TRICEPS, "poids": 12.0, "reps": 10, "historique": []},
            {"nom": "Triceps Push Down corde", "categorie": CAT_TRICEPS, "poids": 20.0, "reps": 10, "historique": []},
            {"nom": "Extension poulie triceps nuque", "categorie": CAT_TRICEPS, "poids": 12.5, "reps": 10, "historique": []},
            {"nom": "Curl banc allongé (Haltères)", "categorie": CAT_HALTERES, "poids": 30.0, "reps": 10, "historique": []},
            {"nom": "Assis épaule (Haltères)", "categorie": CAT_HALTERES, "poids": 14.0, "reps": 10, "historique": []},
            {"nom": "Curl marteaux (Haltères)", "categorie": CAT_HALTERES, "poids": 12.0, "reps": 10, "historique": []},
            {"nom": "Curl haltère assis", "categorie": CAT_HALTERES, "poids": 12.0, "reps": 11, "historique": []},
            {"nom": "Élévation latérale (Haltères)", "categorie": CAT_HALTERES, "poids": 10.0, "reps": 15, "historique": []},
            {"nom": "Curl Pupitre", "categorie": CAT_HALTERES, "poids": 15.0, "reps": 15, "historique": []},
            {"nom": "Curl Pupitre Altère", "categorie": CAT_HALTERES, "poids": 16.0, "reps": 10, "historique": []}
        ]
        sauvegarder_donnees() # Première sauvegarde Cloud de la liste
    st.session_state.initialise_complet = True

# Initialisation de la variable d'authentification
if 'authentifie' not in st.session_state:
    st.session_state.authentifie = False

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
    /* Style des carrés blancs natifs */
    [data-testid="stVerticalBlockBorderWrapper"] { background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); padding: 10px; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# FONCTION REPRÉSENTATION AMÉLIORÉE DU MANNEQUIN (HTML/SVG)
# ==============================================================================
def afficher_mannequin_pro(categorie_active):
    """Génère et affiche le mannequin anatomique professionnel via HTML natif"""
    
    # Couleurs par défaut (Gris neutre)
    color_body = "#cbd5e1"
    color_highlight = "#ef4444" # Rouge vif

    # Logique d'allumage des zones
    c_pecs = color_body
    c_dos = color_body
    c_jambes_f = color_body # Face
    c_jambes_d = color_body # Dos
    c_epaules = color_body
    c_biceps = color_body
    c_triceps = color_body

    if CAT_PECS in categorie_active: c_pecs = color_highlight
    elif CAT_DOS in categorie_active: c_dos = color_highlight
    elif CAT_JAMBES in categorie_active: 
        c_jambes_f = color_highlight
        c_jambes_d = color_highlight
    elif CAT_EPAULES in categorie_active: c_epaules = color_highlight
    elif CAT_BICEPS in categorie_active: c_biceps = color_highlight
    elif CAT_TRICEPS in categorie_active: c_triceps = color_highlight
    elif CAT_HALTERES in categorie_active:
        # Haltères touche souvent Biceps, Épaules ou Pecs, on allume les bras par défaut
        c_biceps = color_highlight
        c_triceps = color_highlight

    # Code HTML/SVG complet du mannequin professionnel
    html_code = f"""
    <div style="background-color: white; padding: 15px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center;">
        <svg width="280" height="260" viewBox="0 0 300 260">
            <text x="70" y="20" font-family="Arial" font-size="14" font-weight="bold" fill="#475569" text-anchor="middle">FACE</text>
            <g transform="translate(10, 30)">
                <circle cx="60" cy="20" r="15" fill="#cbd5e1" /> <path d="M50 35 L70 35 L75 42 L45 42 Z" fill="#cbd5e1" /> <rect x="42" y="42" width="16" height="22" rx="3" fill="{c_pecs}" /> <rect x="62" y="42" width="16" height="22" rx="3" fill="{c_pecs}" /> <rect x="45" y="66" width="30" height="35" rx="2" fill="#cbd5e1" /> <circle cx="38" cy="48" r="8" fill="{c_epaules}" /> <circle cx="82" cy="48" r="8" fill="{c_epaules}" /> <path d="M28 55 L38 55 L35 90 L25 90 Z" fill="{c_biceps}" /> <path d="M82 55 L92 55 L95 90 L85 90 Z" fill="{c_biceps}" /> <path d="M24 90 L34 90 L32 120 L22 120 Z" fill="#cbd5e1" /> <path d="M86 90 L96 90 L98 120 L88 120 Z" fill="#cbd5e1" /> <path d="M45 102 L58 102 L56 160 L43 160 Z" fill="{c_jambes_f}" /> <path d="M62 102 L75 102 L77 160 L64 160 Z" fill="{c_jambes_f}" /> <rect x="43" y="160" width="13" height="30" rx="2" fill="#cbd5e1" /> <rect x="64" y="160" width="13" height="30" rx="2" fill="#cbd5e1" /> </g>

            <text x="210" y="20" font-family="Arial" font-size="14" font-weight="bold" fill="#475569" text-anchor="middle">DOS</text>
            <g transform="translate(150, 30)">
                <circle cx="60" cy="20" r="15" fill="#cbd5e1" /> <path d="M50 35 L70 35 L75 42 L45 42 Z" fill="#cbd5e1" /> <path d="M40 42 L80 42 L75 90 L45 90 Z" fill="{c_dos}" /> <rect x="48" y="90" width="24" height="12" rx="2" fill="#cbd5e1" /> <circle cx="38" cy="48" r="8" fill="{c_epaules}" /> <circle cx="82" cy="48" r="8" fill="{c_epaules}" /> <path d="M28 55 L38 55 L35 90 L25 90 Z" fill="{c_triceps}" /> <path d="M82 55 L92 55 L95 90 L85 90 Z" fill="{c_triceps}" /> <path d="M24 90 L34 90 L32 120 L22 120 Z" fill="#cbd5e1" /> <path d="M86 90 L96 90 L98 120 L88 120 Z" fill="#cbd5e1" /> <path d="M45 102 L58 102 L56 160 L43 160 Z" fill="{c_jambes_d}" /> <path d="M62 102 L75 102 L77 160 L64 160 Z" fill="{c_jambes_d}" /> <rect x="43" y="160" width="13" height="30" rx="2" fill="#cbd5e1" /> <rect x=" Mollet D -->
            </g>
        </svg>
    </div>
    """
    # NOUVEAU : Affichage pro via le composant HTML
    return components.html(html_code, height=300)

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
    
    # Affichage de chaque exercice dans un carré blanc natif
    for exo in exercices_filtrés:
        # Trouver l'index réel dans la session_state globale
        index_reel = st.session_state.exercices_sport.index(exo)
        
        # Carré blanc natif Streamlit
        with st.container(border=True):
            st.markdown(f"<h3 style='margin-bottom:0;'>{exo['nom']} <span style='font-size:12px; font-weight:normal; background-color:#e2e8f0; padding:2px 8px; border-radius:10px; color:#475569; margin-left:10px;'>{exo['categorie']}</span></h3>", unsafe_allow_html=True)
            
            # Formulaire de modification DIRECTEMENT dans le carré
            c1, c2, c3 = st.columns([1.5, 1.5, 1.5])
            
            poids_saisi = c1.number_input("Poids (kg)", min_value=0.0, value=float(exo["poids"]), step=0.5, key=f"poids_{index_reel}")
            reps_saisie = c2.number_input("Répétitions", min_value=0, value=int(exo["reps"]), step=1, key=f"reps_{index_reel}")
            
            c3.write("") # Petit espacement pour aligner le bouton
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
            
            # Historique et Suppression cachés dans un déroulant
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
    st.write("Le mannequin met en valeur la zone musculaire travaillée par la catégorie sélectionnée à gauche :")
    
    # Affichage du tout nouveau mannequin professionnel
    afficher_mannequin_pro(filtre_cat)
