from fastapi import FastAPI
from config import collection, client

app = FastAPI(title="Projet Python Avancé Ynov B3",
              description='''Projet réalisé pour le Bachelor 3 Informatique IA&DATA à Ynov Paris
              Sur cette url, vous trouverez une interface streamlit avec des données sur de nombreux joueurs de foot.''',
              version='1.0.0'
              )

@app.get("/getdata")
def getInfoPlayers():
    Data = []
    req = collection.find({}, {'_id': 0})
    Data.append(req)
    return {Data}
