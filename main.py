import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from config import collection

st.set_option('deprecation.showPyplotGlobalUse', False)

# récupérer tous les enregistrements de la collection AllJoueur
records = collection.find({}, {'_id': 0})

# convertir les enregistrements en DataFrame pandas
df = pd.DataFrame(list(records))

# Barre latérale
st.sidebar.header("Filtres")

# Filtres pour les colonnes
selected_teams = st.sidebar.multiselect("Équipes", df["Équipe"].unique())

# Filtrer le DataFrame en fonction des filtres
if selected_teams:
    df = df[df["Équipe"].isin(selected_teams)]

# Nombre de lignes à afficher par page
nblignes = 100

# Nombre total de pages
total_pages = len(df) // nblignes + (len(df) % nblignes != 0)

# Affichage des boutons pour changer de page
page_num = st.number_input("Page :", min_value=1, max_value=total_pages, value=1)

# Fonction pour afficher le DataFrame en fonction du numéro de page
def display_page(page_num):
    start_idx = (page_num - 1) * nblignes
    end_idx = start_idx + nblignes
    st.table(df.iloc[start_idx:end_idx])

# Affichage du tableau pour la page sélectionnée
display_page(page_num)

# Créer un formulaire pour générer des graphiques
with st.form("graph_form"):
    st.write("Sélectionnez les options pour générer un graphique :")
    graph_type = st.selectbox("Type de graphique :", ["bar", "line", "pie"])
    x_axis = st.selectbox("Axe des abscisses (X) :", ["Joueur"])
    y_axis = st.selectbox("Axe des ordonnées (Y) :", ["Taille", "Âge","Poids"])
    submit_button = st.form_submit_button("Générer le graphique")

# Générer et afficher le graphique lors de la soumission du formulaire
if submit_button:
    fig, ax = plt.subplots()
    if graph_type == "bar":
        ax.bar(df[x_axis], df[y_axis])
    elif graph_type == "line":
        ax.plot(df[x_axis], df[y_axis])
    elif graph_type == "pie":
        ax.pie(df[y_axis], labels=df[x_axis], autopct="%1.1f%%")
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(f"{y_axis} en fonction de {x_axis}")
    st.pyplot(fig)
