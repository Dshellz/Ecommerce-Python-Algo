import csv
from quicksort import triquicksort
from tri_b import tribulle
import hashlib
import requests
import string
import random

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
    print("7| Se connecter")
    print("8| Quitter")

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

def genere_salage(lenght=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=lenght))
    
def register():
    with open("users.csv", mode="a", encoding='utf-8', newline="") as f:
        writer = csv.writer(f, delimiter=",")
        name = input("Entrer un nom : ")
        password = input("Entrer votre mot de passe : ")
        password2 = input("Confirmer votre mot de passe : ")
        if password == password2:
            salt = genere_salage()
            password_salage = password + salt
            pw_hash = hashlib.sha1(password_salage.encode('utf-8')).hexdigest().upper()
            prefix = pw_hash[:5]
            suffix = pw_hash[5:] 

            url = f"https://api.pwnedpasswords.com/range/{prefix}"
            response = requests.get(url)
            if response.status_code != 200:
                raise RuntimeError(f"Error: {response.status_code}")
            
            found = False
            hashes = (line.split(':') for line in response.text.splitlines())
            for returned_suffix, count in hashes:
                if returned_suffix == suffix:
                    print(f"Mot de passe trop peu sécurisé ! Il à été compromis {count} fois.\nVeuillez mettre un mot de passe plus sécurisé.")
                    found = True
                    return register()
            if not found :
                print("Mot de passe sécurisé (aucunes traces de fuites de données de ce mot de passe).")
                writer.writerow([name,pw_hash,salt])
                print("Votre compte a été créé avec succès ! ")
                f = open("users.csv", mode="a", encoding='utf-8', newline='')
        else:
            print("Les mots de passes ne correspondent pas. Veuillez réessayer")


def login():
    with open("users.csv", mode="r", encoding='utf-8') as file:
        reader = csv.reader(file)
        name = input("Entrez votre nom : ")
        password = input("Entrez votre mot de passe : ")
        for row in reader:
            reg_name = row[0]
            reg_pass = row[1]
            salt_stocker = row[2]
            password_salage = password + salt_stocker
            pw_hash = hashlib.sha1(password_salage.encode('utf-8')).hexdigest().upper()
            if pw_hash == reg_pass and name == reg_name:
                print(f"\nBienvenue {name}")
                return True
    print("Les informations que vous avez rentrez sont incorrectes !")
    choix = input("1| Se créer un compte\n2| Se connecter\n ") 
    if choix == "1":
        register()
    elif choix =="2":
        login()
    return afficher_menu()

choix = input("1| Se créer un compte\n2| Se connecter\n ")
if choix == "1":
    register()
elif choix =="2":
    login()

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
        elif choix =="7":
            login()
        elif choix == "8":
            print("Au revoir !")
            break
        else:
            print("Option invalide. Veuillez réessayer.")
menu_principal()