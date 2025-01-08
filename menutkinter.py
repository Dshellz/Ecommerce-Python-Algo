import tkinter as tk
from tkinter import messagebox
from tkinter import *
import csv
import random
import string
import hashlib
import requests

# Fenêtre principale

def login():
    username=entry1.get()
    password=entry2.get()

    if (username=="" and password==""):
        messagebox.showinfo("","Blank Not Allowed")
    
    elif (username=="User" and password=="admin"):
        messagebox.showinfo("","login success")
    
    else:
        messagebox.showinfo("","Incorrect")

master = tk.Tk()
master.title("Gestion des Produits")
master.geometry("800x450")

global entry1
global entry2

Label(master,text="Username").place(x=20, y=20)
Label(master,text="Password").place(x=20,y=70)

entry1=Entry(master,bd=5)
entry1.place(x=140,y=20)

entry2=Entry(master,bd=5)
entry2.place(x=140,y=70)

Button(master,text="Login", command=login,height=3,width=13, bd=6).place(x=100,y=120)
# Fonction pour afficher les produits
def afficher_produits():
    with open('produits.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        produits_text.delete(1.0, tk.END)  # Vider le champ texte
        for row in reader:
            produits_text.insert(tk.END, f"Commerçant : {row['nom']} : {row['produit']} {row['quantite']} en stock Prix = {row['prix']} €\n")

# Fonction pour ajouter un produit
def ajouter_produit():
    nom = entry_nom.get()
    produit = entry_produit.get()
    quantite = entry_quantite.get()
    prix = entry_prix.get()

    with open('produits.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nom, produit, quantite, prix])
    messagebox.showinfo("Ajout", "Produit ajouté avec succès.")

# Fonction pour supprimer un produit
def supprimer_produit():
    produit_a_supprimer = entry_supprimer.get()
    produits_restants = []
    produit_trouve = False

    with open('produits.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['produit'] != produit_a_supprimer:
                produits_restants.append(row)
            else:
                produit_trouve = True

    if produit_trouve:
        with open('produits.csv', 'w', newline='') as csvfile:
            fieldnames = ['produit', 'quantite', 'prix']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for produit in produits_restants:
                writer.writerow(produit)
        messagebox.showinfo("Suppression", f"Le produit '{produit_a_supprimer}' a été supprimé.")
    else:
        messagebox.showwarning("Erreur", f"Produit '{produit_a_supprimer}' non trouvé.")

# Fonction pour rechercher un produit
def recherche_produit():
    sproduit = entry_recherche.get()
    found = False
    with open("produits.csv", "r", newline='', encoding='utf-8') as fichier:
        donnee = list(csv.reader(fichier, delimiter=";"))
        for ligne in donnee:
            if sproduit.lower() in ligne[0].lower():
                produits_text.delete(1.0, tk.END)
                produits_text.insert(tk.END, f"Produit trouvé : {ligne}\n")
                found = True
                break
    if not found:
        messagebox.showwarning("Recherche", "Produit non trouvé.")

# Fonction pour changer le mot de passe
def change_pw():
    email = entry_email.get()
    old_password = entry_old_pw.get()
    new_password = entry_new_pw.get()
    confirm_pw = entry_confirm_pw.get()

    with open("users.csv", mode="r", encoding='utf-8') as file:
        rows = list(csv.reader(file))

    for row in rows:
        reg_name = row[0]
        reg_pass = row[1]
        if email == reg_name:
            pw_hash = hashlib.sha1(old_password.encode('utf-8')).hexdigest().upper()
            if pw_hash == reg_pass:
                if new_password == confirm_pw:
                    pw_hash_new = hashlib.sha1(new_password.encode('utf-8')).hexdigest().upper()
                    with open("users.csv", mode="w", encoding='utf-8', newline="") as file:
                        writer = csv.writer(file, delimiter=",")
                        for r in rows:
                            if r[0] == email:
                                writer.writerow([r[0], pw_hash_new, r[2]])  # Mise à jour du mot de passe
                            else:
                                writer.writerow(r)
                    messagebox.showinfo("Changement", "Votre mot de passe a été modifié avec succès !")
                    return
                else:
                    messagebox.showwarning("Erreur", "Les mots de passe ne correspondent pas.")
                    return
    messagebox.showwarning("Erreur", "Email ou mot de passe incorrect.")

# Interface utilisateur
frame = tk.Frame(master)
frame.pack(padx=10, pady=10)

# Section d'affichage des produits
produits_text = tk.Text(frame, height=10, width=50)
produits_text.grid(row=0, column=0, columnspan=2, pady=10)

# Section d'ajout de produit
label_nom = tk.Label(frame, text="Nom Commerçant:")
label_nom.grid(row=1, column=0)
entry_nom = tk.Entry(frame)
entry_nom.grid(row=1, column=1)

label_produit = tk.Label(frame, text="Nom Produit:")
label_produit.grid(row=2, column=0)
entry_produit = tk.Entry(frame)
entry_produit.grid(row=2, column=1)

label_quantite = tk.Label(frame, text="Quantité:")
label_quantite.grid(row=3, column=0)
entry_quantite = tk.Entry(frame)
entry_quantite.grid(row=3, column=1)

label_prix = tk.Label(frame, text="Prix:")
label_prix.grid(row=4, column=0)
entry_prix = tk.Entry(frame)
entry_prix.grid(row=4, column=1)

button_ajouter = tk.Button(frame, text="Ajouter Produit", command=ajouter_produit)
button_ajouter.grid(row=5, column=0, columnspan=2)

# Section pour supprimer un produit
label_supprimer = tk.Label(frame, text="Nom du produit à supprimer:")
label_supprimer.grid(row=6, column=0)
entry_supprimer = tk.Entry(frame)
entry_supprimer.grid(row=6, column=1)

button_supprimer = tk.Button(frame, text="Supprimer Produit", command=supprimer_produit)
button_supprimer.grid(row=7, column=0, columnspan=2)

# Section de recherche de produit
label_recherche = tk.Label(frame, text="Nom du produit à rechercher:")
label_recherche.grid(row=8, column=0)
entry_recherche = tk.Entry(frame)
entry_recherche.grid(row=8, column=1)

button_recherche = tk.Button(frame, text="Rechercher Produit", command=recherche_produit)
button_recherche.grid(row=9, column=0, columnspan=2)

# Section de changement de mot de passe
label_email = tk.Label(frame, text="Votre Email:")
label_email.grid(row=10, column=0)
entry_email = tk.Entry(frame)
entry_email.grid(row=10, column=1)

label_old_pw = tk.Label(frame, text="Ancien Mot de Passe:")
label_old_pw.grid(row=11, column=0)
entry_old_pw = tk.Entry(frame, show="*")
entry_old_pw.grid(row=11, column=1)

label_new_pw = tk.Label(frame, text="Nouveau Mot de Passe:")
label_new_pw.grid(row=12, column=0)
entry_new_pw = tk.Entry(frame, show="*")
entry_new_pw.grid(row=12, column=1)

label_confirm_pw = tk.Label(frame, text="Confirmer Nouveau Mot de Passe:")
label_confirm_pw.grid(row=13, column=0)
entry_confirm_pw = tk.Entry(frame, show="*")
entry_confirm_pw.grid(row=13, column=1)

button_change_pw = tk.Button(frame, text="Changer Mot de Passe", command=change_pw)
button_change_pw.grid(row=14, column=0, columnspan=2)

# Lancer l'application
master.mainloop()
