import csv
from quicksort import triquicksort
from tri_b import tribulle

with open('produits.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)


def afficher_menu(): # Affichage menu avec les options 
    print("\n=== MENU ===")
    print("1| Afficher les produits")
    print("2| Ajouter un nouveau produit")
    print("3| Supprimer un produit")
    print("4| Rechercher un produit")
    print("5| Trier les produits")
    print("6| Trier les noms de produits")
    print("7| Quitter")

def afficher_produits(): # affichier les produits du fichier.csv
 with open('produits.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        print("\n=== LISTE DES PRODUITS ===")
        for row in reader:
            print(f"{row['produit']}: {row['quantite']} en stock, Prix = {row['prix']} €")

def ajouter_produit(produit, quantite, prix): # Ajout d'un produit 
    with open('produits.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([produit, quantite, prix])

def supprimer_produit(): # Suppression d'un produit
    produit_a_supprimer = input("Entrez le nom du produit à supprimer : ")
    produits_restants = []
    produit_trouve = False
    
    with open('produits.csv', newline='') as csvfile: # Cherche si le produit demander existe
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['produit'] != produit_a_supprimer:
                produits_restants.append(row)
            else:
                produit_trouve = True
    if produit_trouve:
        print(f"Le produit '{produit_a_supprimer}' a été supprimé.")
    else:
        print(f"Produit '{produit_a_supprimer}' non trouvé.")
        return
    with open('produits.csv', 'w', newline='') as csvfile: # Réecriture du fichier produits.csv avec les produits restants
        fieldnames = ['produit', 'quantite', 'prix']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for produit in produits_restants:
            writer.writerow(produit)

def recherche_produit(sproduit): # Recherche ligne par ligne
    with open("produits.csv", "r", newline='', encoding='utf-8') as fichier:
        donnee = list(csv.reader(fichier, delimiter=";"))
        for ligne in donnee:
            if sproduit.lower() in ligne[0].lower(): 
                print(f"Produit trouvé : {ligne}")
                break
    
def menu_principal(): # Menu Principale
    while True:
        afficher_menu()
        choix = input("Choisissez une option : ")
        if choix == "1":
            afficher_produits()
        elif choix == "2":
            produit = input("Entrer un nom de produit : ")
            quantite = int(input("Entrer la quantite : "))
            prix = float(input("Entrer un prix : "))
            ajouter_produit(produit, quantite, prix)
        elif choix == "3":
            supprimer_produit()
        elif choix == "4":
            sproduit = input("Entrer le nom du produit que vous cherchez : ")
            print("Si le produit n'apparait pas c'est qu'il n'existe pas.")
            recherche_produit(sproduit)
        elif choix == "5":
            tribulle()
        elif choix == "6":
            triquicksort()
        elif choix == "7":
            print("Au revoir !")
            break
        else:
            print("Option invalide. Veuillez réessayer.")
menu_principal()