import pandas as pd
from Menu_Interactif import afficher_menu
import csv 

def filtre_nom():
    choix = input("Vous souhaitez voir les produits appartenants à un commerçants sur la plateforme ? oui/non : ")
    if choix.lower() == "oui":
        df = pd.read_csv('produits.csv', usecols=['nom'])
        print("Liste des commerçants\n")
        for idx, row in df.iterrows():
            print(f"{idx}:{row['nom']}")

    try:
        choix_commercant = int(input("Choisissez le numéro du commerçant : "))
        commercant_choisi = df.iloc[choix_commercant]['nom']
        print(f"Vous avez choisi : {commercant_choisi}")

        df_produits = pd.read_csv('produits.csv')
        produits_commercant = df_produits[df_produits['nom'] == commercant_choisi]
        print(f"Les produits de {commercant_choisi} : ")
        print(produits_commercant)

    except (ValueError, IndexError):
        print("Choix invalide, veuillez réssayer.")
        filtre_nom()
    else:
        return afficher_menu()
        