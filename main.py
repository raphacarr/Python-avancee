 ##########################################################################################################
 #                                                                                                        #
 #                                              IMPORTS                                                   #
 #                                                                                                        #
 ##########################################################################################################
 
import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from config import collection

 ##########################################################################################################
 #                                                                                                        #
 #                                         APPEL MONGO                                                    #
 #                                                                                                        #
 ##########################################################################################################

records = collection.find({}, {'_id': 0})
df = pd.DataFrame(list(records))

 ##########################################################################################################
 #                                                                                                        #
 #                                          NETTOYAGE DATAFRAME                                           #
 #                                                                                                        #
 ##########################################################################################################
def clean_dataframe(df): 
    df["Âge"] = pd.to_numeric(df["Âge"], errors='coerce')
    df["Taille"] = pd.to_numeric(df["Taille"], errors='coerce')
    df["Poids"] = pd.to_numeric(df["Poids"], errors='coerce')
    df["Salaire"] = df["Salaire"].str.replace("€", "").str.replace(" ", "")
    df["Salaire"] = df["Salaire"].str.replace(".", "")
    df["Salaire"] = df["Salaire"].str.replace("M", "000000").str.replace("K","000")
    df["Salaire"] = pd.to_numeric(df["Salaire"], errors='coerce')
    df = df.dropna(subset=["Âge", "Taille", "Poids"])
    df[["Âge", "Taille", "Poids"]] = df[["Âge", "Taille", "Poids"]].astype(int)
    return df

 ##########################################################################################################
 #                                                                                                        #
 #                                              STREAMLIT                                                 #
 #                                                                                                        #
 ##########################################################################################################

st.set_option('deprecation.showPyplotGlobalUse', False)
 
st.sidebar.header("Filtres")
selection_equipe = st.sidebar.multiselect("Équipes", df["Équipe"].unique())

# Filtrer le DataFrame en fonction des filtres
if selection_equipe:
    df = df[df["Équipe"].isin(selection_equipe)]

# Fonction pour ajouter un joueur au DataFrame
def ajouter_joueur(num,moy, joueur, equipe,selection, age, taille, poids, salaire):
    global df
    nouveau_joueur = {"#": num, "Moy.": moy, "Joueur":joueur, "Équipe": equipe,"Sélection":selection, "Âge": age, "Taille": taille, "Poids": poids, "Salaire": salaire}
    df = df.append(nouveau_joueur, ignore_index=True)
    collection.insert_one(nouveau_joueur)
    st.success("Le joueur a été ajouté avec succès !")

with st.sidebar.expander("Ajouter un joueur"):
    num = st.number_input("n° dans le classement", min_value=1, max_value=5000, value=10 , step=1)
    moy = st.number_input("note moyenne du joueur", min_value=0.0, max_value=10.0, value=5.5 , step=0.1)
    joueur = st.text_input("Joueur")
    equipe = st.selectbox("Équipe", df["Équipe"].unique())
    selection = st.selectbox("Sélection nationale",df["Sélection"].unique() )
    age = st.number_input("Âge", min_value=0, max_value=100, value=18)
    taille = st.number_input("Taille (cm)", min_value=0, max_value=300, value=170 , step=1)
    poids = st.number_input("Poids (kg)", min_value=0, max_value=500, value=70 , step=1)
    salaire = st.number_input("Salaire (€)", min_value=0)
    
    if st.button("Ajouter"):
        if num and moy and joueur and equipe and selection and age and taille and poids and salaire: #Critères
            ajouter_joueur(num, moy, joueur, equipe, selection, age, taille, poids, salaire)
        else:
            st.error("Veuillez remplir tous les champs !")    

# Nombre de lignes à afficher par page
nblignes = 100
# Nombre total de pages
total_pages = len(df) // nblignes + (len(df) % nblignes != 0)
page_num = st.number_input("Page :", min_value=1, max_value=total_pages, value=1)

def display_app(page_num):
    start_idx = (page_num - 1) * nblignes
    end_idx = start_idx + nblignes
    st.table(df.iloc[start_idx:end_idx])

# Affichage du tableau en fonction de la page sélectionnée
with st.expander("Afficher le tableau des données"):
    clean_dataframe(df)
    display_app(page_num)

 ##########################################################################################################
 #                                                                                                        #
 #                                              GRAPHIQUES                                                #
 #                                                                                                        #
 ##########################################################################################################
 
with st.sidebar.expander("Graphiques"):
    
    afficher_histoGraph_age = st.checkbox("Histogramme des âges")
    afficher_nbJoueursEquipe = st.checkbox("Nombre de joueurs par équipe dans le top Euro")
    afficher_moyTaille = st.checkbox("Moyenne de la taille par équipe")
    afficher_BoxGraph_Poids = st.checkbox("Diagramme en boîte du poids par équipe")
    afficher_bubble_age_poids_taille = st.checkbox("Diagramme à bulles : Âge vs Taille, Poids et Équipe")
    afficher_heatmap_moyAge_Equipe = st.checkbox("Carte de chaleur de la moyenne de l'âge par équipe")
    afficher_NuageGraph_age_poids = st.checkbox("Nuage de points : Âge vs Poids")
    afficherTranche_d_Age = st.checkbox("Répartition des joueurs par tranche d'âge et par équipe")
    afficher_moySalaire = st.checkbox("Moyenne du salaire par équipe")
       
