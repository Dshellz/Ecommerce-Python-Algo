import csv
import pandas as pd
def lire_produits(fichier): #lire le fichier produits.csv
    produits = []
    with open(fichier, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                produit = row[0]
                quantite = int(row[1])
                prix = float(row[2])
                produits.append({'produit': produit, 'quantite': quantite, 'prix': prix})
            return produits

def quicksort_et_afficher(produits): # tri quicksort
    def quicksort_recursive(liste):
        if len(liste) <= 1:
            return liste
        pivot = liste[0]
        moins = [p for p in liste[1:] if p['produit'].lower() <= pivot['produit'].lower()]
        plus = [p for p in liste[1:] if p['produit'].lower() > pivot['produit'].lower()]
        return quicksort_recursive(moins) + [pivot] + quicksort_recursive(plus)

    produits_tries = quicksort_recursive(produits)
    print("\nProduits triés par nom :")
    for produit in produits_tries:
        print(f"{produit['produit']}: {produit['quantite']} en stock Prix = {produit['prix']} €")

def triquicksort(): # triquicksort pour l'appeller dans le menu principale
    fichier = 'produits.csv'
    produits = lire_produits(fichier)

    if not produits:
        print("Aucun produit à afficher.")
        return

    quicksort_et_afficher(produits)

if __name__ == "__main__": # Appel du menu
    triquicksort()
