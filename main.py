import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Connexion MongoDB Atlas
uri = "mongodb+srv://bhamoudan:rawdawraw@cluster0.eu2ysuu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command("ping")
    db = client["transport_api"]
    lignes = db["lignes"]
    utilisateurs = db["utilisateurs"]
    reservations = db["reservations"]
    itineraire_temp = db["itineraire_en_cours"]
    avis = db["avis_utilisateurs"]
    st.success("✅ Connexion MongoDB réussie")
except Exception as e:
    st.error(f"❌ Erreur de connexion : {e}")
    st.stop()

st.title("🚌 Interface MongoDB - Gestion Transport")

# Menu de navigation
choix = st.sidebar.radio("📂 Que veux-tu afficher ?", [
    "Lignes", "Utilisateurs", "Itinéraires en cours", "Réservations", "Avis"
])

if choix == "Lignes":
    st.header("🚌 Lignes de transport")
    data = list(lignes.find())
    for ligne in data:
        st.subheader(f"📍 {ligne.get('nom', '')}")
        st.write(f"Type : {ligne.get('type', '')}")
        st.write(f"Catégorie : {ligne.get('categorie', '')}")
        st.write(f"Fréquence : {ligne.get('frequence', '')} min")
        st.write(f"Horaires : {ligne.get('horaires', {}).get('debut', '')} - {ligne.get('horaires', {}).get('fin', '')}")
        st.write("Arrêts :", ligne.get('arrets', []))
        st.markdown("---")

elif choix == "Utilisateurs":
    st.header("👤 Utilisateurs")
    data = list(utilisateurs.find())
    for user in data:
        st.subheader(user.get("nom", ""))
        st.write(f"Email : {user.get('email')}")
        st.write(f"Adresse : {user.get('adresse')}")
        st.markdown("---")

elif choix == "Itinéraires en cours":
    st.header("🗺️ Itinéraires temporaires")
    data = list(itineraire_temp.find())
    for iti in data:
        st.subheader(f"Utilisateur : {iti.get('email_utilisateur')}")
        st.write("Trajets sélectionnés :")
        for t in iti.get("trajets_selectionnes", []):
            st.write(f"- {t.get('depart')} → {t.get('arrivee')}")
        st.write(f"Prix total : {iti.get('prix_total')} MAD")
        st.markdown("---")

elif choix == "Réservations":
    st.header("🎟️ Réservations")
    data = list(reservations.find())
    for res in data:
        st.subheader(f"Réservation de {res.get('email_utilisateur')}")
        st.write(f"Date : {res.get('date')}")
        st.write(f"Statut paiement : {res.get('statut_paiement')}")
        st.write(f"Statut transport : {res.get('statut_transport')}")
        st.write("Trajets :")
        for t in res.get("trajets", []):
            st.write(f"- {t.get('depart')} → {t.get('arrivee')} ({t.get('prix')} MAD)")
        st.markdown("---")

elif choix == "Avis":
    st.header("⭐ Avis utilisateurs")
    data = list(avis.find())
    for a in data:
        st.subheader(f"Utilisateur : {a.get('email_utilisateur')}")
        st.write(f"Ligne ID : {a.get('ligne_id')}")
        st.write(f"Note : ⭐ {a.get('note')}/5")
        st.write(f"Commentaire : {a.get('commentaire')}")
        st.markdown("---")