# Affichage des graphiques en fonction des cases à cocher sélectionnées
if afficher_nbJoueursEquipe:
    st.subheader("Nombre de joueurs par équipe")
    fig, ax = plt.subplots()
    team_counts = df["Équipe"].value_counts()
    team_counts.plot(kind="bar", ax=ax)
    ax.set_xlabel("Équipe")
    ax.set_ylabel("Nombre de joueurs")
    ax.set_title("Nombre de joueurs par équipe")
    st.pyplot(fig)

if afficher_histoGraph_age:
    st.subheader("Histogramme des âges des joueurs")
    fig, ax = plt.subplots()
    ax.hist(df["Âge"], bins=20)
    ax.set_xlabel("Âge")
    ax.set_ylabel("Fréquence")
    ax.set_title("Histogramme des âges")
    st.pyplot(fig)
    
if afficher_moyTaille:
    st.subheader("Moyenne de la taille des joueurs en fonction des équipes")
    fig, ax = plt.subplots()
    avg_height_by_team = df.groupby("Équipe")["Taille"].mean()
    avg_height_by_team.plot(kind='bar', ax=ax)
    ax.set_xlabel("Équipe")
    ax.set_ylabel("Moyenne de la taille (cm)")
    ax.set_title("Moyenne de la taille des joueurs par équipe")
    st.pyplot(fig)
    
if afficher_BoxGraph_Poids:
    st.subheader("Diagramme en boîte du poids des joueurs en fonction des équipes")
    fig, ax = plt.subplots()
    sns.boxplot(x="Équipe", y="Poids", data=df, ax=ax)
    ax.set_title("Poids des joueurs en fonction des équipes")
    st.pyplot(fig)
    
if afficher_bubble_age_poids_taille:
    st.subheader("Diagramme à bulles : Âge vs Taille, Poids et Équipe")
    fig, ax = plt.subplots()
    sns.scatterplot(x="Âge", y="Taille", size="Poids", hue="Équipe", data=df, ax=ax, sizes=(20, 200), alpha=0.5)
    ax.set_title("Diagramme à bulles : Âge / Taille / Poids / Equipes")
    st.pyplot(fig)

if afficher_heatmap_moyAge_Equipe:
    st.subheader(" Moyenne de l'âge des joueurs en fonction des équipes")
    fig, ax = plt.subplots()
    moy_age = df.groupby("Équipe")["Âge"].mean().reset_index()
    team_pivot = moy_age.pivot_table(index="Équipe", values="Âge")
    sns.heatmap(team_pivot, annot=True, fmt=".1f", cmap="coolwarm", ax=ax)
    ax.set_title(" Moyenne de l'âge des joueurs en fonction des équipes")
    st.pyplot(fig)

if afficher_NuageGraph_age_poids:
    st.subheader("Nuage de points : Âge / Poids")
    fig, ax = plt.subplots()
    sns.scatterplot(x="Âge", y="Poids", data=df, ax=ax)
    ax.set_title(" Comparaisons Âge / Poids")
    st.pyplot(fig)

if afficherTranche_d_Age:
    st.subheader("Répartition des joueurs par tranche d'âge et par équipe")
    fig, ax = plt.subplots()

    # Créer une nouvelle colonne 'Tranche d'âge' pour classer les joueurs par tranche d'âge
    tranche_d_age = [15, 20, 25, 30, 35, 40, 100]
    age_labels = ["15-19", "20-24", "25-29", "30-34", "35-39", "40+"]
    df["Tranche d'âge"] = pd.cut(df["Âge"], bins=tranche_d_age, labels=age_labels)

    # Créer un DataFrame pivot pour le graphique à barres empilées
    pivot_df = df.groupby(["Équipe", "Tranche d'âge"]).size().reset_index(name="Nombre de joueurs")
    pivot_df = pivot_df.pivot_table(index="Équipe", columns="Tranche d'âge", values="Nombre de joueurs", fill_value=0)

    # Créer le graphique à barres empilées
    pivot_df.plot(kind='bar', stacked=True, ax=ax)
    ax.set_ylabel("Nombre de joueurs")
    ax.set_title("Répartition des joueurs par tranche d'âge et par équipe")
    st.pyplot(fig)
    
if afficher_moySalaire:
    st.subheader("Moyenne du salaire des joueurs par équipe")
    fig, ax = plt.subplots()
    moy_salaire = df.groupby("Équipe")["Salaire"].mean()
    moy_salaire.plot(kind='bar', ax=ax)
    ax.set_xlabel("Équipe")
    ax.set_ylabel("Moyenne du salaire")
    ax.set_title("Moyenne du salaire des joueurs par équipe")
    st.pyplot(fig)
