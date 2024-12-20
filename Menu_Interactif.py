import csv
from quicksort import df_sorted
import hashlib
import requests
import string
import random
from tri_b import produits_trie
from logging_log import creer_compte, connection, ajout_prod, mdp_compromis
import pandas as pd
from commercants import filtre_nom
with open('produits.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)


def afficher_menu(): # Affichage menu avec les options 
    print("\n=== MENU ===")
    print("1| Afficher les produits")
    print("2| Ajouter un nouveau produit")
    print("3| Supprimer un produit")
    print("4| Rechercher un produit")
    print("5| Trier les produits par nom")
    print("6| Trier les produits par prix")
    print("7| Rechercher un commerçants")
    print("8| Modifier votre mot de passe")
    print("9| Quitter")

def afficher_produits(): # affichier les produits du fichier.csv
 with open('produits.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        print("\n=== LISTE DES PRODUITS ===")
        for row in reader:
            print(f"Commerçant : {row['nom']} : {row['produit']} {row['quantite']} en stock Prix = {row['prix']} €")

def ajouter_produit(nom, produit, quantite, prix): # Ajout d'un produit 
    with open('produits.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nom ,produit, quantite, prix])
        ajout_prod(nom, produit, quantite, prix) # Pour les logs

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

def quicksort_prix():
    print(df_sorted)

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
        email = input("Entrer un email : ")
        password = input("Entrer votre mot de passe : ")
        password2 = input("Confirmer votre mot de passe : ")
        if password == password2:
            salt = genere_salage()
            # password_salage = password + salt
            pw_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
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
                    mdp_compromis() # Pour les logs 
                    return register()
            if not found :
                print("Mot de passe sécurisé (aucunes traces de fuites de données de ce mot de passe).")
                writer.writerow([email,pw_hash,salt])
                creer_compte(email) # Pour les logs
                print("Votre compte a été créé avec succès ! ")              
        else:
            print("Les mots de passes ne correspondent pas. Veuillez réessayer")
            return register()


def login():
    with open("users.csv", mode="r", encoding='utf-8') as file:
        reader = csv.reader(file)
        email = input("Entrez votre email : ")
        password = input("Entrez votre mot de passe : ")
        for row in reader:
            reg_name = row[0]
            reg_pass = row[1]
            # salt_stocker = row[2] 
            # password_salage = password + salt_stocker
            pw_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            if pw_hash == reg_pass and email == reg_name:
                connection(email) # Pour les logs
                print(f"\nBienvenue {email}")
                return True
    print("Les informations que vous avez rentrez sont incorrectes !")
    return False
def main():
    choix_initial = input("1 | Se connecter\n2 | Créer un compte\nChoisissez une option : ")

    if choix_initial == "1":
        if login():
            pass
        else:
            print("Impossible de se connecter. Réessayez.")
            main()
    elif choix_initial == "2":
        register()
        main()
    else:
        print("Choix invalide. Entrer 1 pour se connecter ou 2 pour créer un compte.")
        main()


if __name__ == "__main__":
    main()

def change_pw():
    email = input("Entrez votre email : ")
    old_password = input("Entrez votre ancien mot de passe : ")

    with open("users.csv", mode="r", encoding='utf-8') as file:
        rows = list(csv.reader(file))
    for row in rows:
        reg_name = row[0]
        reg_pass = row[1]
        
        if email == reg_name:
            pw_hash = hashlib.sha1(old_password.encode('utf-8')).hexdigest().upper()
            if pw_hash == reg_pass:
                print("Ancien mot de passe validé.")
                
                new_password = input("Entrez votre nouveau mot de passe : ")
                new_password2 = input("Confirmez votre nouveau mot de passe : ")
                
                if new_password == new_password2:
                    salt = genere_salage()
                    pw_hash = hashlib.sha1(new_password.encode('utf-8')).hexdigest().upper()
                    
                    with open("users.csv", mode="w", encoding='utf-8', newline="") as file:
                        writer = csv.writer(file, delimiter=",")
                        for r in rows:
                            if r[0] == email:
                                writer.writerow([r[0], pw_hash, salt])
                            else:
                                writer.writerow(r)
                    
                    print("Votre mot de passe a été modifié avec succès !")
                    return True
                else:
                    print("Les mots de passe ne correspondent pas. Veuillez réessayer.")
                    return change_pw()
    print("Email ou mot de passe incorrect.")
    return False

def menu_principal(): # Menu Principale
    while True:
        afficher_menu()
        choix = input("Choisissez une option : ")
        if choix == "1":
            afficher_produits()
        elif choix == "2":
            nom = input("Entrer votre nom : ")
            produit = input("Entrer un nom de produit : ")
            quantite = int(input("Entrer la quantite : "))
            prix = float(input("Entrer un prix : "))
            ajouter_produit(nom, produit, quantite, prix)
        elif choix == "3":
            supprimer_produit()
        elif choix == "4":
            sproduit = input("Entrer le nom du produit que vous cherchez : ")
            print("Si le produit n'apparait pas c'est qu'il n'existe pas.")
            recherche_produit(sproduit)
        elif choix == "5":
            print(produits_trie)
        elif choix == "6":
            quicksort_prix()
        elif choix =="7":
            filtre_nom()
        elif choix == "8":
            change_pw()
        elif choix == "9":
            print("Au revoir !")
            break
        else:
            print("Option invalide. Veuillez réessayer.")
menu_principal()