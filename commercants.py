import pandas as pd
import csv 

def filtre_nom():
    choix = input("Vous souhaitez voir les produits appartenants à un commerçant sur la plateforme ? oui/non : ")
    if choix.lower() == "oui":
        try:
            df = pd.read_csv('produits.csv', usecols=['nom'])
        except FileNotFoundError:
            print("Le fichier 'produits.csv' est introuvable. Assurez-vous qu'il est dans le bon répertoire.")
            return
        except Exception as e:
            print(f"Une erreur est survenue lors de la lecture du fichier : {e}")
            return
        
        print("\nListe des commerçants :")
        commercants = df['nom'].dropna().unique()
        for commercant in commercants:
            print(f"| {commercant}")
        
        choix_commercant = input("\nRechercher un commerçant en indiquant son nom : ").strip().lower()
        commercants_lower = [commercant.lower() for commercant in commercants]
        
        if choix_commercant in commercants_lower:
            index_commercant = commercants_lower.index(choix_commercant)
            commercant_exact = commercants[index_commercant]
            print(f"\nVous avez choisi le commerçant : {commercant_exact}")
            
            try:
                df_produits = pd.read_csv('produits.csv')
                produits_commercant = df_produits[df_produits['nom'] == commercant_exact]
                
                if not produits_commercant.empty:
                    print(f"\nLes produits de {commercant_exact} :")
                    print(produits_commercant)
                else:
                    print(f"\nAucun produit trouvé pour {commercant_exact}.")
            except Exception as e:
                print(f"Une erreur est survenue lors de la lecture des produits : {e}") # En cas d'erreur de lecture du fichier csv
        else:
            print("\nLe commerçant n'a pas été trouvé. Veuillez réssayer.")
    else:
        print("Annulé.")